import os
import subprocess

# Configurações do seu canal e da playlist do Ruralzão
CHANNEL_ID = "UC7wHmjY4RNruABZ9An1crBA"
PLAYLIST_ID = "PLzfuSmZBMwIoLYSVMxQhgjDR3yCpBpRbV"
PLAYLIST_NAME = "Radar TV MG"

def get_live_m3u8(channel_id):
    """Tenta capturar o fluxo direto da live caso o canal esteja ativo"""
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
    
    # 1. Tenta buscar se há uma live rolando agora
    live_url = get_live_m3u8(CHANNEL_ID)
    
    if live_url:
        print("Sinal Aberto! Cortando a programação para a Live Ao Vivo.")
        m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{PLAYLIST_NAME}" tvg-logo="" group-title="Radar TV Ao Vivo", [AO VIVO] {PLAYLIST_NAME}\n'
        m3u_content += f'{live_url}\n'
    else:
        print("Canal Offline. Direcionando para a playlist do Ruralzão de forma compatível.")
        # Usamos o formato direto de incorporação de playlist que o IPTV aceita sem expirar IP
        playlist_stream = f"https://www.youtube.com/embed/videoseries?list={PLAYLIST_ID}"
        m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{PLAYLIST_NAME} - Ruralzão 2026" tvg-logo="" group-title="Ruralzão 2026 - Gravados", {PLAYLIST_NAME} - Ruralzão 2026\n'
        m3u_content += f'{playlist_stream}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Lista atualizada com sucesso!")

if __name__ == "__main__":
    create_m3u()
