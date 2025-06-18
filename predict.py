import cv2
from ultralytics import YOLO
import numpy as np
import classifier
from ultralytics.utils.plotting import Annotator, colors

source_video = "videos/clip_124.mp4"

cap = cv2.VideoCapture(source_video)
model = YOLO("./models/best1.pt")
names = model.names  # lấy tên lớp

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    annotator = Annotator(frame, line_width=2)
    results = model.predict(frame, verbose=False)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            b = box.xyxy[0].cpu().numpy()
            cls_id = int(box.cls[0])
            cls_name = names[cls_id]

            # Lấy tọa độ xywh để crop
            x, y, w, h = box.xywh[0].cpu().numpy().astype(int)
            x1 = max(x - w // 2, 0)
            y1 = max(y - h // 2, 0)
            x2 = min(x + w // 2, frame.shape[1])
            y2 = min(y + h // 2, frame.shape[0])
            crop = frame[y1:y2, x1:x2]

            if crop.size == 0:
                continue  # tránh lỗi nếu crop ngoài vùng ảnh

            if cls_name == "dish":
                label = classifier.predict_image_dish(crop)
            elif cls_name == "tray":
                label = classifier.predict_image_tray(crop)
            else:
                label = "unknown"

            annotator.box_label(b, f"{cls_name}: {label}", color=colors(cls_id, True))

    frame = annotator.result()
    frame = cv2.resize(frame, (800, 600))
    cv2.imshow("YOLO Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
