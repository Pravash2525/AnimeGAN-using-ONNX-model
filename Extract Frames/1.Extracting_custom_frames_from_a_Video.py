
import cv2
import os

videoName = "dfd.mp4"

input_dir_path  = "./img_sequences/"
os.makedirs(input_dir_path, exist_ok=True)

vidcap = cv2.VideoCapture(f"./Video/{videoName}")  # give the location of video
# Get video properties
fps 		 = int(vidcap.get(cv2.CAP_PROP_FPS))
total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
video_length = total_frames / fps
width 		 = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
height 		 = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("FPS:", fps)
print("Total Frames:", total_frames)
print(f"Width*Height: ({width}*{height})")
print(f"Video Length: {video_length:.2f} seconds")
# =========================================================================================== 
# to extract all frames:     p = int(video_length)     or put bigger number
# to extract minimum frames: p = 1
# to extract twice frames:   p = 2
# to extract thrice frames:  p = 3
# and so on 
# ------------------------------------------------------
p = 77    # int(video_length) 
# ===========================================================================================

n = 0     	     
i = 100000	    # image name
frames_to_extract = total_frames // (video_length * p)

while True:
    ret, frame = vidcap.read()
    if (n % frames_to_extract) == 0:
        i += 1
        cv2.imwrite(f"./img_sequences/{i}.jpg", frame)
        print(f"Creating Images......{i}")
        
    n += 1
    if ret == False or n >= total_frames:
        break

vidcap.release()
cv2.destroyAllWindows()




# path = os.getcwd()+ "/Video/" 					# path = os.path.join(location, file)
# video_list = os.listdir(path)
# print(video_list)





