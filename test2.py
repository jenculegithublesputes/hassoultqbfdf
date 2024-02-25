import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Vérifier si le dossier 'videos' existe, sinon le créer
if not os.path.exists('videos'):
    os.makedirs('videos')

# Obtenir le nombre de pages à scraper depuis l'utilisateur
num_pages = int(input("Entrez le nombre de pages à scraper: "))

# Code pour extraire les liens des pages de la première URL
base_url = 'https://hotscope.tv/category/masturbation?page='

links = []
for page in range(1, num_pages + 1):
    url = base_url + str(page)
    print(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href.startswith('/periscope') or href.startswith('/snapchat') or href.startswith('/onlyfans') or href.startswith('/porn'):
            links.append("https://hotscope.tv" + href)

# Utiliser ThreadPoolExecutor pour récupérer les liens en parallèle
def fetch_link_content(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    video_links = []
    for video in soup.find_all('video'):
        src = video.get('src')
        if src and src.startswith('https://cdn.hotscope.tv/files/') and '.mp4' in src:
            video_links.append(src)
    
    return video_links

with ThreadPoolExecutor(max_workers=20) as executor:
    all_video_links = list(executor.map(fetch_link_content, links))

# Flatten the list of lists
video_links = [link for sublist in all_video_links for link in sublist]

with open('links.txt', 'w') as file:
    for link in video_links:
        file.write(link + '\n')

# Utiliser ThreadPoolExecutor pour télécharger en parallèle
def download_video(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Nom du fichier basé sur le dernier segment du lien
        filename = os.path.join('videos', url.split('/')[-1])

        # Télécharger le fichier dans le dossier 'videos'
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print(f'Téléchargé : {filename}')
    except requests.exceptions.RequestException as e:
        print(f'Erreur de téléchargement pour {url}: {e}')

# Utiliser ThreadPoolExecutor pour télécharger en parallèle
with ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(download_video, video_links)
