import os
import re
import subprocess
import urllib.request

# ==========================================
# CONFIGURAÇÕES DA EMISSORA (RADAR TV)
# ==========================================
PLAYLIST_NAME = "Radar TV"
LOGO_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/Logo%20RadarTV%203000x3000.jpg"

# 1. CANAL PRINCIPAL (Programação padrão contínua)
CANAL_PRINCIPAL_FCV = "https://video01.logicahost.com.br/fcvtv/fcvtv/playlist.m3u8"

# 2. CANAL SECUNDÁRIO (Seu player ao vivo no Iblups)
IBLUPS_ID = "e96f8910-bd68-4c58-aae6-785a61a475db"
IBLUPS_PAGE_URL = f"https://iblups.com/{IBLUPS_ID}"


def obter_stream_iblups():
    """
    Tenta capturar o link de vídeo (.m3u8) da sua live no Iblups de duas formas.
    """
    print(f"[DEBUG] Acessando a página do Iblups: {IBLUPS_PAGE_URL}")
    
    # Método 1: Varredura direta no HTML por links .m3u8
    try:
        req = urllib.request.Request(
            IBLUPS_PAGE_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Procura por qualquer link m3u8 dentro do código fonte da página
            m3u8_matches = re.findall(r'https?://[^\s\'"\\]+\.m3u8[^\s\'"\\]*', html)
            if m3u8_matches:
                stream_url = m3u8_matches[0].replace('\\', '')
                print(f"[SUCESSO] Link de transmissão encontrado no HTML: {stream_url}")
                return stream_url
            
            print("[DEBUG] Nenhum link .m3u8 direto foi encontrado no HTML.")
    except Exception as e:
        print(f"[ERRO] Falha ao acessar a página HTML: {e}")

    # Método 2: Extração profunda usando yt-dlp
    try:
        print("[DEBUG] Tentando extrair sinal via yt-dlp...")
        cmd = ["yt-dlp", "-g", "--no-warnings", IBLUPS_PAGE_URL]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        stream_url = result.stdout.strip()
        
        if result.returncode == 0 and "m3u8" in stream_url:
            print(f"[SUCESSO] Link obtido via yt-dlp: {stream_url}")
            return stream_url
        print("[DEBUG] yt-dlp não retornou um link .m3u8 válido.")
    except Exception as e:
        print(f"[ERRO] Falha na execução do yt-dlp: {e}")

    return None


def create_m3u():
    m3u_content = '#EXTM3U\n'
    
    stream_live = obter_stream_iblups()
    
    if stream_live:
        print("🔴 SINAL AO VIVO DETECTADO! Alternando a lista para o Iblups.")
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} [AO VIVO]\n'
        m3u_content += f'{stream_live}\n'
    else:
        print("📺 NENHUM SINAL AO VIVO DETECTADO. Mantendo o canal FCV TV.")
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME}\n'
        m3u_content += f'{CANAL_PRINCIPAL_FCV}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
        
    print("✅ Arquivo lista.m3u gerado!")


if __name__ == "__main__":
    create_m3u()
