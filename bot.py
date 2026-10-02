import os, requests, random, csv, io
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

SHEET_ID = "1hb3WCb4hBcaA4Xz5id7YLyCAcpRRSx2tKk8qHKv6FAM"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

def get_topic():
    r = requests.get(SHEET_URL, timeout=20)
    f = io.StringIO(r.text)
    reader = list(csv.reader(f))
    topics = [row[0].strip() for row in reader[1:] if row and row[0].strip().lower()!= 'topics']
    return random.choice(topics)

def get_pixabay_videos(query):
    q = query.split()[0]
    url = f"https://pixabay.com/api/videos/?key={os.getenv('PIXABAY_KEY')}&q={q}&per_page=20&safesearch=true"
    res = requests.get(url).json()
    return [hit['videos']['medium']['url'] for hit in res.get('hits', [])]

def download_video(url, path):
    r = requests.get(url, stream=True, timeout=30)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk: f.write(chunk)

def make_8min_video():
    topic = get_topic()
    print(f"TOPIC: {topic}")
    vids = get_pixabay_videos(topic)
    if len(vids) < 5: vids = get_pixabay_videos("kids cartoon")

    clips, total, temp_files = [], 0, []
    while total < 480:
        for v_url in vids:
            if total >= 480: break
            fname = f"temp_{len(temp_files)}.mp4"
            download_video(v_url, fname)
            temp_files.append(fname)
            try:
                c = VideoFileClip(fname).subclip(0,8).resize((1280,720))
                clips.append(c); total += 8
            except: continue

    final = concatenate_videoclips(clips).subclip(0,480)
    final.write_videofile("final_8min.mp4", fps=24, codec='libx264', audio=False, preset='ultrafast')
    return "final_8min.mp4", topic

if __name__ == "__main__":
    path, title = make_8min_video()
    print(f"READY: {path} | {title}")
