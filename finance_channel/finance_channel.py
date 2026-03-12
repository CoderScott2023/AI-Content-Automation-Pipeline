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
import os
import random
from PIL import Image
import numpy as np
from moviepy import ImageClip, concatenate_videoclips

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Path to the client secret JSON you downloaded from Google Cloud
CLIENT_SECRET_FILE = r"Youtube-Faceless-Automation-Channel\finance_channel\client_secret.json"  # change if it lives elsewhere

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
            # First time: open browser, you log in and approve
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
            "tags": ["finance", "money", "stocks", "investing", ],
            "categoryId": "25",  # Change to whatever you need
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





IMAGE_FOLDER = r"Youtube-Faceless-Automation-Channel\finance_channel\images"
OUTPUT_BG = r"Youtube-Faceless-Automation-Channel\finance_channel\input_test.mp4"
IMG_DURATION = 5  
TOTAL_IMAGES = 9  
RES = (1080, 1920) # Width, Height (Vertical)

def make_zoom_frame(image_pil, t, duration, zoom_ratio=0.1):
    """Resizes the frame using PIL for a smooth zoom."""
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
    
    # Update this to use your ffmpeg paths if needed (as per previous script)
    os.environ["PATH"] += os.pathsep + r'D:\ffmpeg\bin'
    
    final_bg.write_videofile(
        OUTPUT_BG, 
        fps=24, 
        codec="libx264", 
        bitrate="8000k",
        preset="slow"
    )







FMP_API_KEY = "FMP_API_KEY".strip()  # Get a free key: https://financialmodelingprep.com :contentReference[oaicite:2]{index=2}

TICKERS = [
    "AAPL","MSFT","AMZN","GOOGL","NVDA","TSLA","META","BRK.B","UNH","JNJ",
    "V","PG","MA","HD","DIS","BAC","CMCSA","XOM","PFE","VZ",
    "CSCO","ADBE","NFLX","INTC","KO","PEP","T","ABT","CRM","WMT",
    "MRK","CVX","NKE","TMO","ACN","LLY","TMUS","ORCL","QCOM","MDT",
    "DHR","NEE","TXN","ABBV","HON","MCD","AMGN","COST","LIN","PM",
    "LOW","UNP","UPS","MS","GE","AXP","RTX","IBM","SBUX","BLK",
    "CAT","GS","USB","PLD","MMM","BA","SCHW","GILD","BKNG","ISRG",
    "SPGI","DE","AMT","ADP","CB","ZTS","SYK","NOW","CI","EL",
    "MO","CVS","ISRG","CCI","BDX","MMC","DUK","SO","TGT","CL",
    "CCI","ADI","ETN","FIS","PNC","APD","BDX","ECL","HUM","AON"
]

import requests

def fetch_profile_safe(ticker):
    try:
        url = f"https://financialmodelingprep.com/stable/profile?symbol={ticker}&apikey={FMP_API_KEY}"
        res = requests.get(url, timeout=10).json()
        if isinstance(res, list) and res:
            return res[0]
        elif isinstance(res, dict):
            return res
    except Exception as e:
        print(f"Profile fetch error for {ticker}: {e}")
    return None

def fetch_quote_safe(ticker):
    try:
        url = f"https://financialmodelingprep.com/stable/quote?symbol={ticker}&apikey={FMP_API_KEY}"
        res = requests.get(url, timeout=10).json()
        if isinstance(res, list) and res:
            return res[0]
        elif isinstance(res, dict):
            return res
    except Exception as e:
        print(f"Quote fetch error for {ticker}: {e}")
    return None

def script_generator():
    for _ in range(5):
        ticker = random.choice(TICKERS)
        profile = fetch_profile_safe(ticker)
        quote = fetch_quote_safe(ticker)
        print(str(profile))
        print(str(quote))
        if profile and quote:
            name = profile.get("companyName", ticker)
            industry = profile.get("industry", "the market")
            price = quote.get("price", 0)
            change = quote.get("changePercentage", 0)
            gain_loss_text = "up" if change >= 0 else "down"

            script = (
                f"Breaking finance news: {name} stock is {gain_loss_text} {abs(change):.2f}% today. "
                f"{name} is a company in the {industry} industry. "
                f"Its stock trades under the ticker {ticker} and is currently around ${price:.2f}. "
                f"{profile.get('description', '')[:180]}."
                "Like and subscribe for more finance content."
            )
            return script
    return "Unable to generate script at this time."



os.environ["PATH"] += os.pathsep + r'ffmpeg\bin'

os.environ["IMAGEMAGICK_BINARY"] = r"ImageMagick\magick.exe"

INPUT_VIDEO = r"Youtube-Faceless-Automation-Channel\finance_channel\input_test.mp4"
VOICE = "en-GB-RyanNeural"
MODEL_DIR = r"Youtube-Faceless-Automation-Channel\finance_channel\models"

async def generate_voiceover(text, output_path):
    communicate = edge_tts.Communicate(text, VOICE, rate="-15%")
    await communicate.save(output_path)

def create_video():
    SCRIPT_TEXT = script_generator()
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    print("Step 1: Generating AI Voice...")
    asyncio.run(generate_voiceover(SCRIPT_TEXT, r"Youtube-Faceless-Automation-Channel\finance_channel\voice.mp3"))

    print("Step 2: Transcribing for captions (saving model to D drive)...")
    model = whisper.load_model("base", download_root=MODEL_DIR)
    result = model.transcribe(r"Youtube-Faceless-Automation-Channel\finance_channel\voice.mp3", word_timestamps=True)

    print("Step 3: Processing video layers...")
    video = VideoFileClip(INPUT_VIDEO)
    voice_audio = AudioFileClip(r"Youtube-Faceless-Automation-Channel\finance_channel\voice.mp3")
    
    if os.path.exists(r"Youtube-Faceless-Automation-Channel\finance_channel\music.mp3"):
        bg_music = AudioFileClip(r"Youtube-Faceless-Automation-Channel\finance_channel\music.mp3")
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

    print("Step 4: Rendering final video to D drive...")
    final_video = CompositeVideoClip(clips)
    final_video.write_videofile(OUTPUT_VIDEO, fps=24, codec="libx264")
    print(f"Done! Check {OUTPUT_VIDEO}")

if __name__ == "__main__":
    youtube = authenticate_youtube_upload()

    create_background()
    OUTPUT_VIDEO = os.path.join(r"Youtube-Faceless-Automation-Channel\finance_channel\Final Videos", f"final_video.mp4")
    create_video()

    upload_video(
        youtube,
        file_path=OUTPUT_VIDEO,
        title="Like and subscribe for more finance news💵💰#s",
        description="#investing #stocks #money"
    )
