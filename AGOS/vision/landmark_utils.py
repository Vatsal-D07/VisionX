import math
import numpy as np

class LandmarkUtils:
    @staticmethod
    def calculate_distance(p1, p2):
        """
        Calculate Euclidean distance between two normalized 2D points (x, y).
        p1, p2: (x, y) tuples or objects with x, y attributes.
        """
        # Handle MediaPipe NormalizedLandmark objects which have x, y attributes
        x1, y1 = (p1.x, p1.y) if hasattr(p1, 'x') else p1
        x2, y2 = (p2.x, p2.y) if hasattr(p2, 'x') else p2
        
        return math.hypot(x2 - x1, y2 - y1)

    @staticmethod
    def get_coords(landmark, width, height):
        """
        Convert normalized landmark to pixel coordinates.
        """
        return int(landmark.x * width), int(landmark.y * height)
