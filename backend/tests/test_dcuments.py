from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_and_share_document():
    create_response = client.post(
        "/documents",
        json={
            "title": "Automated Test Document",
            "owner_id": 1,
        },
    )

    assert create_response.status_code == 200

    document = create_response.json()
    document_id = document["id"]

    share_response = client.post(
        f"/documents/{document_id}/share",
        json={
            "owner_id": 1,
            "shared_with_user_id": 2,
        },
    )

    assert share_response.status_code == 200

    ben_docs_response = client.get("/documents?user_id=2")

    assert ben_docs_response.status_code == 200

    ben_docs = ben_docs_response.json()

    assert any(doc["id"] == document_id for doc in ben_docs["shared"])