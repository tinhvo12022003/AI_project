import pandas as pd
import os

BASE_DIR = "Classification/tray"

list_type = os.listdir(BASE_DIR)  # Ví dụ: ["type1", "type2"]
list_class = ["empty", "kakigori", "not_empty"]

data = []


for class_name in list_class:
    folder_path = os.path.join(BASE_DIR, class_name)
        
    if not os.path.isdir(folder_path):
        continue  # Bỏ qua nếu không phải thư mục

    list_images = os.listdir(folder_path)
        
    for image_file in list_images:
        image_path = os.path.join(folder_path, image_file)
            
            # Thêm vào danh sách
        data.append({
                "label": class_name,
                "image_path": image_path
        })

df = pd.DataFrame(data)

print(df.head())

df.to_csv("tray_data.csv", index=False)

