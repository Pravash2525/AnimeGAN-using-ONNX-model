
# Reference from:  https://github.com/TachibanaYoshino/AnimeGANv2

import os
import cv2
import numpy as np
from glob import glob
import zipfile
import onnxruntime as ort
import numpy as np
from tqdm import tqdm 

in_dir = './img_sequences/'
out_dir = "./output/"
model_dir_path  = "./models/" 

os.makedirs(in_dir, exist_ok=True)
os.makedirs(out_dir, exist_ok=True)

# # https://github.com/zunan-islands/AnimeGANv3-Python
model_name = "animeganv3_H64_model"                                        # #@param ['animeganv3_H40_model', 'animeganv3_H50_model', 'animeganv3_H64_model']
onnx_model_type = f"zunan-islands_AnimeGANv3-Python/{model_name}.onnx"    # animeganv3_H64_model == for anime  (average time = 7 sec)

# # https://github.com/TachibanaYoshino/AnimeGANv2
# model_name =  'AnimeGANv2_Hayao'                                         # #@param ['AnimeGAN_Hayao', 'AnimeGANv2_Hayao', 'AnimeGANv2_Shinkai', 'AnimeGANv2_Paprika']
# onnx_model_type = f"TachibanaYoshino_AnimeGANv2/{model_name}.onnx"    #     AnimeGANv2_Hayao == for Realistic  (average time = 14 sec)

# # Other Models: https://github.com/Pravash2525
# model_name =  'AnimeGANv2_Hayao'                                         # #@param ['Shinkai_53', 'AnimeGANv2_Hayao', 'AnimeGANv2_Paprika', 'AnimeGANv3_JP_face_v1', 'AnimeGANv3_PortraitSketch_25']
# onnx_model_type = f"Other_Models/{model_name}.onnx"           #   Let's try  AnimeGANv3_JP_face_v1 == for anime dancing (average time = 7 sec)   
                                                                #    &&&  try  AnimeGANv2_Hayao == for Realistic  (average time = 15 sec)

model_full_path = model_dir_path + onnx_model_type
# ====================================================================================================


pic_form = ['.jpeg','.jpg','.png','.JPEG','.JPG','.PNG']
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
print(f'{model_name}  runtime model is Loaded')


def upload_files_from_local(in_dir):
    files = glob(in_dir + '/*')
    return files

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
    output_image = cv2.resize(images, (scale[1],scale[0]))
    return cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)

def process(files):
    if len(files) == 0:
        print("No files found in the specified directory.")
        return
    
    print('Processing............')
    for image_path in tqdm(files):
        img, scale = load_test_data(image_path)
        res = Convert(img, scale)
        out_name = f"{out_dir}/{os.path.basename(image_path).split('.')[0]}.jpg"
        cv2.imwrite(out_name, res)
    
    # Zip the output folder
    # with zipfile.ZipFile(out_dir + '.zip', 'w') as zipf:
    #     for root, dirs, files in os.walk(out_dir):
    #         for file in files:
    #             zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), out_dir))

    print("Processing complete.")


# Usage
files = upload_files_from_local(in_dir)
process(files)
