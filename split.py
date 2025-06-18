import cv2
import os

def split_video(input_path, output_dir, segment_length=30):
    """Splits a video into smaller segments, ensuring compatibility.

    Args:
        input_path (str): Path to the input video file.
        output_dir (str): Path to the directory to store the output segments.
        segment_length (int): Length of each segment in seconds.
    """

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the input video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file: {input_path}")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the number of frames per segment
    frames_per_segment = int(fps * segment_length)

    # Initialize variables for segmenting
    segment_number = 0
    frame_number = 0
    out = None

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # If there are no more frames, break the loop
        if not ret:
            break

        # If it's the first frame of a new segment, create a new output video
        if frame_number % frames_per_segment == 0:
            # Release the previous video if it exists
            if out is not None:
                out.release()

            # Create the output video path
            output_path = os.path.join(output_dir, f"segment_{segment_number}.mp4")

            # Create the output video writer, force H.264 compatibility
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use MP4 format, H.264 codec
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            # Increment the segment number
            segment_number += 1

        # Write the frame to the output video
        out.write(frame)

        # Increment the frame number
        frame_number += 1

    # Release the last video and the input video
    if out is not None:
        out.release()
    cap.release()

    print(f"Video split into {segment_number} segments in {output_dir}")


if __name__ == "__main__":
    input_video = "test.mp4"  # Replace with your video file
    output_directory = "output_segments"  # Replace with your desired output directory
    segment_size = 30  # Segment length in seconds

    split_video(input_video, output_directory, segment_size)