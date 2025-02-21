import requests
import json
import re

# Kanal konfiqurasiyası (sizin təqdim etdiyiniz JSON)
channel_config = [
    {
        "channelID": "aztv",
        "channelName": "AZTV",
        "channelSource": "https://str.yodacdn.net/aztv/video.m3u8",
        "channelProgramme": "https://azepg.ddns.net/aztv/15_days_archive__aztv_desc.xml",
        "channelIconC": "/logos/aztv.svg",
        "channelIconM": "/logos/aztv.svg",
    },
    # Qalan kanallar burada...
]

# Token almaq üçün URL
TOKEN_URL = "https://yoda.az/api/get_token"
# Token yeniləmək üçün header və ya digər parametrlər lazım ola bilər
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def get_new_token():
    """
    Yeni token almaq üçün funksiya.
    """
    try:
        response = requests.get(TOKEN_URL, headers=HEADERS)
        response.raise_for_status()  # Xəta olduqda istisna atır
        data = response.json()
        token = data.get("token")  # Tokeni JSON-dan çıxarır
        if not token:
            raise ValueError("Token alına bilmədi!")
        return token
    except Exception as e:
        print(f"Token almaq mümkün olmadı: {e}")
        return None

def update_channel_sources(channel_config, new_token):
    """
    Kanal mənbələrini (channelSource) yenilənmiş token ilə yeniləyir.
    """
    updated_channels = []
    for channel in channel_config:
        source = channel.get("channelSource")
        if source and "yodacdn.net" in source:
            # Mənbəni yenilənmiş token ilə yenidən qur
            base_url = re.sub(r"\?.*$", "", source)  # Mövcud query string-i sil
            updated_source = f"{base_url}?token={new_token}"
            channel["channelSource"] = updated_source
        updated_channels.append(channel)
    return updated_channels

def save_to_json(data, filename="updated_channels.json"):
    """
    Yenilənmiş kanal məlumatlarını JSON faylına saxlamaq.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Yenilənmiş kanal məlumatları '{filename}' faylına saxlanıldı.")
    except Exception as e:
        print(f"Fayl saxlanılması mümkün olmadı: {e}")

def main():
    # Yeni token almaq
    new_token = get_new_token()
    if not new_token:
        print("Token alına bilmədi, proses dayandırıldı.")
        return

    print(f"Yeni token alındı: {new_token}")

    # Kanal mənbələrini yeniləmək
    updated_channels = update_channel_sources(channel_config, new_token)

    # Yenilənmiş kanal məlumatlarını JSON faylına saxlamaq
    save_to_json(updated_channels)

if __name__ == "__main__":
    main()
