import os
import re
import urllib.request

# Configurações da sua Emissora (Radar TV)
PLAYLIST_NAME = "Radar TV"
LOGO_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/Logo%20RadarTV%203000x3000.jpg"

# 1. CANAL PRINCIPAL: Sinal contínuo da FCV TV
CANAL_PRINCIPAL_FCV = "https://video01.logicahost.com.br/fcvtv/fcvtv/playlist.m3u8"

# 2. CANAL SECUNDÁRIO: Seu Player na Iblups
IBLUPS_PAGE_URL = "https://iblups.com/e96f8910-bd68-4c58-aae6-785a61a475db"


def obter_stream_iblups(url):
    """
    Acessa a página da Iblups e extrai o link .m3u8 do vídeo ao vivo.
    """
    try:
        req = urllib.request.Request(
            url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Procura por qualquer URL terminada em .m3u8 no código da página
            matches = re.findall(r'https?://[^\s\'"\\]+\.m3u8[^\s\'"\\]*', html)
            if matches:
                # Limpa eventuais caracteres de escape
                stream_m3u8 = matches[0].replace('\\', '')
                print(f"Sinal .m3u8 encontrado na Iblups: {stream_m3u8}")
                return stream_m3u8
            
            return None
    except Exception as e:
        print(f"Canal Iblups offline ou inacessível no momento: {e}")
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
        # 📺 Se estiver offline ou sem sinal: Transmite a FCV TV como Canal Principal
        print("📺 Transmitindo Canal Principal (FCV TV)...")
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME}\n'
        m3u_content += f'{CANAL_PRINCIPAL_FCV}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
        
    print("Arquivo lista.m3u gerado com sucesso!")


if __name__ == "__main__":
    create_m3u()
