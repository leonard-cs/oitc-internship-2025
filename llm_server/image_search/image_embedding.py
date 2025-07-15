# image_embedding.py

import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

class ImageEmbedder:
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        self.model = CLIPModel.from_pretrained(model_name)
        self.processor = CLIPProcessor.from_pretrained(model_name)

    def embed_image(self, image_path: str):
        image = Image.open(image_path)

        # Preprocess the image
        inputs = self.processor(images=image, return_tensors="pt", padding=True)

        # Get the embeddings
        with torch.no_grad():
            features = self.model.get_image_features(**inputs)

        normalized_features = features / features.norm(p=2, dim=-1, keepdim=True)

        # Convert tensor to numpy array
        return normalized_features.cpu().numpy()

if __name__ == "__main__":
    image_path = r"C:\Users\35521\Pictures\aventador.jpg"
    embedder = ImageEmbedder()
    vector = embedder.embed_image(image_path)
    print(vector)