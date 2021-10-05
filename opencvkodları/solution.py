import cv2
from controlled_laser import ControlledLaser

green_lower = (29, 86, 6)  # lower value for green color
green_upper = (64, 255, 255)  # upper value for green color
my_video = cv2.VideoCapture('video.mp4')   # getting video
red_dot = ControlledLaser((1152, 640), (606, 633))  # creating laser instance
initial_coordinates = (606, 633)
# i took that point as an initial because of red ball first time show up in this location

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('output.mp4', fourcc, 33.0, (1152, 640))

def find_green(img):  # function which take image as a parameter then return center coordinates of ball
    ball_coordinates = [-1, -1]  # I give (-1,-1) as an initial value since frames can not get  negative values
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # change color space rgb to hsv to process image
    mask = cv2.inRange(hsv, green_lower, green_upper)  # thresholding between specific range
    _, contour, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # find contours in the ball
    contour = sorted(contour, key=lambda t: cv2.contourArea(t), reverse=True)  # getting areas of contours area

    for cnt in contour:
        if cv2.contourArea(cnt) > 1000:  # to eliminate smallest green areas except ball
            M = cv2.moments(cnt)   # find center of mass of ball to get coordinates of those points
            c_x = int(M['m10'] / M['m00'])
            c_y = int(M['m01'] / M['m00'])
            ball_coordinates = c_x, c_y # initializing ball center coordinates in a list
            break
    return ball_coordinates # return coordinates


while True:
    counter, my_frame = my_video.read()  # getting frames from video

    if counter:  # this value turn True if we can get frame then loop work
        final_coordinates = find_green(my_frame)  # getting center coordinates of green ball

        if final_coordinates[0] == -1 and final_coordinates[1] == -1:
            # if final coordinates return [-1, -1] that means ball is out of frame
            out.write(my_frame)
            cv2.imshow('Laser Dot', my_frame)  # showing frame without red dot on it because there is no ball

        else:  # here works when we get positives coordinates which means there is a ball in the frame
            final_coordinates = find_green(my_frame)  # getting coordinates of ball
            # find speed in x axis by difference of center of x coordinates the green ball
            v_x = final_coordinates[0] - initial_coordinates[0]
            # find speed in y axis by difference of center of y coordinates of the green ball
            v_y = final_coordinates[1] - initial_coordinates[1]
            final_frame = red_dot.step(my_frame, (v_x, v_y))  # using step function for putting red dot on frame
            initial_coordinates = final_coordinates  # setting last center coordinates into initial coordinates
            cv2.imshow('Laser Dot', final_frame)    # showing frame with red dot on the ball
            out.write(final_frame)

        if cv2.waitKey(33) & 0xFF == ord('q'):
            break

    else:
        break

out.release()
my_video.release()
cv2.destroyAllWindows()
