import os
import subprocess

# Configurações do seu canal e da playlist do Ruralzão
CHANNEL_ID = "UC7wHmjY4RNruABZ9An1crBA"
PLAYLIST_ID = "PLzfuSmZBMwIoLYSVMxQhgjDR3yCpBpRbV"
PLAYLIST_NAME = "Radar TV"
LOGO_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/Logo%20RadarTV%203000x3000.jpg"

def get_stream_url(url):
    """Extrai o link direto do fluxo de vídeo usando o yt-dlp"""
    try:
        # Pega o link direto da melhor qualidade disponível
        cmd = ["yt-dlp", "-g", "-f", "best", url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except:
        return None

def create_m3u():
    m3u_content = '#EXTM3U\n'
    
    # 1. Tenta pegar o link da Live
    live_url = get_stream_url(f"https://www.youtube.com/channel/{CHANNEL_ID}/live")
    
    if live_url:
        print("Sinal Ao Vivo detectado!")
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} [AO VIVO]\n'
        m3u_content += f'{live_url}\n'
    else:
        print("Canal Offline. Pegando vídeos da playlist...")
        # Pega os 5 vídeos mais recentes da playlist
        cmd = ["yt-dlp", "--flat-playlist", "--print", "%(title)s|%(id)s", "--playlist-items", "1-5", f"https://www.youtube.com/playlist?list={PLAYLIST_ID}"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout:
            for line in result.stdout.strip().split("\n"):
                if "|" in line:
                    title, vid = line.split("|")
                    stream = get_stream_url(f"https://www.youtube.com/watch?v={vid}")
                    if stream:
                        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{title}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {title}\n'
                        m3u_content += f'{stream}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Lista gerada com links diretos!")

if __name__ == "__main__":
    create_m3u()
