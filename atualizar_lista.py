import os
import subprocess

# Configurações do canal Radar TV
CHANNEL_ID = "UC7wHmjY4RNruABZ9An1crBA"
PLAYLIST_NAME = "Radar TV"
LOGO_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/Logo%20RadarTV%203000x3000.jpg"

def get_live_m3u8(channel_id):
    """Extrai o link .m3u8 puro da transmissão ao vivo atual"""
    try:
        url = f"https://www.youtube.com/channel/{channel_id}/live"
        cmd = ["yt-dlp", "-g", "-f", "best", url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and "manifest" in result.stdout:
            return result.stdout.strip()
        return None
    except:
        return None

def create_m3u():
    m3u_content = '#EXTM3U\n'
    
    # Captura o link da live ativa agora
    live_url = get_live_m3u8(CHANNEL_ID)
    
    if live_url:
        print("Sinal Ao Vivo detectado com sucesso!")
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} [AO VIVO]\n'
        m3u_content += f'{live_url}\n'
    else:
        print("Canal Offline. Gerando link reserva padrão.")
        # Se estiver offline, gera um link limpo temporário para manter o canal ativo no app
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} (Fora do Ar)\n'
        m3u_content += f'https://raw.githubusercontent.com/althierestm/radartv/main/offline.mp4\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Lista atualizada com foco exclusivo na Live!")

if __name__ == "__main__":
    create_m3u()
