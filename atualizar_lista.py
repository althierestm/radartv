import os
import subprocess

# Link direto da sua live que está rolando agora
LIVE_URL = "https://www.youtube.com/watch?v=F23k820MfEU"
PLAYLIST_NAME = "Radar TV"
LOGO_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/Logo%20RadarTV%203000x3000.jpg"

def get_live_m3u8(url):
    """Extrai o link .m3u8 puro direto da URL da transmissão"""
    try:
        cmd = ["yt-dlp", "-g", "-f", "best", url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and "manifest" in result.stdout:
            return result.stdout.strip()
        return None
    except:
        return None

def create_m3u():
    m3u_content = '#EXTM3U\n'
    
    # Captura o fluxo direto usando o link da transmissão do OBS
    live_url = get_live_m3u8(LIVE_URL)
    
    if live_url:
        print("Sinal Direto da Live capturado com sucesso!")
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} [AO VIVO]\n'
        m3u_content += f'{live_url}\n'
    else:
        print("Não foi possível extrair o fluxo. Gerando link reserva.")
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} (Fora do Ar)\n'
        m3u_content += f'https://raw.githubusercontent.com/althierestm/radartv/main/offline.mp4\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Lista atualizada com o link direto da transmissão!")

if __name__ == "__main__":
    create_m3u()
