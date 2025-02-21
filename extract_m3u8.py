import yaml
import requests
import json
import os

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

def build_full_url(base_url, channel_path):
    """
    Qaynaq linkini və kanal yolunu birləşdirərək tam URL yaradır.
    """
    return f"{base_url}{channel_path}"

def save_to_json(data, output_file):
    """
    Yenilənmiş kanal məlumatlarını JSON faylına saxlamaq.
    Qovluğu yoxlayır və yoxdursa yaradır.
    """
    try:
        # Qovluğu yoxla və yarat
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            print(f"Qovluq yaradıldı: {output_dir}")

        # Faylı yaz
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

    # Qaynaq linkini əldə et
    base_url = "https://str.yodacdn.net"

    # Kanalları yenilə
    updated_channels = []
    for channel in config.get("channels", []):
        channel_name = channel.get("channelID")
        channel_path = f"/{channel_name}/index.m3u8"
        full_url = build_full_url(base_url, channel_path)

        # Kanal məlumatlarını yenilə
        channel["channelSource"] = full_url
        updated_channels.append(channel)

    # Yenilənmiş kanal məlumatlarını JSON faylına saxla
    output_file = config.get("output_file", "output/updated_channels.json")
    save_to_json(updated_channels, output_file)

    print("Manual yeniləmə tamamlandı.")

if __name__ == "__main__":
    manual_refresh()
