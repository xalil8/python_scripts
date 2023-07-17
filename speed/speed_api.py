import os
import torch
import cv2
import math
import numpy as np
from ssl import _create_unverified_context
from time import time
from trackers.multi_tracker_zoo import create_tracker
from collections import defaultdict, deque
from scipy.spatial import distance
import telegram


class SpeedTracker:
    def __init__(self, bot_token, chat_id, source_video_path, video_saving_path, model_path, polygon_points, writer,speed_limit, tracker,max_frame=13):
        _create_default_https_context = _create_unverified_context
        self.writer = writer
        self.bot = telegram.Bot(token=bot_token)
        self.chat_id = chat_id
        self.source_video_path = source_video_path
        self.video_saving_path = video_saving_path
        self.model_path = model_path
        self.polygon_points = np.array(polygon_points)
        self.max_frame = max_frame
        self.speed_limit = speed_limit

        self.cars = defaultdict(lambda: {"positions": deque(maxlen=self.max_frame), "times": deque(maxlen=self.max_frame)})

        self.video_cap = cv2.VideoCapture(self.source_video_path)
        width = int(self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # fps = video_cap.get(cv2.CAP_PROP_FPS)
        width, height = int(self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if writer:
            self.result = cv2.VideoWriter(video_saving_path, cv2.VideoWriter_fourcc(*'mp4v'), 16, (width, height))
        
        #CAR DETECTION MODEL 
        self.model = torch.hub.load("ultralytics/yolov5", "custom", path=self.model_path, force_reload=False,device="mps")
        self.names = self.model.names

        # TRACKER
        self.tracker_name = tracker
        self.tracker_list = create_tracker(f'{self.tracker_name}', f"trackers/{self.tracker_name}/configs/{self.tracker_name}.yaml","weights/osnet_x0_25_msmt17.pt", device=torch.device("mps"), half=False)


    def reconnect_video(self, video_cap):
        video_cap.release()
        video_cap = cv2.VideoCapture(self.source_video_path)
        return video_cap

    def process(self):
        count = 0
        #temp_sum = 0
        counter = 0
        prev_time = time()  # Add this line to initialize prev_time
        while self.video_cap.isOpened():
            try:
                ret, frame = self.video_cap.read()  # Update variable name to self.video_cap
                if not ret:
                    raise Exception("Error reading frame")
                count += 1
                if count % 2 != 0:
                    continue

                if counter == 0:
                    counter += 1
                    sum1 = sum(cv2.sumElems(frame))
                    temp_sum = sum1
                    continue

                sum1 = sum(cv2.sumElems(frame))
                diff = abs(sum1 - temp_sum)
                temp_sum = sum1
                ratio = diff / (1920 * 1080)

                if ratio > 45:
                    print("%%%%%%%%%%%%BAD FRAME DETECTED %%%%%%%%%%%%")
                    try:
                        continue
                    except Exception as e:
                        print("Error occurred while saving frame:", e)

                curr_time = time()
                elapsed_time = curr_time - prev_time
                prev_time = curr_time

                fps = 1.0 / elapsed_time
                cv2.putText(frame, f"FPS: {int(fps)}", (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 229, 204), 3)

                results = self.model(frame)
                det = results.xyxy[0]

                cv2.polylines(frame, np.int32([self.polygon_points]), True, (55, 155, 255), 3)

                if det is not None and len(det):
                    outputs = self.tracker_list.update(det.cpu(), frame)

                    for j, (output) in enumerate(outputs):
                        img_count = ""
                        bbox = output[0:4]
                        id = output[4]
                        cls = output[5]
                        conf = output[6]

                        x1, y1, x2, y2 = bbox
                        x1, y1, x2, y2, c, id = int(x1), int(y1), int(x2), int(y2), int(cls), int(id)

                        center_x, center_y = int(x1 + ((x2 - x1) / 2)), y2
                        area_check_1 = cv2.pointPolygonTest(np.int32([self.polygon_points]), ((center_x, center_y)),False)

                        img_count = f"{self.names[int(c)]}{str(id)}"

                        in_color = (50, 255, 50)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), in_color, 2)
                        cv2.circle(frame, (center_x, center_y), radius=3, color=in_color, thickness=-1)
                        cv2.putText(frame, f"{self.names[int(c)]}{str(id)}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,0.7, in_color, 2)

                        if area_check_1 == 1:
                            self.cars[id]["positions"].append((center_x, center_y))
                            self.cars[id]["times"].append(curr_time)

                            if len(self.cars[id]["positions"]) > 1:
                                pixel_distance = distance.euclidean(self.cars[id]["positions"][0],self.cars[id]["positions"][-1])
                                elapsed_time = self.cars[id]["times"][-1] - self.cars[id]["times"][0]
                                speed = abs(int(pixel_distance / elapsed_time if elapsed_time > 0 else 0))

                                cv2.putText(frame, f"SPEED = {str(speed)}", (x1 + 10, y2 + 15),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                                if speed>self.speed_limit:
                                    dosya_yolu = f"speed_limit/img{str(img_count)}.jpg"
                                    if os.path.exists(dosya_yolu):
                                        continue
                                    else:
                                        cv2.imwrite(dosya_yolu, frame)
                                        car_name = (str(self.names[int(c)]) + str(id)).capitalize()
                                    self.bot.send_photo(chat_id=self.chat_id, photo=open(dosya_yolu, 'rb'),caption="Hızlı Araç Geçişi")

                if not self.writer:
                    cv2.imshow("ROI", frame)

                if self.writer:
                    print(f"frame {count} writing")
                    cv2.imshow("ROI", frame)
                    self.result.write(frame)

                if cv2.waitKey(24) == ord('q'):
                    break
            except Exception as e:
                print(f"Error: {str(e)}")
                print("Reconnecting to video source...")
                self.video_cap = self.reconnect_video(self.video_cap)  # Update variable name to self.video_cap

if __name__ == "__main__":
    tracker = "bytetrack"
    speed_limit = 50
    writer = False

    bot_token = "telegram bot token"
    chat_id = "telegram chat id"
    source_video_path="rtsp://"
    video_saving_path = "try_except.mp4"
    model_path = "speed_v1.pt"
    polygon_points = [[714, 128], [714, 128], [1562, 127], [1562, 127], [1599, 196], [1599, 196], [692, 197],[692, 197]]
    tracker = SpeedTracker(bot_token, chat_id, source_video_path, video_saving_path, model_path, polygon_points,writer,speed_limit,tracker)
    tracker.process()
