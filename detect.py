import torch
import cv2
from models.experimental import attempt_load
from utils.datasets import  LoadImages
from utils.general import check_img_size, non_max_suppression,scale_coords
from config_loader import load_config
import time

config = load_config('config.yml')

_model_instance = None

def get_model_instance(model_path=config['model_path'], device='cpu'):
    global _model_instance
    if _model_instance is None:
        _model_instance = attempt_load(model_path, map_location=device)
    return _model_instance


def detect(image,model_path=None,imgsz=640):
    model = get_model_instance(model_path) if model_path is not None else get_model_instance()
    detected_objects = []
    device = 'cpu'
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    dataset = LoadImages(image, img_size=imgsz, stride=stride)
    names = model.module.names if hasattr(model, 'module') else model.names
    for _, img, im0s, _ in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.float()
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        # Inference
        with torch.no_grad():
            pred = model(img)[0]

        # Apply NMS
        pred = non_max_suppression(pred)

        # Process detections
        for det in pred: 
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    obj_info = [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3]), names[int(cls)], conf.item()]
                    detected_objects.append(obj_info)
                    
    # print("detected_objects >>",detected_objects)
    # for box in detected_objects:
    #     cv2.rectangle(imags,(int(box[0]),int(box[1])),(int(box[2]),int(box[3])),(255,255,0),2)
    # cv2.imshow("image",imags)
    # cv2.waitKey(0)
    return detected_objects



if __name__ == '__main__':
    img_path = "elephant.jpeg"
    result = detect(img_path,"yolov7.pt",640)
    print(result)

