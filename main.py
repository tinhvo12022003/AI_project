import streamlit as st
import cv2
import numpy as np
import sys
from ultralytics import YOLO
import classifier

# Lấy đường dẫn video từ dòng lện
# Load model

video_source = ("./videos/test.mp4")

model = YOLO("./models/best1.pt")

# Cấu hình giao diện Streamlit
st.set_page_config(layout="wide")
st.title("🍽️ Kitchen Monitoring Dashboard")

# Tạo columns cho layout
col1, col2 = st.columns(2)

# Tạo placeholders cho frame và stats
frame_placeholder = col1.empty()
stats_placeholder = col2.empty()

# Khu vực polygon xác định vùng theo dõi
points = np.array([
    [943, 57], [1152, 96], [1365, 148], [1346, 247], [1135, 206], [950, 163]
], dtype=np.int32)

# Hàm cập nhật thống kê
def update_stats_ui(dish_count, tray_count):
    stats_placeholder.markdown(f"""
    ### 📊 Statistics
    - 🥣 Dish:
        - Empty: `{dish_count['empty']}`
        - Not Empty: `{dish_count['not_empty']}`
        - Kakigori: `{dish_count['kakigori']}`
    - 📦 Tray:
        - Empty: `{tray_count['empty']}`
        - Not Empty: `{tray_count['not_empty']}`
        - Kakigori: `{tray_count['kakigori']}`
    """)

# Đọc video và xử lý
cap = cv2.VideoCapture(video_source)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    dish_count = {"empty": 0, "not_empty": 0, "kakigori": 0}
    tray_count = {"empty": 0, "not_empty": 0, "kakigori": 0}

    results = model.predict(frame, verbose=False)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            b = box.xyxy[0].cpu().numpy()
            xywh = box.xywh[0].cpu().numpy()
            x, y, w, h = xywh.astype(int)
            center_x, center_y = int(x), int(y)

            if cv2.pointPolygonTest(points, (float(center_x), float(center_y)), False) >= 0:
                crop = frame[y:y+h, x:x+w]
                cls_name = result.names[int(box.cls[0])]

                if cls_name == "dish":
                    label = classifier.predict_image_dish(crop)
                    dish_count[label] += 1
                elif cls_name == "tray":
                    label = classifier.predict_image_tray(crop)
                    tray_count[label] += 1
                else:
                    label = "unknown"

                cv2.rectangle(frame, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (89, 43, 32), 2)
                cv2.putText(frame, f"{cls_name}:{label}", (int(b[0]), int(b[1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Cập nhật UI
    update_stats_ui(dish_count, tray_count)
    cv2.polylines(frame, [points], isClosed=True, color=(0, 255, 0), thickness=4)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(frame_rgb, channels="RGB")

cap.release()

