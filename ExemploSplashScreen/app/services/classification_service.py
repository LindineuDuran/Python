
import cv2, numpy as np

class ClassificationService:
    def classify(self, path):
        img = cv2.imread(path, 0)
        edges = cv2.Canny(img,50,150)
        density = edges.sum()/edges.size
        if density>0.2: return "grafico"
        if density>0.05: return "foto"
        return "texto"
