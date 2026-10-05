import os
print("BOT STARTED - No Pixabay needed")

from moviepy.editor import ColorClip, AudioFileClip, concatenate_audioclips
from gtts import gTTS
import random

def make_8min_video():
    TARGET = 8*60 # 8 minute

    # 1. Voice banate hain
    topics = ["Motivation for success", "Life is beautiful and you can win"]
    text = random.choice(topics) + ". " * 20
    print(f"Topic: {text[:50]}")

    gTTS(text, lang='en', slow=False).save("voice.mp3")
    audio = AudioFileClip("voice.mp3")

    # Audio ko 8 min tak loop karo
    loops = int(TARGET / audio.duration) + 2
    final_audio = concatenate_audioclips([audio]*loops).subclip(0, TARGET)

    # 2. Simple black video with audio - 100% working
    video = ColorClip((1280, 720), color=(15, 15, 15), duration=TARGET).set_audio(final_audio)

    video.write_videofile("final_8min.mp4", fps=24, codec='libx264', audio_codec='aac')
    print("SUCCESS - Video ready")
    return "final_8min.mp4", "Fixed Video"

if __name__ == "__main__":
    make_8min_video()



