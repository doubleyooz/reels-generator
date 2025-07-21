import cv2
import numpy as np
import subprocess
import os

def create_reel(video_path, image_paths, audio_path, output_path, image_scale=0.5):
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

        # Validate number of images
        num_images = len(image_paths)
        if num_images not in [1, 2, 3]:
            raise ValueError(f"Expected 1, 2, or 3 images, got {num_images}")

        # Load and resize images
        images = []
        positions = []
        for i, image_path in enumerate(image_paths):
            print(f"Loading image {i+1} from {image_path}...")
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            if image is None:
                raise ValueError(f"Error loading image {image_path}")
            print(f"Image {i+1} loaded successfully.")

            # Resize image (scale relative to video width)
            img_height, img_width = image.shape[:2]
            new_width = int(width * image_scale)
            new_height = int(img_height * (new_width / img_width))
            image = cv2.resize(image, (new_width, new_height))
            images.append(image)
            print(f"Image {i+1} resized to width={new_width}, height={new_height}")

        # Calculate positions based on number of images
        if num_images == 1:
            # Single image: Center
            x_offset = (width - images[0].shape[1]) // 2
            y_offset = (height - images[0].shape[0]) // 2
            positions.append((x_offset, y_offset))

        elif num_images == 2:
            # Two images: Center-top and center-bottom
            img_width, img_height = images[0].shape[1], images[0].shape[0]
            # Center-top (10% from top)
            x_offset_top = (width - img_width) // 2
            y_offset_top = int(height * 0.1)
            # Center-bottom (10% from bottom)
            x_offset_bottom = (width - img_width) // 2
            y_offset_bottom = height - img_height - int(height * 0.1)
            positions = [(x_offset_top, y_offset_top), (x_offset_bottom, y_offset_bottom)]

        elif num_images == 3:
            # Three images: Center-top, two at center-bottom (evenly spaced)
            img_width, img_height = images[0].shape[1], images[0].shape[0]
            # Center-top (10% from top)
            x_offset_top = (width - img_width) // 2
            y_offset_top = int(height * 0.1)
            # Two images at center-bottom (10% from bottom, evenly spaced)
            spacing = img_width // 2  # Space between bottom images
            x_offset_bottom1 = (width - 2 * img_width - spacing) // 2
            x_offset_bottom2 = x_offset_bottom1 + img_width + spacing
            y_offset_bottom = height - img_height - int(height * 0.1)
            positions = [(x_offset_top, y_offset_top), (x_offset_bottom1, y_offset_bottom), (x_offset_bottom2, y_offset_bottom)]

        # Print positions for debugging
        for i, (x, y) in enumerate(positions):
            print(f"Image {i+1} will be placed at x={x}, y={y}")

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

            # Overlay each image
            for img, (x_offset, y_offset) in zip(images, positions):
                img_height, img_width = img.shape[:2]
                # Ensure the image fits within the frame
                if x_offset < 0 or y_offset < 0 or x_offset + img_width > width or y_offset + img_height > height:
                    print(f"Warning: Image at ({x_offset}, {y_offset}) exceeds frame boundaries")
                    continue

                # If image has alpha channel (RGBA), handle transparency
                if img.shape[2] == 4:
                    img_rgb = img[:, :, :3]
                    alpha = img[:, :, 3] / 255.0
                    roi = frame[y_offset:y_offset+img_height, x_offset:x_offset+img_width]
                    for c in range(3):
                        roi[:, :, c] = (alpha * img_rgb[:, :, c] + (1 - alpha) * roi[:, :, c]).astype(np.uint8)
                    frame[y_offset:y_offset+img_height, x_offset:x_offset+img_width] = roi
                else:
                    frame[y_offset:y_offset+img_height, x_offset:x_offset+img_width] = img

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

# Example usage for each setup
if __name__ == "__main__":
    video_path = "background_video.mp4"
    audio_path = "background_music.mp3"
    
    # Single image (center)
    image_paths = ["img1.png"]
    create_reel(video_path, image_paths, audio_path, "output_reel_single.mp4", image_scale=0.5)
    
    # Two images (center-top, center-bottom)
    image_paths = ["img1.png", "img2.png"]
    create_reel(video_path, image_paths, audio_path, "output_reel_two.mp4", image_scale=0.3)
    
    # Three images (center-top, two at center-bottom)
    image_paths = ["img1.png", "img2.png", "img3.png"]
    create_reel(video_path, image_paths, audio_path, "output_reel_three.mp4", image_scale=0.3)