import cv2
import numpy as np
import os
from tqdm import tqdm
import argparse

def pixelate(image, mask, pixelation_level=15):
    """Apply pixelation effect to areas where mask is 255 (white)"""
    # Get dimensions
    height, width = image.shape[:2]
    
    # Create a small version of the image (pixelated)
    small = cv2.resize(image, (width // pixelation_level, height // pixelation_level),
                       interpolation=cv2.INTER_LINEAR)
    
    # Scale it back up to original size (now pixelated)
    pixelated = cv2.resize(small, (width, height), interpolation=cv2.INTER_NEAREST)
    
    # Convert mask to 3 channels if needed
    if len(mask.shape) == 2:
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    # Apply mask: original image where mask is 0, pixelated where mask is 255
    return np.where(mask == 255, pixelated, image)

def process_video_with_face_detection(input_file, output_file=None, pixelation_level=15, 
                                     detection_method='face', confidence_threshold=0.5):
    """
    Process video for face/head detection and selective pixelation
    
    Parameters:
    -----------
    input_file : str
        Path to input video file
    output_file : str
        Path to output video file (defaults to 'output_' + input_file)
    pixelation_level : int
        Level of pixelation (higher = more pixelated)
    detection_method : str
        'face' for traditional Haar cascade face detection
        'dnn' for deep neural network-based face detection
        'head' for more general head detection
    confidence_threshold : float
        Threshold for DNN-based detection (0-1)
    """
    # Default output filename if not provided
    if output_file is None:
        filename, ext = os.path.splitext(input_file)
        output_file = f"{filename}_pixelated{ext}"
    
    # Open input video
    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print(f"Error opening video file {input_file}")
        return False
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Initialize detector based on method
    if detection_method == 'face':
        # Haar cascade for frontal face detection
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    elif detection_method == 'dnn':
        # Load DNN model for face detection (more robust)
        model_file = "res10_300x300_ssd_iter_140000.caffemodel"
        config_file = "deploy.prototxt"
        # Check if model exists, if not inform user to download it
        if not (os.path.isfile(model_file) and os.path.isfile(config_file)):
            print(f"DNN model files not found. Please download:")
            print(f"1. {model_file}")
            print(f"2. {config_file}")
            print("From: https://github.com/opencv/opencv/tree/master/samples/dnn/face_detector")
            return False
        detector = cv2.dnn.readNetFromCaffe(config_file, model_file)
        
    elif detection_method == 'head':
        # Upper body detection (includes head)
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'XVID' for AVI
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    try:
        # Process frames with progress bar
        for _ in tqdm(range(total_frames), desc="Processing video"):
            ret, frame = cap.read()
            if not ret:
                break
                
            # Create mask (black background)
            mask = np.zeros((height, width), dtype=np.uint8)
            
            if detection_method == 'dnn':
                # DNN-based detection (more robust)
                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                           (300, 300), (104.0, 177.0, 123.0))
                detector.setInput(blob)
                detections = detector.forward()
                
                # Process each detection
                for i in range(detections.shape[2]):
                    confidence = detections[0, 0, i, 2]
                    if confidence > confidence_threshold:
                        box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                        (x1, y1, x2, y2) = box.astype("int")
                        cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)  # Fill rectangle with white
                
            else:  # 'face' or 'head' using Haar cascades
                # Convert to grayscale for detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces/upper bodies
                if detection_method == 'face':
                    detections = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, 
                                                       minSize=(30, 30))
                else:  # 'head' (upper body)
                    detections = detector.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, 
                                                       minSize=(50, 100))
                
                # Draw detected areas on mask (white)
                for (x, y, w, h) in detections:
                    cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)  # Fill rectangle with white
            
            # Invert mask to pixelate everything except faces/heads
            inverted_mask = cv2.bitwise_not(mask)
            
            # Apply pixelation
            result = pixelate(frame, inverted_mask, pixelation_level)
            
            # Write frame to output video
            out.write(result)
            
        print(f"Processing complete! Output saved to {output_file}")
        return True
    
    finally:
        # Release resources
        cap.release()
        out.release()

def main():
    parser = argparse.ArgumentParser(description='Pixelate background while keeping faces clear')
    parser.add_argument('--input', '-i', type=str, help='Input video file path')
    parser.add_argument('--output', '-o', type=str, help='Output video file path')
    parser.add_argument('--pixelation', '-p', type=int, default=15, 
                       help='Pixelation level (higher = more pixelated)')
    parser.add_argument('--method', '-m', type=str, default='face', 
                       choices=['face', 'dnn', 'head'],
                       help='Detection method: face (basic), dnn (robust), head (for profile/back views)')
    parser.add_argument('--threshold', '-t', type=float, default=0.5,
                       help='Confidence threshold for DNN detection (0-1)')
    
    args = parser.parse_args()
    
    # If no input file specified via arguments, ask user
    input_file = args.input
    if input_file is None:
        input_file = input("Enter the path to your video file: ")
    
    # Process the video
    process_video_with_face_detection(
        input_file=input_file,
        output_file=args.output,
        pixelation_level=args.pixelation,
        detection_method=args.method,
        confidence_threshold=args.threshold
    )

if __name__ == "__main__":
    main()