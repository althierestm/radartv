import os
import subprocess

# Configurações do seu canal e da playlist do Ruralzão
CHANNEL_ID = "UC7wHmjY4RNruABZ9An1crBA"
PLAYLIST_ID = "PLzfuSmZBMwIoLYSVMxQhgjDR3yCpBpRbV"
PLAYLIST_NAME = "Radar TV MG - Ruralzão 2026"

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

def get_playlist_m3u8(playlist_id):
    """Captura os fluxos de vídeo diretos da playlist quando a live está offline"""
    try:
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        cmd = ["yt-dlp", "--flat-playlist", "--print", "%(title)s|%(id)s", url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        videos = []
        if result.returncode == 0 and result.stdout:
            lines = result.stdout.strip().split("\n")
            for line in lines:
                if "|" in line:
                    title, video_id = line.split("|", 1)
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    videos.append({"title": title, "url": video_url})
        return videos
    except:
        return []

def create_m3u():
    m3u_content = '#EXTM3U\n'
    
    # 1. Tenta buscar se há uma live rolando agora
    live_url = get_live_m3u8(CHANNEL_ID)
    
    if live_url:
        print("Sinal Aberto! Cortando a programação para a Live Ao Vivo.")
        m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{PLAYLIST_NAME}" tvg-logo="" group-title="Radar TV Ao Vivo", [AO VIVO] {PLAYLIST_NAME}\n'
        m3u_content += f'{live_url}\n'
    else:
        print("Canal Offline. Montando grade com a playlist do Ruralzão.")
        # 2. Se não tiver live, monta a lista com os vídeos salvos da playlist
        videos = get_playlist_m3u8(PLAYLIST_ID)
        
        if videos:
            for idx, video in enumerate(videos, start=1):
                m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{video["title"]}" tvg-logo="" group-title="Ruralzão 2026 - Gravados", {video["title"]}\n'
                m3u_content += f'{video["url"]}\n'
        else:
            m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{PLAYLIST_NAME}" tvg-logo="" group-title="Radar TV", {PLAYLIST_NAME}\n'
            m3u_content += f'https://www.youtube.com/playlist?list={PLAYLIST_ID}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Nova estrutura de lista salva com sucesso!")

if __name__ == "__main__":
    create_m3u()
