import { useEffect, useRef, useState } from "react";
import "./styles.css";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

function App() {
  const editorRef = useRef(null);

  const [users, setUsers] = useState([]);
  const [currentUserId, setCurrentUserId] = useState(1);

  const [ownedDocs, setOwnedDocs] = useState([]);
  const [sharedDocs, setSharedDocs] = useState([]);
  const [sharedByMeDocs, setSharedByMeDocs] = useState([]);

  const [selectedDoc, setSelectedDoc] = useState(null);
  const [title, setTitle] = useState("");
  const [contentHtml, setContentHtml] = useState("");

  const [shareUserId, setShareUserId] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadUsers();
  }, []);

  useEffect(() => {
    loadDocuments();
    clearEditor();
  }, [currentUserId]);

  useEffect(() => {
  if (editorRef.current) {
    editorRef.current.innerHTML = selectedDoc?.content_html || "";
  }
}, [selectedDoc?.id]);

  async function loadUsers() {
    try {
      const response = await fetch(`${API_BASE}/users`);
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      setMessage("Could not load users. Make sure backend is running.");
    }
  }

  async function loadDocuments() {
    try {
      const response = await fetch(`${API_BASE}/documents?user_id=${currentUserId}`);
      const data = await response.json();
      setOwnedDocs(data.owned || []);
      setSharedDocs(data.shared || []);
      setSharedByMeDocs(data.shared_by_me || []);
    } catch (error) {
      setMessage("Could not load documents. Make sure backend is running.");
    }
  }

  function clearEditor() {
    setSelectedDoc(null);
    setTitle("");
    setContentHtml("");
    setShareUserId("");
    if (editorRef.current) {
      editorRef.current.innerHTML = "";
    }
  }

  async function createNewDocument() {
    try {
      const response = await fetch(`${API_BASE}/documents`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: "Untitled Document",
          owner_id: currentUserId,
        }),
      });

      const document = await response.json();

      if (!response.ok) {
        setMessage(document.detail || "Could not create document.");
        return;
      }

      setSelectedDoc(document);
      setTitle(document.title);
      setContentHtml(document.content_html || "");
      setMessage("New document created.");
      await loadDocuments();
    } catch (error) {
      setMessage("Error creating document.");
    }
  }

  async function openDocument(doc) {
    try {
      const response = await fetch(
        `${API_BASE}/documents/${doc.id}?user_id=${currentUserId}`
      );

      const document = await response.json();

      if (!response.ok) {
        setMessage(document.detail || "Could not open document.");
        return;
      }

      setSelectedDoc(document);
      setTitle(document.title);
      setContentHtml(document.content_html || "");
      setShareUserId("");
      setMessage("");
    } catch (error) {
      setMessage("Error opening document.");
    }
  }

  async function saveDocument() {
    if (!selectedDoc) {
      setMessage("Please select or create a document first.");
      return;
    }

    if (!title.trim()) {
      setMessage("Document title cannot be empty.");
      return;
    }

    const latestContent = editorRef.current ? editorRef.current.innerHTML : "";

    try {
      const response = await fetch(`${API_BASE}/documents/${selectedDoc.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: title,
          content_html: latestContent,
          user_id: currentUserId,
        }),
      });

      const updatedDocument = await response.json();

      if (!response.ok) {
        setMessage(updatedDocument.detail || "Could not save document.");
        return;
      }

      setSelectedDoc(updatedDocument);
      setContentHtml(updatedDocument.content_html || "");
      setMessage("Document saved successfully.");
      await loadDocuments();
    } catch (error) {
      setMessage("Error saving document.");
    }
  }

  async function shareDocument() {
    if (!selectedDoc) {
      setMessage("Please select a document first.");
      return;
    }

    if (!shareUserId) {
      setMessage("Please select a user to share with.");
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/documents/${selectedDoc.id}/share`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          owner_id: currentUserId,
          shared_with_user_id: Number(shareUserId),
        }),
      });

      const result = await response.json();

      if (!response.ok) {
        setMessage(result.detail || "Could not share document.");
        return;
      }

      setMessage("Document shared successfully.");
      setShareUserId("");
      await loadDocuments();
    } catch (error) {
      setMessage("Error sharing document.");
    }
  }

  async function uploadFile(event) {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    const lowerName = file.name.toLowerCase();

    if (!lowerName.endsWith(".txt") && !lowerName.endsWith(".md")) {
      setMessage("Only .txt and .md files are supported.");
      event.target.value = "";
      return;
    }

    const formData = new FormData();
    formData.append("owner_id", currentUserId);
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE}/documents/upload`, {
        method: "POST",
        body: formData,
      });

      const document = await response.json();

      if (!response.ok) {
        setMessage(document.detail || "Could not upload file.");
        return;
      }

      setSelectedDoc(document);
      setTitle(document.title);
      setContentHtml(document.content_html || "");
      setMessage("File uploaded and converted into a document.");
      await loadDocuments();
    } catch (error) {
      setMessage("Error uploading file.");
    }

    event.target.value = "";
  }

  function applyFormat(command, value = null) {
    if (!editorRef.current) {
      return;
    }

    editorRef.current.focus();
    document.execCommand(command, false, value);
    setContentHtml(editorRef.current.innerHTML);
  }

  function handleEditorInput() {
    if (editorRef.current) {
      setContentHtml(editorRef.current.innerHTML);
    }
  }

  const currentUser = users.find((u) => u.id === Number(currentUserId));
  const shareableUsers = users.filter((u) => u.id !== Number(currentUserId));

  return (
    <div className="app">
      <aside className="sidebar">
        <h1>DocLite</h1>
        <p className="subtitle">Lightweight collaborative document editor</p>

        <label className="label">Logged in as</label>
        <select
          className="select"
          value={currentUserId}
          onChange={(e) => setCurrentUserId(Number(e.target.value))}
        >
          {users.map((user) => (
            <option key={user.id} value={user.id}>
              {user.name}
            </option>
          ))}
        </select>

        <button className="primary-btn" onClick={createNewDocument}>
          + New Document
        </button>

        <div className="upload-box">
          <label className="label">Upload .txt or .md</label>
          <input type="file" accept=".txt,.md" onChange={uploadFile} />
          <small>Supported files: .txt and .md only</small>
        </div>

        <div className="doc-section">
          <h2>My Documents</h2>
          {ownedDocs.length === 0 && <p className="empty">No owned documents.</p>}
          {ownedDocs.map((doc) => (
            <button
              key={doc.id}
              className={`doc-item ${
                selectedDoc && selectedDoc.id === doc.id ? "active" : ""
              }`}
              onClick={() => openDocument(doc)}
            >
              {doc.title}
            </button>
          ))}
        </div>

        <div className="doc-section">
          <h2>Shared With Me</h2>
          {sharedDocs.length === 0 && <p className="empty">No shared documents.</p>}
          {sharedDocs.map((doc) => (
            <button
              key={doc.id}
              className={`doc-item ${
                selectedDoc && selectedDoc.id === doc.id ? "active" : ""
              }`}
              onClick={() => openDocument(doc)}
            >
              {doc.title}
            </button>
          ))}
        </div>

        <div className="doc-section">
          <h2>Shared By Me</h2>
          {sharedByMeDocs.length === 0 && (
            <p className="empty">No documents shared by me.</p>
          )}

          {sharedByMeDocs.map((doc) => (
            <button
              key={`${doc.id}-${doc.shared_with_user_id}`}
              className={`doc-item ${
                selectedDoc && selectedDoc.id === doc.id ? "active" : ""
              }`}
              onClick={() => openDocument(doc)}
            >
              <span>{doc.title}</span>
              <small className="shared-note">
                Shared with {doc.shared_with_name}
              </small>
            </button>
          ))}
         </div>
      </aside>

      <main className="editor-panel">
        <div className="top-bar">
          <div>
            <h2>
              {selectedDoc
                ? `Editing as ${currentUser?.name || "User"}`
                : "No document selected"}
            </h2>
            <p>
              Create a document, upload a file, or open an existing document.
            </p>
          </div>

          <button className="save-btn" onClick={saveDocument}>
            Save
          </button>
        </div>

        {message && <div className="message">{message}</div>}

        <input
          className="title-input"
          placeholder="Document title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={!selectedDoc}
        />

        <div className="toolbar">
          <button onClick={() => applyFormat("bold")}>Bold</button>
          <button onClick={() => applyFormat("italic")}>Italic</button>
          <button onClick={() => applyFormat("underline")}>Underline</button>
          <button onClick={() => applyFormat("formatBlock", "H1")}>Heading</button>
          <button onClick={() => applyFormat("formatBlock", "P")}>Normal</button>
          <button onClick={() => applyFormat("insertUnorderedList")}>Bullets</button>
          <button onClick={() => applyFormat("insertOrderedList")}>Numbers</button>
        </div>

        <div
          ref={editorRef}
          className="editor"
          contentEditable={!!selectedDoc}
          onInput={handleEditorInput}
          suppressContentEditableWarning={true}
          data-placeholder="Start typing your document here..."
        ></div>

        <div className="share-box">
          <h3>Share Document</h3>

          <select
            className="select"
            value={shareUserId}
            onChange={(e) => setShareUserId(e.target.value)}
            disabled={!selectedDoc}
          >
            <option value="">Select user</option>
            {shareableUsers.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name}
              </option>
            ))}
          </select>

          <button className="secondary-btn" onClick={shareDocument}>
            Share
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;