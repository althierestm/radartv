import os
import subprocess

# Configurações da Radar TV
CHANNEL_ID = "UC7wHmjY4RNruABZ9An1crBA"
PLAYLIST_NAME = "Radar TV"
LOGO_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/Logo%20RadarTV%203000x3000.jpg"

# Link da sua Web TV (Programação padrão / Reprises)
WEB_TV_URL = "https://video01.logicahost.com.br/fcvtv/fcvtv/playlist.m3u8"

def get_live_m3u8(channel_id):
    """
    Tenta capturar o link .m3u8 da transmissão ao vivo usando o yt-dlp.
    """
    try:
        url = f"https://www.youtube.com/channel/{channel_id}/live"
        cmd = ["yt-dlp", "-g", "-f", "best", url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0 and "manifest" in result.stdout:
            return result.stdout.strip()
        return None
    except:
        return None

def create_m3u():
    m3u_content = '#EXTM3U\n'
    
    print("Verificando se a Radar TV está Ao Vivo no YouTube...")
    live_url = get_live_m3u8(CHANNEL_ID)
    
    if live_url:
        # 🔴 SE ESTIVER AO VIVO: Corta para o sinal do OBS no YouTube
        print("🔴 AO VIVO DETECTADO! Cortando a programação para a Live.")
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} [AO VIVO]\n'
        m3u_content += f'{live_url}\n'
    else:
        # 📺 SE ESTIVER OFFLINE: Mantém o sinal da sua Web TV rodando
        print("📺 Canal Offline no YouTube. Transmitindo programação padrão...")
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME}\n'
        m3u_content += f'{WEB_TV_URL}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Lista M3U atualizada com sucesso!")

if __name__ == "__main__":
    create_m3u()
