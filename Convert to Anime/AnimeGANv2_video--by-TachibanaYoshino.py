
# Reference from:  https://github.com/TachibanaYoshino/AnimeGANv2

import os
import cv2
import numpy as np
from glob import glob
import onnxruntime as ort
import numpy as np
from tqdm import tqdm 

# ==========================================================================================
# if you don't want to change fps, then put  "fps = 0"
# else  provide the custom fps               "fps = 24"
videoName = "dfd.mp4" 
fps       = 0      

# ==================================================================================================
# # https://github.com/zunan-islands/AnimeGANv3-Python
# model_name = "animeganv3_H64_model"                                        # #@param ['animeganv3_H40_model', 'animeganv3_H50_model', 'animeganv3_H64_model']
# onnx_model_type = f"zunan-islands_AnimeGANv3-Python/{model_name}.onnx"    # animeganv3_H64_model == for anime  (average time = 7 sec)

# # https://github.com/TachibanaYoshino/AnimeGANv2
# model_name =  'AnimeGANv2_Hayao'                                         # #@param ['AnimeGAN_Hayao', 'AnimeGANv2_Hayao', 'AnimeGANv2_Shinkai', 'AnimeGANv2_Paprika']
# onnx_model_type = f"TachibanaYoshino_AnimeGANv2/{model_name}.onnx"    #     AnimeGANv2_Hayao == for Realistic  (average time = 14 sec)

# # Other Models: https://github.com/Pravash2525
model_name =  'AnimeGANv3_JP_face_v1'                                         # #@param ['Shinkai_53', 'AnimeGANv2_Hayao', 'AnimeGANv2_Paprika', 'AnimeGANv3_JP_face_v1', 'AnimeGANv3_PortraitSketch_25']
onnx_model_type = f"Other_Models/{model_name}.onnx"           #   Let's try  AnimeGANv3_JP_face_v1 == for anime dancing (average time = 7 sec)   
                                                               # #    &&&  try  AnimeGANv2_Hayao == for Realistic  (average time = 15 sec)
out_dir = "./output/"
model_dir_path  = "./models/" 
vid_path = f"./Video/{videoName}"
os.makedirs(out_dir, exist_ok=True)
model_full_path = model_dir_path + onnx_model_type
# ====================================================================================================
vid_form = ['.mp4','.avi','.mkv']
device_name = ort.get_device()

providers = ""
if device_name == 'CPU':
    providers = ['CPUExecutionProvider']
elif device_name == 'GPU':
    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']    
print("Name of Providers =", providers)

#load model
print('Loading...... ONNX runtime model')
session = ort.InferenceSession(model_full_path, providers=providers)
print(f'"{model_name}"  runtime model is Loaded')

def post_process(img, wh):
    img = (img.squeeze()+1) / 2*255
    img = img.astype(np.uint8).clip(0,255)
    img = cv2.resize(img, (wh[0],wh[1]))
    return img

def process_image(img, x32=True):
    h, w = img.shape[:2]
    if x32: # resize image to multiple of 32s
        def to_32s(x):
            return 256 if x < 256 else x - x%32
        img = cv2.resize(img, (to_32s(w), to_32s(h)))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)/ 127.5 - 1.0
    return img

def load_test_data(image_path):
    img0 = cv2.imread(image_path).astype(np.float32)
    img = process_image(img0)
    img = np.expand_dims(img, axis=0)
    return img, img0.shape[:2]

def Convert(img, scale):
    x = session.get_inputs()[0].name
    y = session.get_outputs()[0].name
    fake_img = session.run(None, {x : img})[0]
    images = (np.squeeze(fake_img) + 1.) / 2 * 255
    images = np.clip(images, 0, 255).astype(np.uint8)
    output_image = cv2.resize(images,scale[::-1])
    return cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)

def get_video(video, out_name, my_fps):
    vidcap = cv2.VideoCapture(video)  # give the location of video
    video_name   = os.path.basename(video)
    # Get video properties
    vid_fps 	 = int(vidcap.get(cv2.CAP_PROP_FPS))
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_length = total_frames / vid_fps
    width 		 = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height 		 = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    if my_fps == 0:
        set_fps = vid_fps
    else:
        set_fps = fps
    print("Your Video Will Have...........")
    print("Video Name:", video_name)
    print("FPS:", fps)
    print("Total Frames:", total_frames)
    print(f"Width*Height: ({width}*{height})")
    print(f"Video Length: {video_length:.2f} seconds")

    video_out = cv2.VideoWriter(out_name, cv2_fourcc, set_fps, (width,height))
    pbar = tqdm(total=total_frames,)
    pbar.set_description(f"Making: {video_name.rsplit('.',1)[0] + '_AnimeGAN.mp4'}" )

    while True:
        ret, frame = vidcap.read()
        if not ret:
            break
        frame = np.asarray(np.expand_dims(process_image(frame),0))
        x = session.get_inputs()[0].name
        y = session.get_outputs()[0].name
        fake_img = session.run(None, {x : frame})[0]
        fake_img = post_process(fake_img, (width, height))
        video_out.write(cv2.cvtColor(fake_img, cv2.COLOR_BGR2RGB))
        pbar.update(1)

    vidcap.release()
    video_out.release()
    

# name of output video
out_name = f"{out_dir}/{os.path.basename(vid_path).split('.')[0]}_AnimeGAN.mp4"
get_video(vid_path, out_name, fps)

