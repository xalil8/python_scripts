import time
import cv2
import numpy as np

class PolygonDrawer:
    def __init__(self):
        self.polygons = [[]]  # A list of polygons, where each polygon is a list of points

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Left click - add point to the current polygon
            print(f"[{x}, {y}] added to the current polygon")
            self.polygons[-1].append([x, y])
            print(f"Current polygon: {self.polygons[-1]}")
        elif event == cv2.EVENT_RBUTTONDOWN:
            # Right click - finish the current polygon and start a new one
            if len(self.polygons[-1]) >= 3:  # Only finish if the polygon has at least 3 points
                print(f"Finished polygon: {self.polygons[-1]}")
                self.polygons.append([])
                print(f"Started a new polygon")

    def main(self):
        cap = cv2.VideoCapture("source")
        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (1280, 720))

                for i, polygon in enumerate(self.polygons):
                    if len(polygon) > 1:
                        pts = np.array(polygon, np.int32)
                        pts = pts.reshape((-1, 1, 2))
                        is_closed = len(polygon) >= 3  # Close if there are at least 3 points
                        color = (255, 0, 0)
                        thickness = 2

                        cv2.polylines(frame, [pts], is_closed, color, thickness)

                        # If the polygon is closed, write its index at its centroid
                        if is_closed:
                            centroid = np.mean(pts, axis=0)
                            centroid = (int(centroid[0][0]), int(centroid[0][1]))  # Convert to integer
                            cv2.putText(frame, f"Polygon {i+1}", centroid, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.namedWindow("img", flags=cv2.WINDOW_AUTOSIZE)
                cv2.imshow("img", frame)
                cv2.setMouseCallback("img", self.mouse_callback)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()
        print(f"Took {time.time() - start_time} Sec")
        print("Final Polygon List:")
        for i, polygon in enumerate(self.polygons):
            if polygon:  # Only print non-empty polygons
                print(f"Polygon {i+1}: {polygon}")


if __name__ == "__main__":
    pd = PolygonDrawer()
    pd.main()

