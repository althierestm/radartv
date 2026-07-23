import os
import subprocess

# Configurações da sua Emissora (Radar TV)
PLAYLIST_NAME = "Radar TV"
LOGO_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/Logo%20RadarTV%203000x3000.jpg"

# 1. CANAL PRINCIPAL: Sinal contínuo da FCV TV
CANAL_PRINCIPAL_FCV = "https://video01.logicahost.com.br/fcvtv/fcvtv/playlist.m3u8"

# 2. CANAL SECUNDÁRIO: Cole aqui o link M3U8 ou URL do seu Player Próprio / Live
# (Substitua a URL abaixo pelo link direto do seu outro player)
CANAL_SECUNDARIO_LIVE = "https://SEU_PLAYER_PROPRIO_AQUI.m3u8"


def checar_sinal_ao_vivo(url):
    """
    Verifica se o seu canal secundário está respondendo e transmitindo.
    """
    if "SEU_PLAYER_PROPRIO" in url:
        # Se você ainda não colocou o link real, mantém o principal
        return False
        
    try:
        # Tenta validar se o link do seu player está ativo via yt-dlp ou requisição
        cmd = ["yt-dlp", "-g", url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.returncode == 0 and len(result.stdout.strip()) > 0
    except:
        return False


def create_m3u():
    m3u_content = '#EXTM3U\n'
    
    print("Verificando disponibilidade do Canal Secundário (Sua Live Própria)...")
    tem_live_propria = checar_sinal_ao_vivo(CANAL_SECUNDARIO_LIVE)
    
    if tem_live_propria:
        # 🔴 Se o seu player secundário estiver NO AR: Entra a sua Live
        print("🔴 Live Própria Detectada! Alternando para o Sinal Secundário.")
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} [AO VIVO]\n'
        m3u_content += f'{CANAL_SECUNDARIO_LIVE}\n'
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
