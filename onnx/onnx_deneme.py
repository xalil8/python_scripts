
#TODO make polygons filled with transparant color
import onnxruntime as ort
import cv2
import numpy as np
import time
import torch 
import pandas
import cv2
import numpy as np
import time
from xalil_nonmaxsup import non_max_suppression
start_time = time.time()



#PATH CONFIGURATION
source_video_path = "short_raw.mp4"
video_saving_path = "onnx_first_output.mp4"

#ML MODEL CONFIGURATION

model_path = "genel_model.onnx"

session = ort.InferenceSession(model_path,providers=['CoreMLExecutionProvider', 'CPUExecutionProvider'])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name


#VIDEO CONFIGURATION
video_cap = cv2.VideoCapture(source_video_path)
fps = video_cap.get(cv2.CAP_PROP_FPS)
width, height = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
desired_fps = 35
result = cv2.VideoWriter(video_saving_path, cv2.VideoWriter_fourcc(*'mp4v'), desired_fps, (640, 640))


count=0
while video_cap.isOpened():
    ret,frame=video_cap.read()

    if not ret:
        break
    #ADJUST FPS
    count += 1
    if count % 1 != 0:
        continue

    """if count == 25:
        break"""

    input_data = cv2.resize(frame, (640, 640))[:,:,::-1].transpose(2, 0, 1).astype(np.float32) / 255.0
    input_data = np.expand_dims(input_data, axis=0)
    outputs = session.run([output_name], {input_name: input_data})

    #print(outputs.shape)
    y = torch.tensor(outputs[0]) if isinstance(outputs[0], np.ndarray) else outputs[0]
    pred = non_max_suppression(y)
    pred_array = pred[0].numpy()

    resized_frame = cv2.resize(frame, (640, 640))
    for box in pred_array:
        x1,y1,x2,y2,conf,clas_num = int(box[0]),int(box[1]),int(box[2]),int(box[3]),box[4],int(box[5])

        #cv2.putText(resized_frame, "asd", (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0,0,255), 2)
        cv2.rectangle(resized_frame, (x1, y1), (x2,y2), (0,255,0), 1)
    
    #cv2.imshow("ROI",resized_frame)
    print(f"frame {count} writing")
    result.write(resized_frame)


    if cv2.waitKey(1) == ord('q'):
        break


video_cap.release()
result.release()
cv2.destroyAllWindows()
print("process done")
print("Execution time:", time.time() - start_time, "seconds")
