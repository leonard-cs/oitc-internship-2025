# python -m pytest

from app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    # Test the root endpoint
    response = client.get("/")
    assert response.status_code == 200


def test_embed_image():
    # Test the `/embed_image/` endpoint to ensure embedding generation
    with open("llm_server/test_data/sample.jpg", "rb") as image_file:
        response = client.post(
            "/embed_image/",
            files={"file": ("sample.jpg", image_file, "image/jpeg")},
        )

    assert response.status_code == 200
    data = response.json()
    assert "embedding" in data
    assert isinstance(data["embedding"], list)
    assert len(data["embedding"]) > 0


# def test_store_image(mock_image):
#     # Test the `/store_image/` endpoint to store image embeddings
#     response = client.post(
#         "/store_image/",
#         files={"file": ("test_image.jpg", mock_image, "image/jpeg")},
#     )
#     assert response.status_code == 200
#     assert "message" in response.json()
#     assert "Stored image embedding with id" in response.json()["message"]


# def test_search_similar_images(mock_image):
#     # Test the `/search_similar/` endpoint to search similar images
#     response = client.post(
#         "/search_similar/",
#         files={"file": ("test_image.jpg", mock_image, "image/jpeg")},
#     )
#     assert response.status_code == 200
#     assert "results" in response.json()
#     # Optionally, check if results contain 'id' and 'score'
#     if response.json()["results"]:
#         assert "id" in response.json()["results"][0]
#         assert "score" in response.json()["results"][0]


# def test_get_embedding(mock_image):
#     # Test the `/get_embedding/{point_id}` endpoint to retrieve stored embeddings
#     # We need to first store an image to get a valid point_id for the test
#     store_response = client.post(
#         "/store_image/",
#         files={"file": ("test_image.jpg", mock_image, "image/jpeg")},
#     )
#     point_id = store_response.json()["message"].split("id ")[1]

#     # Now test getting the embedding by point_id
#     response = client.get(f"/get_embedding/{point_id}")
#     assert response.status_code == 200
#     assert "embedding" in response.json()
