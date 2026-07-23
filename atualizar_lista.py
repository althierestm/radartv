import os
import subprocess

# Configurações da sua Emissora (Radar TV)
PLAYLIST_NAME = "Radar TV"
LOGO_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/Logo%20RadarTV%203000x3000.jpg"

# 1. CANAL PRINCIPAL: Sinal contínuo da FCV TV
CANAL_PRINCIPAL_FCV = "https://video01.logicahost.com.br/fcvtv/fcvtv/playlist.m3u8"

# 2. CANAL SECUNDÁRIO: Seu Player na Iblups
IBLUPS_PAGE_URL = "https://iblups.com/e96f8910-bd68-4c58-aae6-785a61a475db"


def obter_stream_iblups(url):
    """
    Usa o yt-dlp para extrair o link .m3u8 direto da página do Iblups.
    """
    try:
        cmd = ["yt-dlp", "-g", "--no-warnings", url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        stream_url = result.stdout.strip()
        
        if result.returncode == 0 and "m3u8" in stream_url:
            print(f"Sinal .m3u8 capturado da Iblups: {stream_url}")
            return stream_url
        return None
    except Exception as e:
        print(f"Erro ao verificar Iblups: {e}")
        return None


def create_m3u():
    m3u_content = '#EXTM3U\n'
    
    print("Verificando se a transmissão da Iblups está no ar...")
    stream_live = obter_stream_iblups(IBLUPS_PAGE_URL)
    
    if stream_live:
        # 🔴 Se o sinal .m3u8 da Iblups for encontrado: Entra a sua Live
        print("🔴 Live Iblups Detectada! Alternando para a sua transmissão.")
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} [AO VIVO]\n'
        m3u_content += f'{stream_live}\n'
    else:
        # 📺 Se estiver offline: Transmite a FCV TV como Canal Principal
        print("📺 Transmitindo Canal Principal (FCV TV)...")
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME}\n'
        m3u_content += f'{CANAL_PRINCIPAL_FCV}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
        
    print("Arquivo lista.m3u gerado com sucesso!")


if __name__ == "__main__":
    create_m3u()
