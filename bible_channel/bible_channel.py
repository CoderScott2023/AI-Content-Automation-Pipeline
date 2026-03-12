import os
import time
import asyncio
import whisper
import edge_tts
from moviepy import VideoFileClip, TextClip, AudioFileClip, CompositeVideoClip, afx, ImageClip, concatenate_videoclips
import requests
import random
from PIL import Image
import numpy as np
import logging
import os
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Full upload scope
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Path to the client secret JSON you downloaded from Google Cloud
CLIENT_SECRET_FILE = "CLIENT-SECRET-FILE.json HERE"  # change if it lives elsewhere

# Where we’ll store the access + refresh tokens after first login. It is automatically saved after first login.
TOKEN_FILE = "token.json"

logging.basicConfig(level=logging.INFO)


def authenticate_youtube_upload():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
          
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    youtube = build("youtube", "v3", credentials=creds)
    return youtube


def upload_video(youtube, file_path, title, description):
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["christianity", "philippenes", "jesus"],
            "categoryId": "20",  # Gaming; change to whatever you need
        },
        "status": {
            "privacyStatus": "public",
        },
    }

    media = MediaFileUpload(
        file_path,
        chunksize=-1,
        resumable=True,
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            logging.info(f"Upload progress: {int(status.progress() * 100)}%")

    logging.info(f"Upload complete! Video ID: {response['id']}")
    return response["id"]




import os
import random
from PIL import Image
import numpy as np
from moviepy import ImageClip, concatenate_videoclips
IMAGE_FOLDER = "PUT YOUR IMAGE REPOSITORY FOLDER HERE"
OUTPUT_BG = "input.mp4"
IMG_DURATION = 5  
TOTAL_IMAGES = 5  
RES = (1080, 1920) # Width, Height (Vertical). Change as you wish

def make_zoom_frame(image_pil, t, duration, zoom_ratio=0.1):
    w, h = RES
    current_zoom = 1 + (zoom_ratio * (t / duration))
    
    new_w, new_h = int(w * current_zoom), int(h * current_zoom)
    
    resized_img = image_pil.resize((new_w, new_h), Image.LANCZOS)
    
    left = (new_w - w) / 2
    top = (new_h - h) / 2
    right = (new_w + w) / 2
    bottom = (new_h + h) / 2
    
    return np.array(resized_img.crop((left, top, right, bottom)))

def create_background():
    all_images = [os.path.join(IMAGE_FOLDER, f) for f in os.listdir(IMAGE_FOLDER) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not all_images:
        print("Error: No images found!")
        return

    selected_images = random.sample(all_images, min(TOTAL_IMAGES, len(all_images)))
    clips = []

    for img_path in selected_images:
        print(f"Adding {os.path.basename(img_path)}...")
   
        current_img = Image.open(img_path).convert("RGB")
        
        img_ratio = current_img.width / current_img.height
        target_ratio = RES[0] / RES[1]
        
        if img_ratio > target_ratio:
            new_h = RES[1]
            new_w = int(new_h * img_ratio)
        else:
            new_w = RES[0]
            new_h = int(new_w / img_ratio)
            
        current_img = current_img.resize((new_w, new_h), Image.LANCZOS)

        left = (new_w - RES[0]) / 2
        top = (new_h - RES[1]) / 2
        current_img = current_img.crop((left, top, left + RES[0], top + RES[1]))

        clip = ImageClip(np.array(current_img)).with_duration(IMG_DURATION)
        animated = clip.transform(
            lambda get_frame, t, i=current_img: make_zoom_frame(i, t, IMG_DURATION)
        )
        clips.append(animated)

    print("Rendering background video...")
    final_bg = concatenate_videoclips(clips, method="compose")
    
    # Update this to use your D-drive paths if needed
    os.environ["PATH"] += os.pathsep + r'D:\ffmpeg\bin'
    
    final_bg.write_videofile(
        OUTPUT_BG, 
        fps=24, 
        codec="libx264", 
        bitrate="8000k",
        preset="slow"
    )








def get_bible_verse():
    themes = {
        "Law": "This reminds us that following the right path leads to a life of true purpose.",
        "History": "We see here how the past shapes the strength of our faith in the present.",
        "Poetry": "This beautiful imagery serves as a comfort for the soul in times of need.",
        "Prophecy": "A powerful reminder that even in uncertainty, there is a greater plan at work.",
        "Gospel": "This teaches us the ultimate lesson of love and sacrifice for one another.",
        "Letter": "An encouraging call to live with integrity and grace in our daily lives."
    }

    random_book_id = random.randint(1, 66)

    try:
        url = f"https://bolls.life/get-random-verse/NIV/?book={random_book_id}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return f"API error: {response.status_code}"

        data = response.json()

        # handle both list and dict responses
        if isinstance(data, list):
            data = data[0]

        book_name = data["book"]
        chapter = data["chapter"]
        verse_num = data["verse"]
        verse_text = data["text"].strip()

        if random_book_id <= 5:
            theme = themes["Law"]
        elif random_book_id <= 17:
            theme = themes["History"]
        elif random_book_id <= 22:
            theme = themes["Poetry"]
        elif random_book_id <= 39:
            theme = themes["Prophecy"]
        elif random_book_id <= 43:
            theme = themes["Gospel"]
        else:
            theme = themes["Letter"]

        return f"{book_name} chapter {chapter} verse {verse_num}. {verse_text} {theme}"

    except Exception as e:
        return f"Error: {e}"





# 1. Point to the FFmpeg folder (required for reading/writing video)
os.environ["PATH"] += os.pathsep + r'D:\ffmpeg\bin'

# 2. Point to ImageMagick (required for TextClip captions)
# Note: Ensure you checked "Install legacy utilities" during ImageMagick install
os.environ["IMAGEMAGICK_BINARY"] = r"D:\ImageMagick\magick.exe"

INPUT_VIDEO = "input.mp4"
VOICE = "en-GB-RyanNeural" #Adapt this to whatever voice you choose
MODEL_DIR = "CHOOSE WHICH DIRECTORY TO SAVE THE MODEL TO"

async def generate_voiceover(text, output_path):
    # Choose whatever rate is good for you. -15% seemed to be normal talking voice, but adapt as you wish
    communicate = edge_tts.Communicate(text, VOICE, rate="-15%")
    await communicate.save(output_path)

def create_video():
    SCRIPT_TEXT = get_bible_verse()

    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    print("Step 1: Generating AI Voice...")
    asyncio.run(generate_voiceover(SCRIPT_TEXT, "voice.mp3"))

    print("Step 2: Transcribing for captions")
    model = whisper.load_model("base", download_root=MODEL_DIR)
    result = model.transcribe("voice.mp3", word_timestamps=True)

    print("Step 3: Processing video layers...")
    video = VideoFileClip(INPUT_VIDEO)
    voice_audio = AudioFileClip("voice.mp3")

    if os.path.exists("music.mp3"):
        bg_music = AudioFileClip("music.mp3")
        bg_music = bg_music.with_volume_scaled(0.1) 
        bg_music = bg_music.with_effects([afx.AudioFadeOut(2)]) 
        bg_music = bg_music.with_duration(voice_audio.duration)

        from moviepy import CompositeAudioClip
        final_audio = CompositeAudioClip([voice_audio, bg_music])
    else:
        print("Music file not found, skipping background music.")
        final_audio = voice_audio

    video = video.with_audio(final_audio).with_duration(voice_audio.duration)
  
    clips = [video]
    for segment in result['segments']:
        for word in segment['words']:
            txt = TextClip(
                text=word['word'].upper(), 
                font_size=70, 
                color='white', 
                font=r'C:\Windows\Fonts\arialbd.ttf',
                stroke_color='black',
                stroke_width=20,
                method='label',
                margin=(0, 0, 0, 10)
            ).with_start(word['start']).with_end(word['end']).with_position(('center', 'center'))
            clips.append(txt)
          
    final_video = CompositeVideoClip(clips)
    final_video.write_videofile(OUTPUT_VIDEO, fps=24, codec="libx264")

if __name__ == "__main__":
    youtube = authenticate_youtube_upload()
    create_background()
    OUTPUT_VIDEO = os.path.join(r"D:\FULL AUTOMATION CONTROLLER\bible_channel\Final Videos", f"final_video.mp4")
    create_video()

    upload_video(
        youtube,
        file_path=OUTPUT_VIDEO,
        title="Jesus Loves You❤️✝️#s",
        description="#jesus #christian #christianity"
    )
