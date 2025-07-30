import os

import open_clip
import torch

os.makedirs("weights", exist_ok=True)
model, _, _ = open_clip.create_model_and_transforms("ViT-B-32", pretrained="openai")
torch.save(model.state_dict(), "weights/ViT-B-32.pt")
