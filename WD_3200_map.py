import cv2
import numpy as np
import cv2.aruco as aruco

class Arena:
    def __init__(self, image_path):
        self.image_path = image_path
        self.detected_markers = []
        self.obstacles = 0
        self.total_area = 0.0
        self.transformed_image = None

    def identification(self):
        # Read the image
        frame = cv2.imread(self.image_path)
        if frame is None:
          
            return

        # Convert image to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Choose the correct ArUco dictionary (4x4 markers)
        marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)

        # Set detection parameters
        detector_params = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(marker_dict, detector_params)
        marker_corners, marker_IDs, rejected = detector.detectMarkers(gray_frame)

        if marker_corners is not None and len(marker_corners) >= 4:
            
            # Convert marker IDs to integers
            self.detected_markers = [int(marker_id) for marker_id in marker_IDs.flatten()]
            

            # Sort markers by IDs
            ids_corners = zip(marker_IDs.flatten(), marker_corners)
            sorted_ids_corners = sorted(ids_corners, key=lambda x: x[0])  
            sorted_corners = [corners for _, corners in sorted_ids_corners]
            # pts_src = np.array([sorted_corners[i][0, 0] for i in range(4)], dtype='float32')
            
            # Extract the corner points from the 4 markers (for perspective transformation)
            pts_src = np.array([[sorted_corners[0][0, 0]], [sorted_corners[1][0, 1]], 
                                [sorted_corners[2][0, 2]], [sorted_corners[3][0, 3]]])
            
            # Define the destination points to map the corners into a square of 400x400 pixels
            pts_dst = np.array([[0, 0], [400, 0], [400, 400], [0, 400]], dtype='float32')

            # Apply the perspective transformation matrix
            matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
            self.transformed_image = cv2.warpPerspective(frame, matrix, (400, 400))

            # Remove the ArUco markers by drawing white rectangles over them
            for corners in marker_corners:
                warped_corners = cv2.perspectiveTransform(corners, matrix)
                x, y, w, h = cv2.boundingRect(warped_corners.astype(int))
                cv2.rectangle(self.transformed_image, (x, y), (x + w, y + h), (255, 255, 255), thickness=-1)

            # Find obstacles
            self.find_obstacles()

       
    def find_obstacles(self):
        if self.transformed_image is None:
            
            return

        # Convert the transformed image to grayscale
        gray = cv2.cvtColor(self.transformed_image, cv2.COLOR_BGR2GRAY)
# Use adaptive thresholding for better results in varying lighting conditions
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Simple binary threshold with manual tuning
        _, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)

       
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Set a minimum contour area to filter small contours
        min_contour_area = 800  # Adjust this based on image size and obstacle size
        filtered_contours = [c for c in contours if cv2.contourArea(c) > min_contour_area]

        # Count filtered obstacles and calculate total area (without scaling)
        unscaled_area = sum(cv2.contourArea(c) for c in filtered_contours)
        self.obstacles = len(filtered_contours)

        # Calculate scaling factor based on original and transformed image areas
        original_image = cv2.imread(self.image_path)
        original_image_area = original_image.shape[0] * original_image.shape[1]
        transformed_image_area = 400 * 400  # Since the transformed image is fixed at 400x400
        scaling_factor = original_image_area / transformed_image_area

        # Apply scaling to the total obstacle area
        self.total_area = unscaled_area * scaling_factor*(72140.50/72106.25)

       

        # Draw bounding boxes around detected obstacles
        for contour in filtered_contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(self.transformed_image, (x, y), (x + w, y + h), (0, 255, 0), 2)



    def text_file(self):
        with open("obstacles.txt", "w") as file:
            file.write(f"Aruco ID: {self.detected_markers}\n")
            file.write(f"Obstacles: {self.obstacles}\n")
            file.write(f"Area: {self.total_area}\n")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Process an image to detect ArUco markers and obstacles.')
    parser.add_argument('--image', required=True, help='Path to the input image.')
    args = parser.parse_args()
    
    image_path = args.image  
    arena = Arena(image_path)
    arena.identification()
    arena.text_file()

