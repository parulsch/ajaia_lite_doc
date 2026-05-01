<<<<<<< HEAD
# DocLite

DocLite is a lightweight collaborative document editor inspired by Google Docs. It was built as a focused full-stack MVP for the AJAIA AI Implementation Manager / Project Manager assessment.

The app allows seeded users to create, edit, save, upload, and share documents.

## Seeded Users

The app uses seeded users instead of full authentication.

- Alice Morgan
- Ben Carter
- Priya Shah

Use the dropdown in the app to switch between users.

## Core Features

- Create a new document
- Rename a document
- Edit document content in browser
- Basic rich-text formatting:
  - Bold
  - Italic
  - Underline
  - Heading
  - Bulleted list
  - Numbered list
- Save and reopen documents
- Upload `.txt` or `.md` files as editable documents
- Share documents with another seeded user
- View documents in:
  - My Documents
  - Shared With Me
  - Shared By Me
- SQLite persistence
- Basic validation and error handling
- One automated backend test

## Supported File Types

This MVP supports only:

- `.txt`
- `.md`

DOCX, PDF, and image uploads were intentionally deprioritized.

## Local Setup

### Backend

Open a terminal:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
=======
# DocLite

DocLite is a lightweight collaborative document editor inspired by Google Docs. It was built as a focused full-stack MVP for the AJAIA AI Implementation Manager / Project Manager assessment.

The app allows seeded users to create, edit, save, upload, and share documents.

## Seeded Users

The app uses seeded users instead of full authentication.

- Alice Morgan
- Ben Carter
- Priya Shah

Use the dropdown in the app to switch between users.

## Core Features

- Create a new document
- Rename a document
- Edit document content in browser
- Basic rich-text formatting:
  - Bold
  - Italic
  - Underline
  - Heading
  - Bulleted list
  - Numbered list
- Save and reopen documents
- Upload `.txt` or `.md` files as editable documents
- Share documents with another seeded user
- View documents in:
  - My Documents
  - Shared With Me
  - Shared By Me
- SQLite persistence
- Basic validation and error handling
- One automated backend test

## Supported File Types

This MVP supports only:

- `.txt`
- `.md`

DOCX, PDF, and image uploads were intentionally deprioritized.

## Local Setup

### Backend

Open a terminal:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
>>>>>>> 37e21760ae63c1531bb307cd25709b73c6fe789e
python -m uvicorn main:app --reload

Live Product URL: your Vercel frontend URL
Backend API URL: your Render backend URL