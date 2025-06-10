🎵 YouTube Mood-Based Music Recommender AI

This project is an AI application that detects the user's mood through facial analysis using a webcam and recommends YouTube music videos accordingly.

🌟 Features

🎭 Emotion Detection
- Real-Time Analysis: Analyzes your facial expressions through webcam
- 7 Emotions Supported: Happy, sad, angry, surprised, fearful, disgusted, neutral
- High Accuracy: Uses DeepFace library for reliable detection
- Visual Feedback: Displays detected emotion on camera feed

🎵 Smart Music Recommendation
- Mood-Based Search: Custom music keywords for each emotion
- Multi-Search Strategy: Uses different genres and keywords for broad results
- YouTube API Integration: Uses official YouTube Data API v3
- Turkey-Centric: Optimized for Turkish music culture

📱 User-Friendly Interface
- Simple Navigation: Easy-to-use menu system
- Multiple Playback Options: Open first result, random pick, or manual selection
- Playlist Generation: Save results in .txt playlist files
- History Tracking: View mood history and emotion stats

🛠️ Setup

Requirements:
Python 3.7+
Webcam (USB or built-in)
YouTube Data API v3 key
Internet connection

1. Install Python Libraries
pip install opencv-python
pip install deepface
pip install google-api-python-client
pip install numpy

2. Get a YouTube API Key
1. Go to Google Cloud Console
2. Create a new project or select an existing one
3. Go to "APIs & Services" > "Library"
4. Search for "YouTube Data API v3" and enable it
5. Go to "Credentials" and click "Create Credentials" > "API Key"
6. Copy your API key

3. Set the API Key

Windows:
set YOUTUBE_API_KEY=your_api_key

Linux/Mac:
export YOUTUBE_API_KEY=your_api_key

Persistent Setting (Windows):
setx YOUTUBE_API_KEY "your_api_key"

Persistent Setting (Linux/Mac):
echo 'export YOUTUBE_API_KEY="your_api_key"' >> ~/.bashrc
source ~/.bashrc

4. Run the Program
python youtube_mood_ai.py

🎯 User Guide

Main Menu Options:
1. Detect Mood via Camera: Opens webcam and analyzes your face for 5 seconds. Press ESC to exit early. Automatically suggests music based on detected mood.
2. Select Mood Manually: Choose from 7 moods manually. Get music suggestions without using the camera.
3. Mood History: View your last 10 mood detections. See your most common emotion. Includes confidence scores and statistics.
4. YouTube API Tests: Test your API connection. Preview example results. Debug common API errors.

Playlist Options:
1. Open First Video: Opens the top result in your browser.
2. Random Video: Randomly selects a video from the list.
3. Manual Selection: Lists the first 20 videos and lets you pick one.
4. Show All Links: Displays all found video links in terminal.
5. Generate Playlist File: Creates a .txt playlist file. Named with timestamp and mood.

🎨 Supported Moods & Music Types

😊 Happy
Genres: Pop, disco, funk, reggae, afrobeat
Keywords: Happy songs, upbeat music, feel good songs

😢 Sad
Genres: Indie, folk, blues, soul, singer-songwriter
Keywords: Sad songs, emotional music, heartbreak songs

😠 Angry
Genres: Rock, metal, punk, hardcore, nu-metal
Keywords: Rock music, metal songs, aggressive music

😲 Surprise
Genres: Jazz, fusion, world, experimental, electronic
Keywords: Unique music, experimental songs, world music

😨 Fear
Genres: Ambient, dark ambient, classical, soundtrack, drone
Keywords: Dark ambient, atmospheric music, cinematic music

🤢 Disgust
Genres: Industrial, noise, post-punk, gothic, darkwave
Keywords: Alternative rock, grunge music, industrial music

😐 Neutral
Genres: Chillout, downtempo, lo-fi, acoustic, indie
Keywords: Chill music, background music, lo-fi hip hop

🔧 Troubleshooting

Common Errors & Fixes:

"Camera could not be opened"
Fix:
- Check webcam connection
- Ensure no other app is using the camera
- Verify camera permissions

"Missing YouTube API key"
Fix:
- Set YOUTUBE_API_KEY environment variable
- Verify that the key is correct
- Ensure YouTube Data API v3 is enabled

"quotaExceeded" Error
Fix:
- Your daily YouTube API quota is exceeded
- Try again tomorrow
- Use a different API key

"keyInvalid" Error
Fix:
- Double-check your API key
- Make sure it’s active in Google Cloud Console

"Emotion analysis error"
Fix:
- Make sure your face is clearly visible
- Improve lighting conditions
- Check webcam quality

Performance Optimization:

Faster Emotion Detection:
- Lower camera resolution (e.g., 640x480)
- Analyze fewer frames (e.g., every 15–20 frames)
- Reduce detection duration (e.g., to 3 seconds)

Lower API Usage:
- Limit search terms
- Reduce maxResults value
- Add caching mechanism

📊 Technical Details

Technologies Used:
- OpenCV: Camera access and image processing
- DeepFace: Face recognition and emotion detection
- YouTube Data API v3: Video search and metadata retrieval
- Google API Client: Communication with YouTube API

File Structure:
main.py                     # Main program file
playlist_[mood]_[date].txt  # Generated playlist files
README.md                   # This documentation
requirements.txt            # Python requirements

API Limits:
- Daily Quota: 10,000 units (free)
- Search Request: 100 units
- Video Details: 1 unit
- Recommended Usage: 50–100 searches per day

🔐 Security Notes

Important Security Tips:
- Never store your API key in source code
- Always use environment variables
- Never share your API key in public repositories
- Rotate your API key regularly

🤝 Contributing

To contribute:
1. Fork the repo
2. Create a feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add AmazingFeature')
4. Push to your branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

🐛 Bug Reporting

To report bugs:
- Open an issue
- Include error details and reproduction steps
- Share your system info
- Attach any relevant logs

🎉 Thanks

- Thanks to the DeepFace team for emotion detection
- Thanks to the OpenCV community for image processing tools
- Thanks to Google for YouTube API support
- And to all contributors!

Developer: mayaonthetrack
Version: 1.0
Last Updated: June 2025

🎵 Enjoy the music! 🎵
