import os, random, datetime, textwrap
from gtts import gTTS
from PIL import Image, ImageDraw

TOPICS = [
    "Twinkle Twinkle Little Star Poem for Babies",
    "Johny Johny Yes Papa Poem",
    "Wheels on the Bus Poem",
    "Baby Shark Song for Kids",
    "Lakdi Ki Kathi Poem",
    "Frozen Movie Explained for Kids",
    "Lion King Story Explained",
    "Avengers Endgame for Kids",
    "SpiderMan Story for Kids",
    "Two Cats and Monkey Funny Story",
    "Akbar Birbal Funny Story",
    "Foolish Donkey Moral Story",
    "Honest Woodcutter Story",
    "Why Sky is Blue Science for Kids",
    "How Rainbow Form Science",
    "What is Gravity Science",
    "Why Stars Twinkle Science"
]

HASHTAGS = "#kids #babypoem #cartoon #kidssong #funny #moralstory #scienceforkids #learning #education #kidsvideo"

def make_video(topic, filename):
    script = f"Hello kids! Today: {topic}. " * 70
    tts = gTTS(text=script, lang='en')
    tts.save("voice.mp3")
    img = Image.new('RGB', (1280,720), random.choice([(255,107,107),(78,205,196),(255,230,109)]))
    d = ImageDraw.Draw(img)
    for j, line in enumerate(textwrap.wrap(topic, 28)):
        d.text((80, 250+j*70), line, fill=(0,0,0))
    d.text((80,650), "Kids Learning TV", fill=(255,255,255))
    img.save("bg.jpg")
    os.system(f'ffmpeg -y -loop 1 -i bg.jpg -i voice.mp3 -c:v libx264 -c:a aac -shortest -t 480 {filename}')
    os.remove("voice.mp3")
    os.remove("bg.jpg")
    return filename

def upload_yt(file, title):
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        creds = Credentials(None, refresh_token=os.getenv("YT_REFRESH_TOKEN"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.getenv("YT_CLIENT_ID"),
            client_secret=os.getenv("YT_CLIENT_SECRET"),
            scopes=["https://www.googleapis.com/auth/youtube.upload"])
        yt = build("youtube", "v3", credentials=creds)
        
        yt.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": f"{title}\n\n{title} for kids.\n\n{HASHTAGS}",
                    "tags": ["kids","poem","story","science","cartoon"],
                    "categoryId": "27"
                },
                "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": True}
            },
            media_body=MediaFileUpload(file)
        ).execute()
        print(f"✅ UPLOADED: {title}")
    except Exception as e:
        print(f"Upload skip (keys nahi hain): {e}")

today = datetime.date.today()
random.seed(today.toordinal() + datetime.datetime.now().hour)
topic = random.choice(TOPICS)

file = f"video_{today}.mp4"
make_video(topic, file)
upload_yt(file, topic)
