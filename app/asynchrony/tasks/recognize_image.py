import io
import cv2
import redis
import torch
import base64
import numpy as np
import logging
import logging.config


from PIL import Image
from torchvision import models, transforms
from celery import current_app

from config import REDIS_HOST, REDIS_PORT, LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("celery_log")

redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# === Модель и классы ===
class_names = ['Bacterial_spot', 'Early_blight', 'Late_blight', 'Leaf_Mold',
               'Septoria_leaf_spot', 'Spider_mites', 'Target_Spot',
               'Tomato_Yellow_Leaf_Curl_Virus', 'Tomato_mosaic_virus', 'healthy']

model = models.convnext_tiny(weights=None)
model.classifier[2] = torch.nn.Linear(model.classifier[2].in_features, len(class_names))
model.load_state_dict(torch.load("./models/convnext_tiny_tomato_best.pth", map_location="cpu"))
model.eval()

# === Преобразование ===
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# === Grad-CAM ===
class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None

        self.target_layer.register_forward_hook(self.save_activation)
        self.target_layer.register_full_backward_hook(self.save_gradient)

    def save_activation(self, module, input, output):
        self.activations = output.detach()

    def save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def __call__(self, x, class_idx=None):
        output = self.model(x)
        if class_idx is None:
            class_idx = output.argmax(dim=1).item()
        self.model.zero_grad()
        output[0, class_idx].backward()

        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * self.activations).sum(dim=1, keepdim=True)
        cam = torch.relu(cam).squeeze().numpy()
        cam = cv2.resize(cam, (224, 224))
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        return cam, class_idx

gradcam = GradCAM(model, model.features[-1])

@current_app.task
def recognize_image_task(image_base64: str) -> dict:
    logger.info("recognize_image started")
    try:
        # Декодирование изображения
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        input_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            outputs = model(input_tensor)
            probs = torch.nn.functional.softmax(outputs, dim=1)
            pred_idx = torch.argmax(probs, dim=1).item()

        cam, _ = gradcam(input_tensor, class_idx=pred_idx)
        orig = np.array(image.resize((224, 224)))
        heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
        overlay = np.uint8(0.5 * heatmap + 0.5 * orig)

        _, buffer = cv2.imencode(".jpg", overlay)
        overlay_b64 = base64.b64encode(buffer).decode("utf-8")

        result = {
            "class": class_names[pred_idx],
            "confidence": float(probs[0, pred_idx]),
            "heatmap_base64": overlay_b64
        }

        return result

    except Exception as e:
        logger.exception("Error in recognize_image_task")
        raise e

    finally:
        logger.info("recognize_image ended")
