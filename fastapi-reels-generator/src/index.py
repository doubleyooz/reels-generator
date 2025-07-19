import cv2
import numpy as np
import subprocess
import os

def create_reel(video_path, image_path, audio_path, output_path, image_scale=0.5):
    try:
        print(f"Loading video from {video_path}...")
        # Load the video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError("Error opening video file")
        print("Video loaded successfully.")

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"Video properties: width={width}, height={height}, fps={fps}, frame_count={frame_count}")

        # Load the image (supporting transparency)
        print(f"Loading image from {image_path}...")
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise ValueError("Error loading image")
        print("Image loaded successfully.")

        # Resize image (scale relative to video width)
        img_height, img_width = image.shape[:2]
        new_width = int(width * image_scale)
        new_height = int(img_height * (new_width / img_width))
        image = cv2.resize(image, (new_width, new_height))
        print(f"Image resized to width={new_width}, height={new_height}")

        # Calculate position to center the image
        x_offset = (width - new_width) // 2
        y_offset = (height - new_height) // 2
        print(f"Image will be centered at x={x_offset}, y={y_offset}")

        # Prepare output video
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        temp_video = "temp_video.mp4"
        out = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))
        print("Output video initialized.")

        # Process each frame
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            print(f"Processing frame {frame_count}...")

            # If image has alpha channel (RGBA), handle transparency
            if image.shape[2] == 4:
                # Split image into color and alpha channels
                img_rgb = image[:, :, :3]
                alpha = image[:, :, 3] / 255.0

                # Create ROI (Region of Interest) in the frame
                roi = frame[y_offset:y_offset+new_height, x_offset:x_offset+new_width]

                # Blend image with background
                for c in range(3):
                    roi[:, :, c] = (alpha * img_rgb[:, :, c] + (1 - alpha) * roi[:, :, c]).astype(np.uint8)

                # Place blended ROI back into frame
                frame[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = roi
            else:
                # No transparency, directly overlay the image
                frame[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = image

            # Write frame to output video
            out.write(frame)

        # Release video objects
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print("Video processing complete.")

       
        # Add audio using FFmpeg
        print("Adding audio to output video...")
        ffmpeg_cmd = [
            "ffmpeg", "-i", temp_video, "-i", audio_path, "-c:v", "copy",
            "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output_path
        ]
        subprocess.run(ffmpeg_cmd, check=True)
        print("Audio added successfully.")

        # Clean up temporary video
        os.remove(temp_video)
        print("Temporary video removed.")

        print(f"Reel created successfully at {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
video_path = "background_video.mp4"
image_path = "center_image.png"
audio_path = "background_music.mp3"
output_path = "output_reel.mp4"

create_reel(video_path, image_path, audio_path, output_path, image_scale=0.5)