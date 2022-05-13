import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision.models.detection import fasterrcnn_mobilenet_v3_large_320_fpn

from config import COCO_LABELS, THRESHOLD


class Detector:
    def __init__(
        self,
        detection_model=fasterrcnn_mobilenet_v3_large_320_fpn,
        labels=COCO_LABELS,
        threshold=THRESHOLD,
        bbox_tol=10,
    ):
        self.model = detection_model(pretrained=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.eval().to(self.device)
        self.threshold = threshold
        self.labels = labels
        self.bbox_tol = bbox_tol

    def filter_bbox(self, box, bboxes):
        for b in bboxes:
            close_vertexes = [abs(box[i] - b[i]) <= self.bbox_tol for i in range(4)]
            if all(close_vertexes):
                return False
        return True

    def predict(self, image, filter_classes=None):
        # transform the image to tensor
        transf = transforms.ToTensor()
        image = transf(image).to(self.device)
        image = image.unsqueeze(0)  # add a batch dimension
        with torch.no_grad():
            outputs = self.model(image)  # get the predictions on the image

        # get bbox and labels
        boxes, labels = [], []
        for box, label, score in zip(
            outputs[0]["boxes"], outputs[0]["labels"], outputs[0]["scores"]
        ):
            if score > self.threshold and (filter_classes is None or label in filter_classes):
                bbox = box.detach().cpu().numpy().astype(np.int32)
                if self.bbox_tol is None or self.filter_bbox(bbox, boxes):
                    boxes.append(bbox)
                    labels.append(self.labels[label.cpu().numpy()])

        return boxes, labels
