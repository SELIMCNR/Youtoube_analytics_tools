
#API_KEY = "AIzaSyAHkKMg1yh9SM7YM1jK3f-CTgyOEbFdZOA"
# 9PCvS5nphhM
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

API_KEY = "your_apıkey"
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

def get_video_stats(video_id):
    try:
        request = youtube.videos().list(
            part="statistics, snippet, contentDetails",
            id=video_id
        )
        response = request.execute()
        
        stats = response["items"][0]["statistics"]
        snippet = response["items"][0]["snippet"]
        content_details = response["items"][0]["contentDetails"]

        # Kanal bilgilerini alma
        channel_id = snippet["channelId"]
        channel_request = youtube.channels().list(
            part="statistics, snippet",
            id=channel_id
        )
        channel_response = channel_request.execute()
        channel_info = channel_response["items"][0]

        # Kanalın en popüler 5 videosunu bulma
        popular_videos_request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            order="viewCount",
            type="video",
            maxResults=5
        )
        popular_videos_response = popular_videos_request.execute()
        popular_videos = [video["snippet"]["title"] for video in popular_videos_response["items"]]

        # SEO Optimizasyonu - Video başlığını analiz etme
        keywords = snippet["title"].split()
        seo_score = len(keywords) * 5  # Basit bir SEO puanı hesaplama mantığı

        # Etkileşim oranı hesaplama
        view_count = int(stats.get("viewCount", 0))
        like_count = int(stats.get("likeCount", 0))
        comment_count = int(stats.get("commentCount", 0))
        engagement_rate = (like_count + comment_count) / view_count * 100 if view_count > 0 else 0

        # Reklam stratejisi - Para kazanma analizi
        monetization_ready = "Evet" if int(channel_info["statistics"].get("subscriberCount", 0)) > 1000 and view_count > 4000 else "Hayır"

        video_data = {
            "Video Başlığı": snippet["title"],
            "Yayın Tarihi": snippet["publishedAt"],
            "İzlenme Sayısı": view_count,
            "Beğeni Sayısı": like_count,
            "Yorum Sayısı": comment_count,
            "Etkileşim Oranı (%)": round(engagement_rate, 2),
            "Kanal Adı": channel_info["snippet"]["title"],
            "Kanal Abone Sayısı": channel_info["statistics"].get("subscriberCount", "Veri Yok"),
            "Kanalın En Popüler Videoları": popular_videos,
            "SEO Puanı": seo_score,
            "Para Kazanmaya Uygun mu?": monetization_ready
        }
        
        return video_data
    
    except googleapiclient.errors.HttpError as e:
        print(f"Hata oluştu: {e}")
        return None

video_id = "your_Video_id"
video_stats = get_video_stats(video_id)

if video_stats:
    df = pd.DataFrame([video_stats])
    df.to_csv("video_istatistikleri_gelistirilmis.csv", index=False)
    print("CSV dosyası oluşturuldu: video_istatistikleri_gelistirilmis.csv")
    print(df)