import os
import sqlite3
import html
from datetime import datetime

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# SQLite database file
DB_FILE = "doclite.db"

app = FastAPI(title="DocLite API")


# Allows frontend React app to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Database helper functions
# -----------------------------

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def now():
    return datetime.utcnow().isoformat()


def row_to_dict(row):
    if row is None:
        return None
    return dict(row)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Users table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        """
    )

    # Documents table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content_html TEXT NOT NULL DEFAULT '',
            owner_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(owner_id) REFERENCES users(id)
        )
        """
    )

    # Sharing table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS document_shares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            shared_with_user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(document_id) REFERENCES documents(id),
            FOREIGN KEY(shared_with_user_id) REFERENCES users(id),
            UNIQUE(document_id, shared_with_user_id)
        )
        """
    )

    # Seed fake users
    users = [
        (1, "Alice Morgan", "alice@doclite.local"),
        (2, "Ben Carter", "ben@doclite.local"),
        (3, "Priya Shah", "priya@doclite.local"),
    ]

    cur.executemany(
        """
        INSERT OR IGNORE INTO users (id, name, email)
        VALUES (?, ?, ?)
        """,
        users,
    )

    conn.commit()
    conn.close()


# Create DB tables when app starts
init_db()


def user_exists(user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()

    conn.close()
    return user is not None


def can_access_document(document_id: int, user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    # Owner can access
    cur.execute(
        """
        SELECT id FROM documents
        WHERE id = ? AND owner_id = ?
        """,
        (document_id, user_id),
    )

    if cur.fetchone():
        conn.close()
        return True

    # Shared user can access
    cur.execute(
        """
        SELECT id FROM document_shares
        WHERE document_id = ? AND shared_with_user_id = ?
        """,
        (document_id, user_id),
    )

    shared = cur.fetchone()
    conn.close()

    return shared is not None


# -----------------------------
# Request models
# -----------------------------

class DocumentCreate(BaseModel):
    title: str = "Untitled Document"
    owner_id: int


class DocumentUpdate(BaseModel):
    title: str
    content_html: str
    user_id: int


class ShareRequest(BaseModel):
    owner_id: int
    shared_with_user_id: int


# -----------------------------
# API routes
# -----------------------------

@app.get("/")
def home():
    return {"message": "DocLite API is running"}


@app.get("/users")
def get_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, email FROM users ORDER BY id")
    rows = cur.fetchall()

    conn.close()

    return [row_to_dict(row) for row in rows]


@app.get("/documents")
def get_documents(user_id: int):
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")

    conn = get_connection()
    cur = conn.cursor()

    # Documents owned by user
    cur.execute(
        """
        SELECT *
        FROM documents
        WHERE owner_id = ?
        ORDER BY updated_at DESC
        """,
        (user_id,),
    )
    owned_docs = [row_to_dict(row) for row in cur.fetchall()]

    # Documents shared with user
    cur.execute(
        """
        SELECT d.*
        FROM documents d
        JOIN document_shares s
        ON d.id = s.document_id
        WHERE s.shared_with_user_id = ?
        ORDER BY d.updated_at DESC
        """,
        (user_id,),
    )
    shared_docs = [row_to_dict(row) for row in cur.fetchall()]

    # Documents this user has shared with others
    cur.execute(
        """
        SELECT
            d.id,
            d.title,
            d.content_html,
            d.owner_id,
            d.created_at,
            d.updated_at,
            u.id AS shared_with_user_id,
            u.name AS shared_with_name,
            u.email AS shared_with_email
        FROM documents d
        JOIN document_shares s
        ON d.id = s.document_id
        JOIN users u
        ON s.shared_with_user_id = u.id
        WHERE d.owner_id = ?
        ORDER BY d.updated_at DESC
        """,
        (user_id,),
    )
    shared_by_me = [row_to_dict(row) for row in cur.fetchall()]

    conn.close()

    return {
        "owned": owned_docs,
        "shared": shared_docs,
        "shared_by_me": shared_by_me,
    }

@app.get("/documents/{document_id}")
def get_document(document_id: int, user_id: int):
    if not can_access_document(document_id, user_id):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this document",
        )

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM documents
        WHERE id = ?
        """,
        (document_id,),
    )

    document = row_to_dict(cur.fetchone())
    conn.close()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document


@app.post("/documents")
def create_document(payload: DocumentCreate):
    if not user_exists(payload.owner_id):
        raise HTTPException(status_code=404, detail="Owner user not found")

    title = payload.title.strip()

    if not title:
        title = "Untitled Document"

    created_time = now()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO documents (
            title,
            content_html,
            owner_id,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            title,
            "",
            payload.owner_id,
            created_time,
            created_time,
        ),
    )

    document_id = cur.lastrowid
    conn.commit()

    cur.execute(
        """
        SELECT *
        FROM documents
        WHERE id = ?
        """,
        (document_id,),
    )

    document = row_to_dict(cur.fetchone())
    conn.close()

    return document


@app.put("/documents/{document_id}")
def update_document(document_id: int, payload: DocumentUpdate):
    if not payload.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Document title cannot be empty",
        )

    if not can_access_document(document_id, payload.user_id):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to update this document",
        )

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE documents
        SET title = ?,
            content_html = ?,
            updated_at = ?
        WHERE id = ?
        """,
        (
            payload.title.strip(),
            payload.content_html,
            now(),
            document_id,
        ),
    )

    conn.commit()

    cur.execute(
        """
        SELECT *
        FROM documents
        WHERE id = ?
        """,
        (document_id,),
    )

    updated_document = row_to_dict(cur.fetchone())
    conn.close()

    return updated_document


@app.post("/documents/{document_id}/share")
def share_document(document_id: int, payload: ShareRequest):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM documents
        WHERE id = ?
        """,
        (document_id,),
    )

    document = cur.fetchone()

    if not document:
        conn.close()
        raise HTTPException(status_code=404, detail="Document not found")

    # Only owner can share
    if document["owner_id"] != payload.owner_id:
        conn.close()
        raise HTTPException(
            status_code=403,
            detail="Only the owner can share this document",
        )

    # Cannot share with self
    if payload.owner_id == payload.shared_with_user_id:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="You cannot share a document with yourself",
        )

    if not user_exists(payload.shared_with_user_id):
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="User to share with was not found",
        )

    try:
        cur.execute(
            """
            INSERT INTO document_shares (
                document_id,
                shared_with_user_id,
                created_at
            )
            VALUES (?, ?, ?)
            """,
            (
                document_id,
                payload.shared_with_user_id,
                now(),
            ),
        )

        conn.commit()

    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Document is already shared with this user",
        )

    conn.close()

    return {"message": "Document shared successfully"}


@app.post("/documents/upload")
async def upload_document(
    owner_id: int = Form(...),
    file: UploadFile = File(...),
):
    if not user_exists(owner_id):
        raise HTTPException(status_code=404, detail="Owner user not found")

    filename = file.filename or ""
    filename_lower = filename.lower()

    # Only allow .txt and .md
    if not (
        filename_lower.endswith(".txt")
        or filename_lower.endswith(".md")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .md files are supported",
        )

    file_bytes = await file.read()

    try:
        text_content = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be a UTF-8 text file",
        )

    # Convert text into safe HTML
    safe_text = html.escape(text_content)
    safe_text = safe_text.replace("\n", "<br/>")
    content_html = f"<p>{safe_text}</p>"

    title = os.path.splitext(filename)[0]

    if not title:
        title = "Uploaded Document"

    created_time = now()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO documents (
            title,
            content_html,
            owner_id,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            title,
            content_html,
            owner_id,
            created_time,
            created_time,
        ),
    )

    document_id = cur.lastrowid
    conn.commit()

    cur.execute(
        """
        SELECT *
        FROM documents
        WHERE id = ?
        """,
        (document_id,),
    )

    document = row_to_dict(cur.fetchone())
    conn.close()

    return document