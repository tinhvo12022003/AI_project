# DEMO
Based on the requirements and the provided data, my initial idea was to build an application capable of tracking items in the kitchen space using the input video

The idea is to use the YOLOv12 model to detect objects labeled as 'tray' and 'dish', and then use a compact ResNet18 model to classify each object as 'empty', 'kakigori' or 'not_empty'.

Results are displayed using the streamlit tool.


First, analyze the provided dataset and perform training.

- The result on object detection is not effective, the reason is that the images are partially cropped, which makes it difficult for the model to detect multiple objects in long videos. Additionally, some objects are labeled inconsistently or have missing labels, further hindering the model's performance.

- For the classification dataset, the image quality is not high but it is still acceptable and can be trained and the results are relatively stable.

Solution: I manually labeled the data using the Roboflow platform to enhance the quality of the dataset. You can download from link https://app.roboflow.com/detection-ahsgp/traydish/4 .


## Step 1: 
<pre>$ git clone https://github.com/tinhvo12022003/AI_projec</pre>
<pre>$ cd AI_project</pre>

## Step 2:

The demo is deployed based on the provided video, but due to its large size, the video file named 1473_CH05_20250501133703_154216.mp4 will be renamed to test.mp4 and placed in the videos folder before deploying the project (Because as I understand I will predict on this actual video)

## Step 3: 
<pre>$ docker-compose up --build</pre>


## Step 4: 
Change the path 0.0.0.0:8501 to localhost:8501 (Sorry for the inconvenience)


# Further explanation
To save time, you can install the libraries from the requirements.txt file directly on your local environment instead of building the Docker image.


Both the predict and main files include prediction functionality; however, the main file predicts items only on the serving table (a specific ROI area), while the predict file detects all visible items in the frame.

Just change the video path in the beginning of the source code (simple)


If you want to save time and view the results directly, you can access them on Google Drive using the following link: https://drive.google.com/drive/u/0/folders/1dX3sdgiI4N7RKUhOR8E-2J67dW8HsxAY


# Conclusion
This project has been truly practical and has helped me gain a deeper understanding of business operations. It made me realize how essential AI is and how much it can support businesses. I sincerely thank you for the time we spent working together—even though it was brief, I truly appreciate it. 

Regardless of the outcome, I look forward to receiving your feedback to further improve this project!

