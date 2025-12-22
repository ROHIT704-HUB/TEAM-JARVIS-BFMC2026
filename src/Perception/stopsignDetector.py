Python
import torch
import cv2

class StopSignDetector:
    """
    YOLOv5-based Stop Sign Detector.
    Tested using laptop webcam during development.
    """

    def _init_(self, camera_index=0, confidence_threshold=0.5):
        print("[STOP SIGN] Loading YOLOv5 model...")
        self.model = torch.hub.load(
            'ultralytics/yolov5', 'yolov5s', pretrained=True
        )
        self.confidence_threshold = confidence_threshold
        self.cap = cv2.VideoCapture(camera_index)

    def detect(self):
        ret, frame = self.cap.read()
        if not ret:
            return False

        results = self.model(frame)
        detections = results.pandas().xyxy[0]

        for _, det in detections.iterrows():
            if det['name'] == "stop sign" and det['confidence'] > self.confidence_threshold:
                return True

        return False

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
