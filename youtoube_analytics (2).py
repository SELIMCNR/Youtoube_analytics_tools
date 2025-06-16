import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import datetime

API_KEY = "your apı key"
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

# 📌 Otomatik Video Yükleme
def upload_video(video_file_path, title, description, category_id, tags):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=video_file_path
    )
    response = request.execute()
    print(f"🚀 {title} başarıyla yüklendi! Video ID: {response['id']}")

# 📌 İçerik Takvimi – Yayın Planı Oluşturma
def schedule_video_upload(video_title, upload_date):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    if upload_date > today:
        print(f"📅 {video_title} adlı video {upload_date} tarihinde yayınlanacak!")
    else:
        print(f"🚀 {video_title} hemen yayınlanmalı!")

# 📌 Kanal Büyüme Analizi – Abone Artışı Takibi
def get_channel_growth(channel_id):
    try:
        request = youtube.channels().list(
            part="statistics",
            id=channel_id
        )
        response = request.execute()
        
        if "items" not in response or len(response["items"]) == 0:
            print("⚠ Kanal bilgileri bulunamadı, kanal ID'yi kontrol et!")
            return None
        
        stats = response["items"][0]["statistics"]
        growth_data = {
            "Toplam Abone": stats.get("subscriberCount", "Veri Yok"),
            "Toplam İzlenme": stats.get("viewCount", "Veri Yok"),
            "Toplam Video Sayısı": stats.get("videoCount", "Veri Yok")
        }
        return growth_data
    
    except googleapiclient.errors.HttpError as e:
        print(f"API Hatası: {e}")
        return None
# 📌 Reklam & Gelir Analizi – Para Kazanma Stratejisi
def calculate_monetization(channel_id):
    stats = get_channel_growth(channel_id)
    if int(stats["Toplam Abone"]) >= 1000 and int(stats["Toplam İzlenme"]) >= 4000:
        monetization_status = "Evet, para kazanma aktif olabilir!"
    else:
        monetization_status = "Hayır, YouTube İş Ortağı Programı gereksinimleri karşılanmıyor."
    
    return monetization_status

# 📌 Video Analiz – Trendler, SEO ve Etkileşim
def get_video_stats(video_id):
    request = youtube.videos().list(
        part="statistics, snippet, contentDetails",
        id=video_id
    )
    response = request.execute()
    
    stats = response["items"][0]["statistics"]
    snippet = response["items"][0]["snippet"]

    # Etkileşim oranı hesaplama
    view_count = int(stats.get("viewCount", 0))
    like_count = int(stats.get("likeCount", 0))
    comment_count = int(stats.get("commentCount", 0))
    engagement_rate = (like_count + comment_count) / view_count * 100 if view_count > 0 else 0

    video_data = {
        "Video Başlığı": snippet["title"],
        "İzlenme Sayısı": view_count,
        "Beğeni Sayısı": like_count,
        "Yorum Sayısı": comment_count,
        "Etkileşim Oranı (%)": round(engagement_rate, 2)
    }

    return video_data

# 📌 İçerik Planı – Takvimde Yayınlanacak Videolar
video_list = [
    {"title": "Python ile YouTube Otomasyon", "upload_date": "2025-06-21"},
    {"title": "YouTube Kanal Büyütme Stratejileri", "upload_date": "2025-06-28"}
]

for video in video_list:
    schedule_video_upload(video["title"], video["upload_date"])

# 📌 Kanal ID ile Analiz
channel_id = "YOUR_CHANNEL_ID"
growth_stats = get_channel_growth(channel_id)
monetization_status = calculate_monetization(channel_id)

video_id = "9PCvS5nphhM"
video_stats = get_video_stats(video_id)

# 📌 Verileri CSV'ye Kaydetme
df = pd.DataFrame([video_stats])
df.to_csv("youtube_video_analiz.csv", index=False)

print("📊 Kanal Büyüme Verileri:", growth_stats)
print("💰 Para Kazanma Durumu:", monetization_status)
print("📊 CSV dosyası oluşturuldu: youtube_video_analiz.csv")