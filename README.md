PROJECT NAME
YouTube Faceless Automation Channel

PROJECT DESCRIPTION

This project is a fully automated Python-based pipeline designed to generate, render, and publish short-form informational videos with minimal human interaction. The system integrates multiple APIs, machine learning models, and media processing libraries to automate the entire production workflow from script generation to final upload.

The goal of this project was to explore large-scale automation systems, media generation pipelines, and API integration by building a system capable of producing short-form content automatically across multiple independent channels.

The system supports multiple automated content pipelines simultaneously, each operating as its own independent channel. A central controller script schedules and orchestrates the pipelines, enabling scalable automated media production.


SYSTEM OVERVIEW

The automation system performs the following steps:

1. Generate a script for the video
2. Convert the script into AI-generated voice narration
3. Transcribe the narration to obtain word-level timestamps
4. Generate animated background footage
5. Render captions synchronized with speech
6. Assemble the final video
7. Upload the finished video automatically using the YouTube API

Each of these steps is performed programmatically using Python scripts and third-party libraries.


SYSTEM ARCHITECTURE

The project is organized as a pipeline controlled by a scheduling controller.

Controller Scheduler
        |
        |---- Bible Channel Pipeline
        |        |---- Script Generator
        |        |---- AI Voice Generation
        |        |---- Speech Transcription
        |        |---- Caption Rendering
        |        |---- Video Composition
        |        |---- Automated Upload
        |
        |---- Finance Channel Pipeline
                 |---- Data API Retrieval
                 |---- Script Generator
                 |---- AI Voice Generation
                 |---- Caption Rendering
                 |---- Video Composition
                 |---- Automated Upload

Each channel runs its own script and environment while the controller schedules execution.


MULTI-CHANNEL AUTOMATION

The project includes a controller script that acts as a scheduler for multiple content pipelines. Each channel is defined as a job with its own configuration including script location, execution environment, and upload interval.

Example job configuration:

jobs = [
    {
        "name": "bible",
        "script": "bible_channel.py",
        "folder": "...",
        "python": "...",
        "interval": 43200,
        "offset": 0
    },
    {
        "name": "finance",
        "script": "finance_channel.py",
        "folder": "...",
        "python": "...",
        "interval": 43200,
        "offset": 0
    }
]

The scheduler continuously runs and launches each job based on its configured timing interval. Channels can also be staggered using offsets to prevent simultaneous execution.

The system can support many channels depending on available computing resources.


SCRIPT GENERATION

Scripts are generated dynamically depending on the content niche.

For example, the finance channel pulls real-time stock data from a financial API and generates short narration scripts describing stock movements and company information.

Example generated narration:

Breaking finance news: Apple stock is up 1.32 percent today. Apple is a company in the consumer electronics industry. Its stock trades under the ticker AAPL and is currently around 185 dollars.


AI VOICE GENERATION

Narration is generated automatically using neural text-to-speech technology.

The project uses Edge TTS voices which provide natural-sounding speech synthesis. Voice type and speaking rate can be configured within the pipeline.


SPEECH TRANSCRIPTION AND CAPTIONING

The project uses a speech recognition model to transcribe the generated narration.

The transcription process extracts word-level timestamps which are then used to generate synchronized captions for the video.

Model used:
Whisper speech recognition model.

Captions are rendered dynamically during video composition.


VIDEO RENDERING

Video assembly is performed programmatically using the MoviePy library.

The video generation pipeline includes:

- Animated background images with slow zoom effects
- Caption overlays synchronized with speech
- AI-generated narration
- Optional background music

Videos are rendered at 1080x1920 resolution for vertical short-form platforms.


AUTOMATED VIDEO UPLOAD

Once rendering is complete, videos are uploaded automatically through the YouTube Data API.

The upload system includes:

- OAuth authentication
- automated upload requests
- metadata assignment
- tags and categories


CONTROLLER SCHEDULER

The controller script is responsible for orchestrating all pipelines.

Key features include:

- automated job scheduling
- configurable execution intervals
- staggered job offsets
- parallel job execution using subprocesses

This allows the system to continuously run and produce content at defined intervals.


TECHNOLOGIES USED

Programming Language
Python

Core Libraries
MoviePy
NumPy
Pillow
asyncio
requests

Machine Learning Tools
Whisper speech recognition
Edge TTS neural speech synthesis

APIs
YouTube Data API
Financial Modeling Prep API

External Tools
FFmpeg
ImageMagick


EXAMPLE PIPELINE EXECUTION

Script Generation
        |
        v
AI Voice Generation
        |
        v
Speech Transcription
        |
        v
Caption Timing Extraction
        |
        v
Video Composition
        |
        v
Video Rendering
        |
        v
Automated Upload


PROJECT GOALS

The project was created to explore several areas of software engineering including:

automation systems
media generation pipelines
AI speech synthesis
speech transcription
API integration
automated publishing workflows
multi-process job scheduling


FUTURE IMPROVEMENTS

Possible future expansions include:

adding additional content niches
analytics-driven content optimization
performance tracking for generated videos


AUTHOR

Independent software project developed to explore automation systems, AI media generation, and large-scale content pipelines.
