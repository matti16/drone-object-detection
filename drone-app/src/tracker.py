import math

MAX_DIST = 80
PATIENCE = 10

class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        self.center_ages = {}

    def create_new_id(self):
        cur_max = max(list(self.center_points.keys()) + [0])
        for i in range(1, cur_max):
            if i not in self.center_points:
                return i
        return cur_max + 1

    def update(self, objects_rect):
        # Objects boxes and ids
        bboxes,  ids = [], []

        # Get center point of new object
        for i, rect in enumerate(objects_rect):
            x1, y1, x2, y2 = rect
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                if dist <= MAX_DIST and id not in ids:
                    new_id = id
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                new_id = self.create_new_id()

            self.center_points[new_id] = (cx, cy)
            self.center_ages[new_id] = 0
            bboxes.append(rect)
            ids.append(new_id)
            

        # Add all centers present now
        new_center_points = {}
        for object_id in ids:
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return bboxes, ids



