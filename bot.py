import os
print("BOT STARTED")
os.system("ffmpeg -y -f lavfi -i color=c=black:s=1280x720:d=480 -f lavfi -i anullsrc=r=44100:cl=stereo -shortest final_8min.mp4")
print("Done - file exists:", os.path.exists("final_8min.mp4"))
