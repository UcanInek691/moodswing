
# 🚀 YouTube Mood AI - Quick Setup Guide

This guide helps you set up the project step by step.

## ⚡ Quick Start (5 Minutes)

### 1. Check Python Installation
```bash
python --version
# Python 3.7+ required
```

### 2. Download the Project
```bash
git clone [project-url]
cd youtube-mood-ai
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Get YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/) → Create a new project
2. APIs & Services → Library → Search "YouTube Data API v3"
3. Enable it → Go to Credentials → Create API Key
4. Copy your API key

### 5. Set Environment Variable

**Windows (Cmd):**
```cmd
set YOUTUBE_API_KEY=YOUR_API_KEY_HERE
```

**Windows (PowerShell):**
```powershell
$env:YOUTUBE_API_KEY="YOUR_API_KEY_HERE"
```

**Linux/Mac:**
```bash
export YOUTUBE_API_KEY="YOUR_API_KEY_HERE"
```

### 6. Run the Program
```bash
python youtube_mood_ai.py
```

## 🎯 First Use Test

1. When the program starts, select "4" (API tests)
2. If the API connection is successful, select "1" (camera test)
3. Look at the camera for 5 seconds
4. Test the suggested music

## 🔧 Troubleshooting

### Problem: "No module named 'cv2'"
```bash
pip install opencv-python
```

### Problem: "No module named 'deepface'"
```bash
pip install deepface
pip install tensorflow
```

### Problem: "YouTube API key missing"
- Make sure the environment variable is set correctly
- Close and reopen your terminal/cmd
- Ensure the API key is inside quotes

### Problem: Camera not opening
- Check if another app is using the camera
- Check camera permissions (Windows 10/11)
- If using USB camera, check the connection

## 💡 Performance Tips

- **For slow computers**: Lower the camera resolution
- **For slow internet**: Limit the number of videos
- **For API limits**: Monitor daily usage

## 📞 Support

If you're having issues:
1. Try the solutions in this guide
2. Search in the GitHub Issues section
3. Open a new issue

🎵 **Setup complete! Enjoy!** 🎵
