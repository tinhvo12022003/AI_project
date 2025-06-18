# DEMO
Based on the requirements and the provided data, my initial idea was to build an application capable of tracking items in the kitchen space using the input video

The idea is to use the YOLOv12 model to detect objects labeled as 'tray' and 'dish', and then use a compact ResNet18 model to classify each object as 'empty', 'kakigori' or 'not_empty'.

Results are displayed using the streamlit tool.


First, analyze the provided dataset and perform training.

- The result on object detection is not effective, the reason is that the images are partially cropped, which makes it difficult for the model to detect multiple objects in long videos. Additionally, some objects are labeled inconsistently or have missing labels, further hindering the model's performance.

- For the classification dataset, the image quality is not high but it is still acceptable and can be trained and the results are relatively stable.

Solution: I manually labeled the data using the Roboflow platform to enhance the quality of the dataset. You can download from link https://app.roboflow.com/detection-ahsgp/traydish/4 .


## Step 1: 
The demo is deployed based on the provided video, but due to its large size, the video file named 1473_CH05_20250501133703_154216.mp4 will be renamed to test.mp4 and placed in the videos folder before deploying the project (Because as I understand I will predict on this actual video.)

## Step 2:
<pre>$ cd ./testYOLO</pre>

## Step 3: 
<pre>$ docker-compose up --build</pre>


## Step 4: 
Change the path 0.0.0.0:8501 to localhost:8501 (Sorry for the inconvenience)


# Further explanation
To save time, you can install the libraries from the requirements.txt file directly on your local environment instead of building the Docker image.


Both the predict and main files include prediction functionality; however, the main file predicts items only on the serving table (a specific ROI area), while the predict file detects all visible items in the frame.

Just change the video path in the beginning of the source code (simple)
