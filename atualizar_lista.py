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
    """Captura os fluxos de vídeo DIRETO (.mp4/.m3u8) da playlist"""
    try:
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        # Coleta título e link direto do fluxo de mídia de uma vez só
        cmd = ["yt-dlp", "-g", "-f", "best", "--print", "%(title)s|%(url)s", url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        videos = []
        if result.returncode == 0 and result.stdout:
            lines = result.stdout.strip().split("\n")
            # Divide as linhas em blocos de Título | Link Direto de Fluxo
            for line in lines:
                if "|" in line:
                    title, direct_url = line.split("|", 1)
                    if "http" in direct_url:
                        videos.append({"title": title, "url": direct_url})
        return videos
    except:
        return []

def create_m3u():
    # Adicionamos uma propriedade global para o player fingir que é um navegador (Safari no Mac)
    # Isso evita que o YouTube bloqueie o app de IPTV por segurança
    m3u_content = '#EXTM3U x-tvg-url=""\n#EXTVLCOPT:http-user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"\n'
    
    # 1. Tenta buscar se há uma live rolando agora
    live_url = get_live_m3u8(CHANNEL_ID)
    
    if live_url:
        print("Sinal Aberto! Cortando a programação para a Live Ao Vivo.")
        m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{PLAYLIST_NAME}" tvg-logo="" group-title="Radar TV Ao Vivo", [AO VIVO] {PLAYLIST_NAME}\n'
        m3u_content += f'#EXTVLCOPT:http-user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"\n'
        m3u_content += f'{live_url}\n'
    else:
        print("Canal Offline. Montando grade com os fluxos da playlist do Ruralzão.")
        # 2. Se não tiver live, monta a lista com os links diretos extraídos
        videos = get_playlist_m3u8(PLAYLIST_ID)
        
        if videos:
            for video in videos:
                m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{video["title"]}" tvg-logo="" group-title="Ruralzão 2026 - Gravados", {video["title"]}\n'
                m3u_content += f'#EXTVLCOPT:http-user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"\n'
                m3u_content += f'{video["url"]}\n'
        else:
            # Fallback seguro
            m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{PLAYLIST_NAME}" tvg-logo="" group-title="Radar TV", {PLAYLIST_NAME}\n'
            m3u_content += f'https://www.youtube.com/playlist?list={PLAYLIST_ID}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Nova estrutura calibrada salva com sucesso!")

if __name__ == "__main__":
    create_m3u()
