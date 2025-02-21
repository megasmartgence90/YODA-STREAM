import yaml
import requests
import json
import re
import schedule
import time

def load_config(config_file="config.yml"):
    """
    YAML konfiqurasiya faylını yükləyir.
    """
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Konfiqurasiya faylı yüklənə bilmədi: {e}")
        return None

def get_new_token(token_url, headers):
    """
    Yeni token almaq üçün funksiya.
    """
    try:
        response = requests.get(token_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        token = data.get("token")
        if not token:
            raise ValueError("Token alına bilmədi!")
        return token
    except Exception as e:
        print(f"Token almaq mümkün olmadı: {e}")
        return None

def update_channel_sources(channels, new_token):
    """
    Kanal mənbələrini (channelSource) yenilənmiş token ilə yeniləyir.
    """
    updated_channels = []
    for channel in channels:
        source = channel.get("channelSource")
        if source and "yodacdn.net" in source:
            base_url = re.sub(r"\?.*$", "", source)
            updated_source = f"{base_url}?token={new_token}"
            channel["channelSource"] = updated_source
        updated_channels.append(channel)
    return updated_channels

def save_to_json(data, output_file):
    """
    Yenilənmiş kanal məlumatlarını JSON faylına saxlamaq.
    """
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Yenilənmiş kanal məlumatları '{output_file}' faylına saxlanıldı.")
    except Exception as e:
        print(f"Fayl saxlanılması mümkün olmadı: {e}")

def manual_refresh():
    """
    Manual yeniləmə prosesi.
    """
    print("Manual yeniləmə başladı...")
    
    # Konfiqurasiya faylını yüklə
    config = load_config()
    if not config:
        print("Konfiqurasiya yüklənmədi, proses dayandırıldı.")
        return

    # Token almaq üçün məlumatları əldə et
    token_url = config["token"]["url"]
    headers = config["token"]["headers"]

    # Yeni token almaq
    new_token = get_new_token(token_url, headers)
    if not new_token:
        print("Token alına bilmədi, proses dayandırıldı.")
        return

    print(f"Yeni token alındı: {new_token}")

    # Kanal mənbələrini yeniləmək
    channels = config["channels"]
    updated_channels = update_channel_sources(channels, new_token)

    # Yenilənmiş kanal məlumatlarını JSON faylına saxlamaq
    output_file = config["output_file"]
    save_to_json(updated_channels, output_file)

    print("Manual yeniləmə tamamlandı.")

def auto_refresh_job():
    """
    Avtomatik yeniləmə işi (əgər aktivdirsə).
    """
    print("Avtomatik yeniləmə başladı...")
    manual_refresh()

def main():
    # Konfiqurasiyadan zamanlama və manual yenilənmə parametrlərini əldə et
    config = load_config()
    if not config:
        print("Konfiqurasiya yüklənmədi, proses dayandırıldı.")
        return

    auto_refresh = config["schedule"].get("auto_refresh", False)
    interval_hours = config["schedule"].get("interval_hours", 1)

    if auto_refresh:
        # Avtomatik yenilənməni planlaşdır
        schedule.every(interval_hours).hours.do(auto_refresh_job)
        print(f"Avtomatik yeniləmə hər {interval_hours} saatda bir aktiv edildi.")
    else:
        print("Avtomatik yenilənmə deaktiv edilib. Manual yenilənmə üçün 'manual_refresh()' funksiyasını çağırın.")

    # Daimi döngü (avtomatik yenilənmə üçün)
    while auto_refresh:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
