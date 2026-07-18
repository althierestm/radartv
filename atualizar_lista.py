import os

# Configurações do canal Radar TV
PLAYLIST_NAME = "Radar TV"
LOGO_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/Logo%20RadarTV%203000x3000.jpg"

# URL de incorporação direta da sua live ativa no OBS
LIVE_STREAM_URL = "https://www.youtube.com/embed/F23k820MfEU"

def create_m3u():
    m3u_content = '#EXTM3U\n'
    
    # Monta o canal único apontando para o link estável da transmissão
    print("Gerando arquivo de canal único estável para o player.")
    m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME} [AO VIVO]\n'
    m3u_content += f'{LIVE_STREAM_URL}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Lista criada com sucesso!")

if __name__ == "__main__":
    create_m3u()
