import os
import subprocess

# Configurações do seu canal e da playlist do Ruralzão
CHANNEL_ID = "UC7wHmjY4RNruABZ9An1crBA"
PLAYLIST_ID = "PLzfuSmZBMwIoLYSVMxQhgjDR3yCpBpRbV"
PLAYLIST_NAME = "Radar TV"

# Link direto para a logo que você acabou de subir no repositório
LOGO_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/Logo%20RadarTV%203000x3000.jpg"

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

def get_current_playlist_info(playlist_id):
    """Puxa os dados dos vídeos para pegar o título principal da playlist"""
    try:
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        cmd = ["yt-dlp", "--flat-playlist", "--print", "%(title)s", url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout:
            lines = result.stdout.strip().split("\n")
            return lines if lines else []
        return []
    except:
        return []

def create_m3u():
    m3u_content = '#EXTM3U\n'
    
    # 1. Verifica se está AO VIVO
    live_url = get_live_m3u8(CHANNEL_ID)
    
    if live_url:
        print("Sinal Aberto! Gerando canal único focado na Live.")
        # Injeta a logo e define o status como Ao Vivo
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} [AO VIVO]\n'
        m3u_content += f'{live_url}\n'
    else:
        print("Canal Offline. Unificando playlist em um único canal contínuo.")
        titulos = get_current_playlist_info(PLAYLIST_ID)
        
        # Cria a informação de EPG adaptada baseada nos vídeos da playlist
        status_programa = "Programação Ruralzão 2026"
        if titulos and len(titulos) > 0:
            status_programa = f"Exibindo: {titulos[0]}" # Pega o título do vídeo principal/mais recente
        
        # Link agregador da playlist do YouTube que roda de forma contínua
        playlist_stream = f"https://www.youtube.com/embed/videoseries?list={PLAYLIST_ID}"
        
        # Cria APENAS uma linha de canal com o logo e o título dinâmico na descrição
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} ({status_programa})\n'
        m3u_content += f'{playlist_stream}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Canal único estruturado e salvo com sucesso!")

if __name__ == "__main__":
    create_m3u()
