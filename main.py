import cv2
import numpy as np
from deepface import DeepFace
import os
import time
from datetime import datetime
import sys
import webbrowser
from googleapiclient.discovery import build
import random

class YouTubeMoodPlaylistAI:
    def __init__(self):
        self.youtube = None
        self.current_mood = None
        self.mood_history = []
        
        # YouTube API settings (replace with your own API key)
        # GÜVENLIK UYARISI: Bu bilgiler environment variables'da saklanmalı
        self.YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_API_HERE")
        
        # Mood to search keywords mapping
        self.mood_keywords = {
            'happy': [
                'happy songs', 'upbeat music', 'feel good songs', 'pop music',
                'dance music', 'energetic songs', 'positive vibes', 'cheerful music'
            ],
            'sad': [
                'sad songs', 'emotional music', 'heartbreak songs', 'melancholy music',
                'acoustic ballads', 'slow songs', 'indie sad', 'piano ballads'
            ],
            'angry': [
                'rock music', 'metal songs', 'aggressive music', 'hard rock',
                'punk rock', 'intense music', 'powerful songs', 'heavy metal'
            ],
            'surprise': [
                'unique music', 'experimental songs', 'world music', 'jazz fusion',
                'electronic music', 'indie music', 'alternative songs', 'ambient music'
            ],
            'fear': [
                'dark ambient', 'atmospheric music', 'cinematic music', 'suspense music',
                'classical horror', 'drone music', 'minimal music', 'eerie sounds'
            ],
            'disgust': [
                'alternative rock', 'grunge music', 'industrial music', 'noise music',
                'experimental rock', 'post punk', 'dark wave', 'gothic music'
            ],
            'neutral': [
                'chill music', 'background music', 'lo-fi hip hop', 'study music',
                'ambient music', 'instrumental music', 'relaxing songs', 'indie pop'
            ]
        }
        
        # Genre-specific search terms for better results
        self.mood_genres = {
            'happy': ['pop', 'disco', 'funk', 'reggae', 'afrobeat'],
            'sad': ['indie', 'folk', 'blues', 'soul', 'singer-songwriter'],
            'angry': ['rock', 'metal', 'punk', 'hardcore', 'nu-metal'],
            'surprise': ['jazz', 'fusion', 'world', 'experimental', 'electronic'],
            'fear': ['ambient', 'dark ambient', 'classical', 'soundtrack', 'drone'],
            'disgust': ['industrial', 'noise', 'post-punk', 'gothic', 'darkwave'],
            'neutral': ['chillout', 'downtempo', 'lo-fi', 'acoustic', 'indie']
        }
    
    def setup_youtube(self):
        """Initialize YouTube API connection"""
        try:
            if not self.YOUTUBE_API_KEY or self.YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY_HERE":
                print("❌ YouTube API anahtarı eksik!")
                print("💡 YouTube Data API v3 anahtarı alın:")
                print("   1. Google Cloud Console'a gidin")
                print("   2. Yeni proje oluşturun")
                print("   3. YouTube Data API v3'ü etkinleştirin")
                print("   4. API anahtarı oluşturun")
                print("   5. YOUTUBE_API_KEY environment variable olarak ayarlayın")
                return False
            
            self.youtube = build('youtube', 'v3', developerKey=self.YOUTUBE_API_KEY)
            
            # Test the connection
            test_response = self.youtube.search().list(
                q='test',
                part='snippet',
                maxResults=1,
                type='video'
            ).execute()
            
            print("✅ YouTube API'ye başarıyla bağlandı!")
            return True
            
        except Exception as e:
            print(f"❌ YouTube API bağlantı hatası: {str(e)}")
            if "quotaExceeded" in str(e):
                print("⚠️ YouTube API quota'nız doldu. Yarın tekrar deneyin.")
            elif "keyInvalid" in str(e):
                print("⚠️ YouTube API anahtarınız geçersiz.")
            return False
    
    def detect_emotion_from_camera(self, duration=5):
        """Detect emotion from webcam"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Kamera açılamadı! Kamera bağlı mı kontrol edin.")
            return 'neutral'
        
        # Kamera ayarları
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        emotions_detected = []
        print(f"📷 Duygu tespiti başladı... {duration} saniye boyunca kameraya bakın!")
        
        start_time = time.time()
        frame_count = 0
        
        try:
            while time.time() - start_time < duration:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Kamera frame'i okunamadı!")
                    break
                
                frame_count += 1
                
                # Her 10 frame'de bir analiz yap (performans için)
                if frame_count % 10 == 0:
                    try:
                        # Frame'i RGB'ye çevir (DeepFace RGB bekler)
                        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        
                        result = DeepFace.analyze(
                            rgb_frame, 
                            actions=['emotion'], 
                            enforce_detection=False,
                            silent=True
                        )
                        
                        # DeepFace'in yeni versiyonlarında result bir liste döner
                        if isinstance(result, list):
                            result = result[0]
                        
                        dominant_emotion = max(result['emotion'], key=result['emotion'].get)
                        emotions_detected.append(dominant_emotion)
                        
                        # Display emotion on frame
                        cv2.putText(frame, f"Duygu: {dominant_emotion.title()}", 
                                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                    except Exception as emotion_error:
                        print(f"⚠️ Duygu analiz hatası: {emotion_error}")
                        emotions_detected.append('neutral')
                
                # Show remaining time
                remaining = int(duration - (time.time() - start_time))
                cv2.putText(frame, f"Kalan sure: {remaining}s", 
                            (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                
                cv2.imshow('Duygu Tespiti (ESC ile cik)', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC key
                    break
                    
        except KeyboardInterrupt:
            print("\n⚠️ Kullanıcı tarafından durduruldu.")
        finally:
            cap.release()
            cv2.destroyAllWindows()
        
        if emotions_detected:
            self.current_mood = max(set(emotions_detected), key=emotions_detected.count)
            confidence = emotions_detected.count(self.current_mood) / len(emotions_detected)
            self.mood_history.append({
                'mood': self.current_mood,
                'timestamp': datetime.now().isoformat(),
                'confidence': confidence
            })
            print(f"🎭 Tespit edilen duygu: {self.current_mood.title()} (Güven: {confidence:.1%})")
            return self.current_mood
        
        print("⚠️ Duygu tespit edilemedi, 'neutral' kullanılıyor.")
        return 'neutral'
    
    def search_youtube_songs(self, mood, limit=20):
        """Search YouTube for songs based on mood"""
        if not self.youtube:
            print("❌ YouTube API bağlantısı yok!")
            return []
        
        try:
            # Get search keywords for this mood
            keywords = self.mood_keywords.get(mood, ['music'])
            genres = self.mood_genres.get(mood, ['music'])
            
            all_videos = []
            search_terms = keywords + [f"{genre} music" for genre in genres]
            
            # Perform multiple searches to get diverse results
            for search_term in search_terms[:5]:  # Limit API calls
                try:
                    print(f"🔍 Arama yapılıyor: '{search_term}'")
                    
                    search_response = self.youtube.search().list(
                        q=search_term,
                        part='snippet',
                        maxResults=min(10, limit // len(search_terms[:5]) + 2),
                        type='video',
                        videoCategoryId='10',  # Music category
                        order='relevance',
                        regionCode='TR'  # Turkish region for better local results
                    ).execute()
                    
                    for item in search_response.get('items', []):
                        video_info = {
                            'title': item['snippet']['title'],
                            'channel': item['snippet']['channelTitle'],
                            'video_id': item['id']['videoId'],
                            'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                            'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                            'description': item['snippet']['description'][:100] + '...',
                            'published': item['snippet']['publishedAt'][:10]
                        }
                        all_videos.append(video_info)
                    
                    time.sleep(0.1)  # Rate limiting
                    
                except Exception as search_error:
                    print(f"⚠️ Arama hatası '{search_term}': {search_error}")
                    continue
            
            # Remove duplicates and shuffle
            unique_videos = []
            seen_ids = set()
            for video in all_videos:
                if video['video_id'] not in seen_ids:
                    unique_videos.append(video)
                    seen_ids.add(video['video_id'])
            
            # Shuffle and limit results
            random.shuffle(unique_videos)
            result = unique_videos[:limit]
            
            print(f"✅ {len(result)} video bulundu!")
            return result
            
        except Exception as e:
            print(f"❌ YouTube arama hatası: {str(e)}")
            if "quotaExceeded" in str(e):
                print("⚠️ YouTube API quota'nız doldu.")
            return []
    
    def create_playlist_file(self, mood, videos):
        """Create a local playlist file with YouTube links"""
        if not videos:
            print("❌ Playlist oluşturulamıyor: Video bulunamadı!")
            return None
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"playlist_{mood}_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"🎵 {mood.title()} Ruh Hali Playlist\n")
                f.write(f"📅 Oluşturulma: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
                f.write("=" * 60 + "\n\n")
                
                for i, video in enumerate(videos, 1):
                    f.write(f"{i:2d}. {video['title']}\n")
                    f.write(f"    Kanal: {video['channel']}\n")
                    f.write(f"    Link: {video['url']}\n")
                    f.write(f"    Tarih: {video['published']}\n\n")
                
                f.write("\n" + "=" * 60 + "\n")
                f.write("💡 İpucu: Linklere tıklayarak şarkıları YouTube'da açabilirsiniz!\n")
            
            print(f"✅ Playlist dosyası oluşturuldu: {filename}")
            print(f"📊 {len(videos)} video eklendi")
            
            return filename
            
        except Exception as e:
            print(f"❌ Playlist dosyası oluşturma hatası: {str(e)}")
            return None
    
    def play_youtube_playlist(self, videos, auto_play=False):
        """Open YouTube videos in browser"""
        if not videos:
            print("❌ Çalınacak video yok!")
            return
        
        print(f"\n🎵 {len(videos)} video bulundu!")
        print("\nPlaylist:")
        print("-" * 60)
        
        for i, video in enumerate(videos[:10], 1):  # Show first 10
            print(f"{i:2d}. {video['title'][:50]}...")
            print(f"    {video['channel']}")
        
        if len(videos) > 10:
            print(f"    ... ve {len(videos) - 10} video daha")
        
        print(f"\nSeçenekler:")
        print("1. İlk videoyu tarayıcıda aç")
        print("2. Playlist'i rastgele çal")
        print("3. Belirli bir videoyu seç")
        print("4. Tüm linkleri göster")
        print("5. Playlist dosyası oluştur")
        print("6. Geri dön")
        
        try:
            choice = input("\nSeçiminiz (1-6): ").strip()
            
            if choice == '1':
                print(f"🌐 Açılıyor: {videos[0]['title']}")
                webbrowser.open(videos[0]['url'])
                
            elif choice == '2':
                random_video = random.choice(videos)
                print(f"🎲 Rastgele seçim: {random_video['title']}")
                webbrowser.open(random_video['url'])
                
            elif choice == '3':
                print("\nMevcut videolar:")
                for i, video in enumerate(videos[:20], 1):  # Show first 20
                    print(f"{i:2d}. {video['title'][:60]}")
                
                try:
                    video_idx = int(input(f"\nVideo seçin (1-{min(20, len(videos))}): ")) - 1
                    if 0 <= video_idx < len(videos):
                        selected = videos[video_idx]
                        print(f"🌐 Açılıyor: {selected['title']}")
                        webbrowser.open(selected['url'])
                    else:
                        print("❌ Geçersiz seçim!")
                except ValueError:
                    print("❌ Lütfen geçerli bir sayı girin!")
                    
            elif choice == '4':
                print("\n🔗 Tüm video linkleri:")
                print("-" * 80)
                for i, video in enumerate(videos, 1):
                    print(f"{i:2d}. {video['title']}")
                    print(f"    {video['url']}")
                    print()
                    
            elif choice == '5':
                return self.create_playlist_file(self.current_mood or 'mixed', videos)
                
            elif choice == '6':
                return
            else:
                print("❌ Geçersiz seçim!")
                
        except KeyboardInterrupt:
            print("\n⚠️ İşlem iptal edildi.")
    
    def show_mood_stats(self):
        """Show mood history"""
        if not self.mood_history:
            print("📊 Henüz ruh hali geçmişi yok!")
            return
        
        print("\n📊 RUH HALİ GEÇMİŞİ:")
        print("-" * 60)
        for entry in self.mood_history[-10:]:  # Son 10 kayıt
            timestamp = entry['timestamp'][:19].replace('T', ' ')
            mood = entry['mood'].title()
            confidence = entry['confidence']
            print(f"{timestamp} | {mood:>10} | Güven: {confidence:.1%}")
        
        # İstatistikler
        if len(self.mood_history) > 1:
            moods = [entry['mood'] for entry in self.mood_history]
            most_common = max(set(moods), key=moods.count)
            print(f"\n📈 En yaygın ruh hali: {most_common.title()}")
    
    def test_youtube_api(self):
        """Test YouTube API functionality"""
        if not self.youtube:
            print("❌ YouTube API bağlantısı yok!")
            return False
        
        try:
            print("🧪 YouTube API testleri başlatılıyor...")
            
            # Test 1: Simple search
            test_response = self.youtube.search().list(
                q='music',
                part='snippet',
                maxResults=3,
                type='video'
            ).execute()
            
            print(f"✅ Test 1 - Basit arama: {len(test_response.get('items', []))} sonuç")
            
            # Test 2: Category search
            category_response = self.youtube.search().list(
                q='pop music',
                part='snippet',
                maxResults=3,
                type='video',
                videoCategoryId='10'
            ).execute()
            
            print(f"✅ Test 2 - Kategori araması: {len(category_response.get('items', []))} sonuç")
            
            # Show sample results
            if test_response.get('items'):
                print("\n🎵 Örnek sonuçlar:")
                for i, item in enumerate(test_response['items'][:3], 1):
                    title = item['snippet']['title'][:50]
                    channel = item['snippet']['channelTitle']
                    print(f"   {i}. {title}... - {channel}")
            
            print("🎉 Tüm testler başarılı!")
            return True
            
        except Exception as e:
            print(f"❌ API Test hatası: {e}")
            return False
    
    def run(self):
        """Main program loop"""
        print("🎵 YOUTUBE RUH HALİNE GÖRE MÜZİK ÖNERİCİSİ 🎵")
        print("=" * 55)
        
        if not self.setup_youtube():
            print("❌ YouTube API'ye bağlanılamadı!")
            print("💡 API anahtarınızı kontrol edin ve tekrar deneyin.")
            return
        
        while True:
            try:
                print("\n🎯 Seçenekler:")
                print("1. Kamera ile ruh halini tespit et ve müzik öner")
                print("2. Ruh halini manuel seç")
                print("3. Ruh hali geçmişini göster")
                print("4. YouTube API testleri çalıştır")
                print("5. Çıkış")
                
                choice = input("\nSeçiminiz (1-5): ").strip()
                
                if choice == '1':
                    print("\n📷 Kamera başlatılıyor...")
                    mood = self.detect_emotion_from_camera()
                    print(f"🎭 Tespit edilen ruh hali: {mood.title()}")
                    
                    print("🔍 YouTube'da müzik aranıyor...")
                    videos = self.search_youtube_songs(mood)
                    
                    if videos:
                        self.play_youtube_playlist(videos)
                    else:
                        print("❌ Video bulunamadı!")
                
                elif choice == '2':
                    print("\n🎭 Mevcut ruh halleri:")
                    moods = list(self.mood_keywords.keys())
                    for i, mood in enumerate(moods, 1):
                        print(f"   {i}. {mood.title()}")
                    
                    try:
                        idx = int(input("\nRuh hali seçin (1-{}): ".format(len(moods)))) - 1
                        if 0 <= idx < len(moods):
                            mood = moods[idx]
                            self.current_mood = mood
                            print(f"🔍 {mood.title()} için YouTube'da aranıyor...")
                            videos = self.search_youtube_songs(mood)
                            if videos:
                                self.play_youtube_playlist(videos)
                            else:
                                print("❌ Video bulunamadı!")
                        else:
                            print("❌ Geçersiz seçim!")
                    except ValueError:
                        print("❌ Lütfen geçerli bir sayı girin!")
                
                elif choice == '3':
                    self.show_mood_stats()
                
                elif choice == '4':
                    self.test_youtube_api()
                
                elif choice == '5':
                    print("👋 Görüşmek üzere!")
                    break
                
                else:
                    print("❌ Geçersiz seçim! Lütfen 1-5 arası bir sayı girin.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Program sonlandırıldı!")
                break
            except Exception as e:
                print(f"\n❌ Beklenmeyen hata: {e}")
                print("Program devam ediyor...")

if __name__ == "__main__":
    try:
        app = YouTubeMoodPlaylistAI()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Program kapatıldı!")
    except Exception as e:
        print(f"❌ Program başlatma hatası: {e}")
        sys.exit(1)