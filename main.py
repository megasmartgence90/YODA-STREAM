import os
import json
from tqdm import tqdm

def main():
    try:
        # config.json faylını oxuyun
        with open('config.json', 'r') as f:
            sites = json.load(f)

        for site in sites:
            # 'slug' açarının mövcudluğunu yoxlayın
            if "slug" not in site:
                print(f"Xəta: '{site.get('name', 'Naməlum')}' saytı üçün 'slug' açarı tapılmadı.")
                continue  # Bu saytı atlayıb növbəti sayta keçin

            # Sayt üçün yol yaradın
            site_path = os.path.join(os.getcwd(), site["slug"])
            print(f"İşlənilir: {site['name']} - Yol: {site_path}")

            # 'channels' açarının mövcudluğunu yoxlayın
            channels = site.get("channels", [])
            if not channels:
                print(f"Xəbərdarlıq: '{site['name']}' saytında kanal yoxdur.")
                continue  # Kanal yoxdursa, bu saytı atlayın

            # Kanalları işləyin
            for channel in tqdm(channels):
                print(f"Kanal: {channel['name']} - URL: {channel['url']}")

    except FileNotFoundError:
        print("Xəta: 'config.json' faylı tapılmadı.")
    except json.JSONDecodeError:
        print("Xəta: 'config.json' faylının formatı düzgün deyil.")
    except Exception as e:
        print(f"Başqa bir xəta baş verdi: {e}")

if __name__ == "__main__":
    main()
