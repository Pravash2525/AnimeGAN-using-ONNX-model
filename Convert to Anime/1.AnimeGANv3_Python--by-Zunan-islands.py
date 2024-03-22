
# Reference from:  https://github.com/zunan-islands/AnimeGANv3-Python

import os
import cv2
import onnxruntime as ort
import numpy as np
import sys
import time
from glob import glob
from pathlib import Path

# ====================================================================================================
input_dir_path  = "./img_sequences/"
output_dir_path = "./output/"
model_dir_path  = "./models/"   
os.makedirs(input_dir_path, exist_ok=True)
os.makedirs(output_dir_path, exist_ok=True)

# # https://github.com/zunan-islands/AnimeGANv3-Python
model_name = "animeganv3_H64_model"                                        # #@param ['animeganv3_H40_model', 'animeganv3_H50_model', 'animeganv3_H64_model']
onnx_model_type = f"zunan-islands_AnimeGANv3-Python/{model_name}.onnx"    # animeganv3_H64_model == for anime  (average time = 7 sec)

# # https://github.com/TachibanaYoshino/AnimeGANv2
# model_name =  'AnimeGANv2_Hayao'                                         # #@param ['AnimeGAN_Hayao', 'AnimeGANv2_Hayao', 'AnimeGANv2_Shinkai', 'AnimeGANv2_Paprika']
# onnx_model_type = f"TachibanaYoshino_AnimeGANv2/{model_name}.onnx"    #     AnimeGANv2_Hayao == for Realistic  (average time = 14 sec)

# # Other Models: https://github.com/Pravash2525
# model_name =  'AnimeGANv2_Hayao'                                         # #@param ['Shinkai_53', 'AnimeGANv2_Hayao', 'AnimeGANv2_Paprika', 'AnimeGANv3_JP_face_v1', 'AnimeGANv3_PortraitSketch_25']
# onnx_model_type = f"Other_Models/{model_name}.onnx"           #   Let's try  AnimeGANv3_JP_face_v1 == for anime dancing (average time = 7 sec)   
 

model_full_path = model_dir_path + onnx_model_type
# ====================================================================================================


device_name = ort.get_device()
providers = ""
if device_name == 'CPU':
    providers = ['CPUExecutionProvider']
elif device_name == 'GPU':
    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
print("Name of Providers =", providers)


def LoadImageAsNDArray(path):
    image_mat = cv2.imread(str(path))
    image, width_and_height = PreprocessImage(image_mat)
    image = np.asarray(np.expand_dims(image, 0))
    return (image, tuple(width_and_height))

def PreprocessImage(image, x32=True):
    height, width = image.shape[:2]
    if x32:
        def to_32s(x):
            if x < 256:
                return 256
            return x - x % 32
        image = cv2.resize(image, (to_32s(width), to_32s(height)))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32) / 127.5 - 1.0
    return (image, [width, height])

def SaveImage(transform_image_ndarray, width_and_height, output_image):
    transform_image_ndarray = (transform_image_ndarray.squeeze() + 1.0) / 2 * 255
    transform_image_ndarray = transform_image_ndarray.astype(np.uint8)
    transform_image_ndarray = cv2.resize(transform_image_ndarray, (width_and_height[0], width_and_height[1]))
    save_path =  output_dir_path + output_image
    cv2.imwrite(save_path, cv2.cvtColor(transform_image_ndarray, cv2.COLOR_RGB2BGR))

# ============================================================================================================================
def TransformImage(input_dir_path, model_full_path):                

    # get input image paths
    input_image_paths = [i for i in Path(input_dir_path).glob('**/*.*') if i.suffix.lower() in ('.jpg', '.jpeg', '.png')]
    if len(input_image_paths) == 0:
        print('Error: No images in ".jpg, ".jpeg", ".png" format in specified directory.')
        sys.exit(1)
    
# --------------------------- load onnx runtime model -------------------------------------------------------
    print('Loading...... ONNX runtime model')
    session = ort.InferenceSession(model_full_path, providers=providers) 
    x = session.get_inputs()[0].name
    y = session.get_outputs()[0].name
    print(f'{model_name}  runtime model is Loaded')
# --------------------------------------------------------------------------------------------------------------------
    # start inference
    print('Processing............')
    total_start_at = time.time()
    
    files = glob(input_dir_path + '/*')
    input_image = []
    for img in files:
        image = img.split("\\")[-1]
        input_image.append(image)
  
    count = 0
    for input_image_path in input_image_paths:
        start_at = time.time()

        # load image as ndarray
        image_ndarray, width_and_height = LoadImageAsNDArray(input_image_path)

        # run inference
        transform_data = session.run(None, {x: image_ndarray})

        # save image
        SaveImage(transform_data[0], width_and_height, input_image[count])
        print(f'{count}. Processed image: "{input_image_path}" ({width_and_height[0]}×{width_and_height[1]}) time: {time.time() - start_at:.3f}s')
        count+=1
        
    total_end_at = time.time()
    print(f"Average time per image: {(total_end_at - total_start_at) / len(input_image_paths):.3f}s")


# =======================================================================================================================
if __name__ == '__main__':

    # start transform
    TransformImage(input_dir_path, model_full_path)