import os
import re
import urllib.request

# ==========================================
# CONFIGURAÇÕES DA EMISSORA (RADAR TV)
# ==========================================
PLAYLIST_NAME = "Radar TV"
LOGO_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/Logo%20RadarTV%203000x3000.jpg"

# 1. CANAL PRINCIPAL (Programação padrão contínua)
CANAL_PRINCIPAL_FCV = "https://video01.logicahost.com.br/fcvtv/fcvtv/playlist.m3u8"

# 2. CANAL SECUNDÁRIO (Link de Embed Direto do Iblups)
IBLUPS_EMBED_URL = "https://iblups.com/embed/radartv032"


def obter_stream_iblups():
    """
    Acessa o player de embed do Iblups e extrai o sinal .m3u8 ao vivo.
    """
    print(f"[DEBUG] Lendo o player de embed: {IBLUPS_EMBED_URL}")
    try:
        req = urllib.request.Request(
            IBLUPS_EMBED_URL, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Procura por qualquer URL .m3u8 ou manifest dentro do player
            m3u8_matches = re.findall(r'https?://[^\s\'"\\]+\.m3u8[^\s\'"\\]*', html)
            if m3u8_matches:
                stream_url = m3u8_matches[0].replace('\\', '')
                print(f"[SUCESSO] Sinal .m3u8 encontrado: {stream_url}")
                return stream_url
            
            # Segunda tentativa: captura de links HLS alternativos
            hls_matches = re.findall(r'(https?://[^\s\'"\\]+iblups[^\s\'"\\]+)', html)
            for match in hls_matches:
                if "live" in match or "m3u8" in match:
                    clean_url = match.replace('\\', '').strip()
                    print(f"[SUCESSO] Sinal HLS encontrado: {clean_url}")
                    return clean_url

            print("[DEBUG] Nenhum sinal ativo encontrado no player do Iblups.")
            return None
    except Exception as e:
        print(f"[ERRO] Erro ao conectar no Iblups: {e}")
        return None


def create_m3u():
    m3u_content = '#EXTM3U\n'
    
    stream_live = obter_stream_iblups()
    
    if stream_live:
        print("🔴 SINAL AO VIVO DETECTADO! Alternando lista para a Radar TV.")
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} [AO VIVO]\n'
        m3u_content += f'{stream_live}\n'
    else:
        print("📺 NENHUM SINAL AO VIVO. Transmitindo FCV TV (Programação Padrão).")
        m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME}\n'
        m3u_content += f'{CANAL_PRINCIPAL_FCV}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
        
    print("✅ Arquivo lista.m3u atualizado!")


if __name__ == "__main__":
    create_m3u()
