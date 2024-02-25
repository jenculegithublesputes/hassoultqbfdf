import os
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from concurrent.futures import ThreadPoolExecutor

# Vérifier si le dossier 'videos' existe, sinon le créer
if not os.path.exists('videos'):
    os.makedirs('videos')

# Code pour extraire les liens des pages de la première URL
url = 'https://hotscope.tv/category/masturbation?page=1'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

links = []
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

with ThreadPoolExecutor(max_workers=5) as executor:
    all_video_links = list(executor.map(fetch_link_content, links))

# Flatten the list of lists
video_links = [link for sublist in all_video_links for link in sublist]

with open('links.txt', 'w') as file:
    for link in video_links:
        file.write(link + '\n')

# Lire les URL à partir du fichier links.txt
with open('links.txt', 'r') as file:
    urls = file.read().splitlines()

# Utiliser ThreadPoolExecutor pour télécharger en parallèle
def download_video(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver les balises vidéo et extraire les liens
    for video in soup.find_all('video'):
        src = video.get('src')
        if src and src.startswith('https://cdn.hotscope.tv/files/') and '.mp4' in src:
            # Nom du fichier basé sur le dernier segment du lien
            filename = os.path.join('videos', src.split('/')[-1])

            # Télécharger le fichier dans le dossier 'videos'
            urlretrieve(src, filename)
            print(f'Téléchargé : {filename}')

# Utiliser ThreadPoolExecutor pour télécharger en parallèle
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(download_video, urls)
