<<<<<<< HEAD
# Submission

## Project Name

DocLite – Lightweight Collaborative Document Editor

## Assessment

AJAIA AI Implementation Manager / Project Manager Assessment

## Project Summary

DocLite is a lightweight collaborative document editor inspired by Google Docs. The goal was to build a focused working MVP that demonstrates document creation, editing, file upload, sharing, persistence, and clear product tradeoffs.

The app uses seeded users instead of full authentication so reviewers can quickly test the sharing workflow.

## Live Product URL

`<add your deployed frontend URL here>`

## Backend API URL

`<add your deployed backend URL here>`

## Walkthrough Video

`<add your Loom, YouTube, or Google Drive video URL here>`

## Source Code

Included in this submission folder.

## Seeded Users

The app uses seeded users to simulate login:

- Alice Morgan
- Ben Carter
- Priya Shah

Use the user dropdown in the app to switch between users.

## What Is Included

This submission includes:

- React frontend
- FastAPI backend
- SQLite database persistence
- Source code
- README.md
- ARCHITECTURE.md
- AI_WORKFLOW.md
- SUBMISSION.md
- Automated backend test
- Walkthrough video URL
- Screenshots, if needed

## What Works

The following features are working:

- Create a new document
- Rename a document
- Edit document content in the browser
- Apply basic formatting:
  - Bold
  - Italic
  - Underline
  - Heading
  - Bulleted list
  - Numbered list
- Save and reopen documents
- Persist documents after refresh
- Upload `.txt` and `.md` files as editable documents
- Share a document with another seeded user
- View documents under:
  - My Documents
  - Shared With Me
  - Shared By Me
- Basic validation and error handling
- One automated backend test using Pytest

## Supported File Types

This MVP supports:

- `.txt`
- `.md`

Other file types such as `.docx`, `.pdf`, and images were intentionally deprioritized.

## Automated Test

One backend automated test is included.

The test verifies that:

1. A document can be created.
2. The document can be shared with another user.
3. The shared document appears in the receiving user's shared document list.

Test result:

```text
1 passed


Incomplete / Intentionally Deprioritized

The following features were intentionally not included in this MVP:

Real authentication
Password-based login
Real-time multi-user collaboration
Collaboration cursors
Comments
Suggestion mode
Document version history
DOCX upload
PDF export
Advanced role-based permissions

These features were deprioritized to keep the product focused on the core document workflow within the assessment timebox.

What I Would Build Next With Another 2–4 Hours

With more time, I would add:

Viewer/editor permission levels
Document version history
Commenting
Real-time collaboration indicators
Better rich-text editor controls
More automated frontend and backend tests
Production-ready database support such as Postgres
Real authentication
Product Judgment Note

I prioritized the core product loop over optional complexity:

Create
Edit
Save
Reopen
Upload
Share

=======
# Submission

## Project Name

DocLite – Lightweight Collaborative Document Editor

## Assessment

AJAIA AI Implementation Manager / Project Manager Assessment

## Project Summary

DocLite is a lightweight collaborative document editor inspired by Google Docs. The goal was to build a focused working MVP that demonstrates document creation, editing, file upload, sharing, persistence, and clear product tradeoffs.

The app uses seeded users instead of full authentication so reviewers can quickly test the sharing workflow.

## Live Product URL

`<add your deployed frontend URL here>`

## Backend API URL

`<add your deployed backend URL here>`

## Walkthrough Video

`<add your Loom, YouTube, or Google Drive video URL here>`

## Source Code

Included in this submission folder.

## Seeded Users

The app uses seeded users to simulate login:

- Alice Morgan
- Ben Carter
- Priya Shah

Use the user dropdown in the app to switch between users.

## What Is Included

This submission includes:

- React frontend
- FastAPI backend
- SQLite database persistence
- Source code
- README.md
- ARCHITECTURE.md
- AI_WORKFLOW.md
- SUBMISSION.md
- Automated backend test
- Walkthrough video URL
- Screenshots, if needed

## What Works

The following features are working:

- Create a new document
- Rename a document
- Edit document content in the browser
- Apply basic formatting:
  - Bold
  - Italic
  - Underline
  - Heading
  - Bulleted list
  - Numbered list
- Save and reopen documents
- Persist documents after refresh
- Upload `.txt` and `.md` files as editable documents
- Share a document with another seeded user
- View documents under:
  - My Documents
  - Shared With Me
  - Shared By Me
- Basic validation and error handling
- One automated backend test using Pytest

## Supported File Types

This MVP supports:

- `.txt`
- `.md`

Other file types such as `.docx`, `.pdf`, and images were intentionally deprioritized.

## Automated Test

One backend automated test is included.

The test verifies that:

1. A document can be created.
2. The document can be shared with another user.
3. The shared document appears in the receiving user's shared document list.

Test result:

```text
1 passed


Incomplete / Intentionally Deprioritized

The following features were intentionally not included in this MVP:

Real authentication
Password-based login
Real-time multi-user collaboration
Collaboration cursors
Comments
Suggestion mode
Document version history
DOCX upload
PDF export
Advanced role-based permissions

These features were deprioritized to keep the product focused on the core document workflow within the assessment timebox.

What I Would Build Next With Another 2–4 Hours

With more time, I would add:

Viewer/editor permission levels
Document version history
Commenting
Real-time collaboration indicators
Better rich-text editor controls
More automated frontend and backend tests
Production-ready database support such as Postgres
Real authentication
Product Judgment Note

I prioritized the core product loop over optional complexity:

Create
Edit
Save
Reopen
Upload
Share

>>>>>>> 37e21760ae63c1531bb307cd25709b73c6fe789e
This allowed the app to demonstrate a complete working flow while keeping the implementation understandable and reviewable.

Live Product URL: your Vercel frontend URL
Backend API URL: your Render backend URL