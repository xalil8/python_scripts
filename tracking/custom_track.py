#import argparse
import cv2
import os
# limit the number of cpus used by high performance libraries
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import sys
import platform
import numpy as np
from pathlib import Path
import torch
import torch.backends.cudnn as cudnn


#import logging
from yolov8.ultralytics.nn.autobackend import AutoBackend
from yolov8.ultralytics.yolo.data.dataloaders.stream_loaders import LoadImages, LoadStreams
from yolov8.ultralytics.yolo.data.utils import IMG_FORMATS, VID_FORMATS
from yolov8.ultralytics.yolo.utils import DEFAULT_CFG, LOGGER, SETTINGS, callbacks, colorstr, ops
from yolov8.ultralytics.yolo.utils.checks import check_file, check_imgsz, check_imshow, print_args, check_requirements
from yolov8.ultralytics.yolo.utils.files import increment_path
#from yolov8.ultralytics.yolo.utils.torch_utils import select_device
from yolov8.ultralytics.yolo.utils.ops import Profile, non_max_suppression, scale_boxes, process_mask, process_mask_native
from yolov8.ultralytics.yolo.utils.plotting import Annotator, colors, save_one_box

from trackers.multi_tracker_zoo import create_tracker


@torch.no_grad()
def main():

    ####################### MY CONFIGURATION ##########################
    source = "output.mp4"
    #device = "mps"
    yolo_weights= "yolov8m.pt"  # model.pt path(s),
    classes=None  # filter by class: --class 0, or --class 0 2 3
    #show_vid = True
    tracking_method='bytetrack'
    tracking_config="trackers/bytetrack/configs/bytetrack.yaml"
    reid_weights="weights/osnet_x0_25_msmt17.pt"  # model.pt path,


    imgsz=[640, 640]  # inference size (height, width)
    conf_thres=0.25  # confidence threshold
    iou_thres=0.45  # NMS IOU threshold
    max_det=1000  # maximum detections per image
    half=False  # use FP16 half-precision inference
    dnn=False  # use OpenCV DNN for ONNX inference
    line_thickness=2  # bounding box thickness (pixels)
    save_trajectories=False  # save trajectories for each track
    #save_vid=False  # save confidences in --save-txt labels
    agnostic_nms=False  # class-agnostic NMS
    augment=False  # augmented inference
    visualize=False  # visualize features
    vid_stride=1  # video frame-rate stride




    # Load model
    device = torch.device("mps")
    #device = select_device(device)
    model = AutoBackend(yolo_weights, device=device, dnn=dnn, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_imgsz(imgsz, stride=stride)  # check image size

    # Dataloader
    bs = 1

    dataset = LoadImages(
            source,
            imgsz=imgsz,
            stride=stride,
            auto=pt,
            transforms=getattr(model.model, 'transforms', None),
            vid_stride=vid_stride # fps stride = 1
        )
    
    #vid_path, vid_writer, txt_path = [None] * bs, [None] * bs, [None] * bs
    #model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    model.warmup(imgsz=(1, 3, *imgsz))  # warmup

    # Create as many strong sort instances as there are video sources
    tracker_list = []

    tracker = create_tracker(tracking_method, tracking_config, reid_weights, device, half)
    tracker_list.append(tracker, )
    if hasattr(tracker_list, 'model'):
        if hasattr(tracker_list.model, 'warmup'):
            tracker_list[i].model.warmup()

    outputs = [None] * bs

    # Run tracking
    #model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], (Profile(), Profile(), Profile(), Profile())
    #curr_frames, prev_frames = [None], [None]
    curr_frames = [None]


    #################POLYGON####################
    polygon_points= np.array([[226, 307], [706, 305]])

    polygon_points_2= np.array( [[226, 307], [706, 305], [712, 337], [201, 338]])

    object_counter = 0
    passing_dict = {}
    for frame_idx, batch in enumerate(dataset):
        
        #im  is processed image
        #im0s is raw data, without any preprocess, mostly used in visulization
        path, im, im0s, vid_cap, s = batch
        #visualize = increment_path(save_dir / Path(path[0]).stem, mkdir=True) if visualize else False
        cv2.polylines(im0s, np.int32([polygon_points]), True, (255,0,0),3)

        with dt[0]:
            im = torch.from_numpy(im).to(device)
            im = im.half() if half else im.float()  # uint8 to fp16/32
            im /= 255.0  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim

        # Inference
        with dt[1]:
            preds = model(im, augment=augment, visualize=visualize)

        # Apply NMS
        with dt[2]:

            p = non_max_suppression(preds, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        

        # Process detections
        for i, det in enumerate(p):  # detections per image
            seen += 1

            p, im0, _ = path, im0s.copy(), getattr(dataset, 'frame', 0)
            p = Path(p)  # to Path
            cv2.putText(im0, f"{object_counter} OBJECT PASSED ", (30,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

            # video file
            #if source.endswith(VID_FORMATS):
            #    txt_file_name = p.stem
                #save_path = str(save_dir / p.name)  # im.jpg, vid.mp4, ...
            # folder with imgs
            #else:
            #    txt_file_name = p.parent.name  # get folder name containing current img
                #save_path = str(save_dir / p.parent.name)  # im.jpg, vid.mp4, ...
            curr_frames[i] = im0

            #txt_path = str(save_dir / 'tracks' / txt_file_name)  # im.txt
            s += '%gx%g ' % im.shape[2:]  # print string

            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            
            #if hasattr(tracker_list[i], 'tracker') and hasattr(tracker_list[i].tracker, 'camera_update'):
            #    if prev_frames[i] is not None and curr_frames[i] is not None:  # camera motion compensation
            #        tracker_list[i].tracker.camera_update(prev_frames[i], curr_frames[i])

            if det is not None and len(det):

                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()  # rescale boxes to im0 size

                # Print results
                for c in det[:, 5].unique():
                    n = (det[:, 5] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

#############################DEEP SORT WORKING HERE ##########################
                # pass detections to strongsort
                with dt[3]:
                    outputs[i] = tracker_list[i].update(det.cpu(), im0)
                
                # draw boxes for visualization

                if len(outputs[i]) > 0:
                    for j, (output) in enumerate(outputs[i]):
                        #print(output)
                        bbox = output[0:4]
                        id = output[4]
                        cls = output[5]
                        conf = output[6]
                        
                        x1, y1, x2, y2 = bbox
                        x1, y1, x2, y2, c, id= int(x1),int(y1),int(x2), int(y2), int(cls), int(id)
                        ###############################ALGORITHM WORK HERE###################################
                        center_x, center_y= int((x1+x2)/2), int((y1+y2)/2)
                        area_check_1 = cv2.pointPolygonTest(np.int32([polygon_points_2]),((center_x,center_y)), False)
                        
                        cv2.circle(im0, (center_x, center_y), radius=3, color=(0, 0, 255), thickness=-1)
                        cv2.rectangle(im0,(x1,y1),(x2,y2),(20,255,20),2)
                        cv2.putText(im0, f"{names[int(c)]}{str(id)}", (x1,y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20,255,20), 2)

                        color = colors(c, True)


                        if id not in passing_dict:
                            passing_dict[id] = 0
                        if area_check_1 == 1:
                            new_val = passing_dict[id] + 1
                            passing_dict.update({id:new_val})
                            if passing_dict[id] == 1:
                                object_counter += 1
                        ##################################################################
                        #annotator.box_label(bbox, "", color=color)
                        
                        if save_trajectories and tracking_method == 'strongsort':
                            q = output[7]
                            tracker_list[i].trajectory(im0, q, color=color)

                
            # Stream results
            im0 = annotator.result()

            cv2.imshow(str(p), im0)

            if cv2.waitKey(1) == ord('q'):  # 1 millisecond
                exit()

            #prev_frames[i] = curr_frames[i]
            


        # Print total time (preprocessing + inference + NMS + tracking)
        LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{sum([dt.dt for dt in dt if hasattr(dt, 'dt')]) * 1E3:.1f}ms")

    # Print results
    t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS, %.1fms {tracking_method} update per image at shape {(1, 3, *imgsz)}' % t)



if __name__ == "__main__":
    main()
