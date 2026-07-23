import os
CHANNEL_ID = "UC7wHmjY4RNruABZ9An1crBA"
PLAYLIST_NAME = "Radar TV"
LOGO_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/Logo%20RadarTV%203000x3000.jpg"

WEB_TV_URL = "https://video01.logicahost.com.br/fcvtv/fcvtv/playlist.m3u8"

YOUTUBE_LIVE_URL = f"https://www.youtube.com/embed/live_stream?channel={CHANNEL_ID}"

def create_m3u():
    m3u_content = '#EXTM3U\n'
    
    
    print("Gerando canal com link dinâmico de Live do YouTube...")
    m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} [AO VIVO]\n'
    m3u_content += f'{YOUTUBE_LIVE_URL}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Lista M3U atualizada com sucesso!")

if __name__ == "__main__":
    create_m3u()
