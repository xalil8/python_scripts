import numpy as np
import cv2
from controlled_laser import ControlledLaser

my_video = cv2.VideoCapture('video.mp4')
red_dot = ControlledLaser((1152, 640), (606, 638.5))


def find_green(img):
    ball_coordinates = [0, 0]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (29, 86, 6), (64, 255, 255))
    _, contour, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = sorted(contour, key=lambda t: cv2.contourArea(t), reverse=True)

    for cnt in contour:
        if cv2.contourArea(cnt) > 100:
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            ball_coordinates = x, y
            break
    return ball_coordinates


initial_coordinates = [606, 638.5]

while True:
    _, my_frame = my_video.read()

    if _:
        final_coordinates = find_green(my_frame)
        v_x = final_coordinates[0] - initial_coordinates[0]
        v_y = final_coordinates[1] - initial_coordinates[1]
        final_frame = red_dot.step(my_frame, (v_x, v_y))
        initial_coordinates = final_coordinates
        cv2.imshow('Laser Dot', final_frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    else:
        break


my_video.release()
cv2.destroyAllWindows()
