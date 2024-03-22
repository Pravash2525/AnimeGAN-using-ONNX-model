# import cv2
# import os

# videoName = "Kala_Sha_kala.mp4"

# vidcap = cv2.VideoCapture(f"./Video/{videoName}")  # give the location of video

# p = 1
# n = 0
# i = 0

# total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
# fps = int(vidcap.get(cv2.CAP_PROP_FPS))
# video_length = total_frames/fps
# frames_to_extract = total_frames // (video_length * p)

# print(total_frames)
# print(fps)
# print(video_length)
# print(frames_to_extract)

# while True:
#     ret, frame = vidcap.read()
#     if (n % frames_to_extract) == 0:
#         i += 1
#         cv2.imwrite(f"./img_sequences/{i}.jpg", frame)
#         print(f"Creating Images......{i}")
        
#     n += 1
#     if ret == False or n >= total_frames:
#         break

# vidcap.release()
# cv2.destroyAllWindows()


x = 6//4
y = 6%4
print(x)
print(y)