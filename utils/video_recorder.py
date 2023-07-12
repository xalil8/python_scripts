import cv2
import numpy as np



video_path = "video_source.py"
# Specify the output video file path
output_path = "dataset.mp4"
# Call the function to start processing

video = cv2.VideoCapture(video_path)


frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)

des_fps = 30
output_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), 30, (frame_width, frame_height))

writing = False

while True:
    try:
        ret, frame = video.read()

        if not ret:
            raise Exception("Error reading frame")

        cv2.imshow("Video", frame)
        key = cv2.waitKey(30)

        if key == ord("q"):
            break
        elif key == ord(" "):
            writing = not writing
            if writing:
                print("Start writing video...")
            else:
                print("Stop writing video.")

        if writing:
            output_video.write(frame)

    except Exception as e:
        print("Error occurred: ", str(e))
        print("Reconnecting...")
        video.release()
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            print("Error reopening video file")
            continue
        empty_frame = np.zeros((frame_height, frame_width, 3), np.uint8)
        cv2.imshow("Video", empty_frame)

video.release()
output_video.release()
cv2.destroyAllWindows()



print("code executed")
