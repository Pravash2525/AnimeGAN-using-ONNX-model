## Sequence Photos to Video
import cv2
import os 

# ==================================================================================
# mention the fps of a video 
# Note: high fps == short_video_length
fps = 10
# ===================================================================================

in_path = './img_sequences/'
out_path = './img_to_video/'
out_video_name = 'combined.mp4'
os.makedirs(out_path, exist_ok=True)
out_video_full_path = out_path + out_video_name

pre_images = os.listdir(in_path)
# print(pre_images)

img = []
for i in pre_images:
	i = in_path + i
	img.append(i)

cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')
frame = cv2.imread(img[0])
size = list(frame.shape)
del size[2]
size.reverse()

video = cv2.VideoWriter(out_video_full_path, cv2_fourcc, fps, size) #output video name, fourcc, fps, size

for i in range(len(img)): 
    video.write(cv2.imread(img[i]))
    print('frame ', i+1, ' of ', len(img))

video.release()
print('outputed video saved to: ', out_path)
