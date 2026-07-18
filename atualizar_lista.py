import os

# Configurações do canal Radar TV
PLAYLIST_NAME = "Radar TV"
LOGO_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/Logo%20RadarTV%203000x3000.jpg"

# Link direto e oficial do formato de live do YouTube que os players conseguem interpretar
LIVE_STREAM_URL = "https://www.youtube.com/watch?v=F23k820MfEU"

def create_m3u():
    m3u_content = '#EXTM3U\n'
    
    # Monta o canal fixo apontando direto para a transmissão ativa do OBS
    print("Gerando canal único apontando para a transmissão direta.")
    m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} [AO VIVO]\n'
    m3u_content += f'{LIVE_STREAM_URL}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Lista criada com sucesso com o link direto!")

if __name__ == "__main__":
    create_m3u()
