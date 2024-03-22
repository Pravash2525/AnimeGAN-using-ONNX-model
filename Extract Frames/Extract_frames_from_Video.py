## Extract frames from Video

# pip install opencv-python

import cv2
import os

videoName = "Kim.mp4"
vidcap = cv2.VideoCapture(f"./Video/{videoName}")  # give the location of video

fps = int(vidcap.get(cv2.CAP_PROP_FPS))
print(f"{videoName} has fps == ", fps)

# create a folder if doesn't exists
if not os.path.exists('./img_sequences/'):
	os.makedirs('./img_sequences/')

currentFrame = 10000
while vidcap.isOpened():
	success, frame = vidcap.read()
	
	if success:
		fileName = f"./img_sequences/{currentFrame}.jpg"
		cv2.imwrite(fileName, frame)  # frame will saved in "frames" folder
		print(f"Creating Images......{currentFrame}")
		currentFrame+=1
	else:
		break
	
vidcap.release()
cv2.destroyAllWindows()

