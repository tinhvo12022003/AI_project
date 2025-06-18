from torchvision import transforms
from PIL import Image
import torch
from torchvision import models
import torch.nn as nn
from collections import OrderedDict
import numpy as np

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model_dish = models.resnet18(weights=None)
model_dish.fc = nn.Linear(model_dish.fc.in_features, 3)
model_dish = model_dish.to(DEVICE)

state_dict1 = torch.load("./models/best_resnet_dish.pth", map_location="cpu")
new_state_dict1 = OrderedDict()
for k, v in state_dict1.items():
    name = k.replace("module.", "")  
    new_state_dict1[name] = v
model_dish.load_state_dict(new_state_dict1)

model_dish.eval()


model_tray = models.resnet18(weights=None)
model_tray.fc = nn.Linear(model_tray.fc.in_features, 3)
model_tray = model_tray.to(DEVICE)

state_dict2 = torch.load("./models/best_resnet_tray.pth", map_location="cpu")
new_state_dict2 = OrderedDict()
for k, v in state_dict2.items():
    name = k.replace("module.", "")  
    new_state_dict2[name] = v
model_tray.load_state_dict(new_state_dict2)

model_tray.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

labels = ['empty', 'kakigori', 'not_empty']

def predict_image_dish(frame):
    if isinstance(frame, np.ndarray):
        frame = Image.fromarray(frame)
    image = frame.convert("RGB")
    image = transform(image).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        output = model_dish(image)
        pred = torch.argmax(output, dim=1).item()
    return labels[pred]

def predict_image_tray(frame):
    if isinstance(frame, np.ndarray):
        frame = Image.fromarray(frame)
    image = frame.convert("RGB")
    image = transform(image).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        output = model_tray(image)
        pred = torch.argmax(output, dim=1).item()
    return labels[pred]
