import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def scrape_dropbox_links(url, num_pages):
    all_links = []
    for page in range(1, num_pages+1):
        page_url = f"{url}&page={page}"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        dropbox_links = [link['href'] for link in links if 'dropbox.com' in link['href']]
        all_links.extend(dropbox_links)
    return all_links

def verifier_lien_dropbox(lien):
    response = requests.get(lien)
    soup = BeautifulSoup(response.text, 'html.parser')
    titre = soup.find('title').text if soup.find('title') else ''
    
    if titre == 'Dropbox - Error - Simplify your life' or titre == 'Dropbox - File Deleted - Simplify your life':
        return False
    else:
        return True

# Exemple d'utilisation
url_forum = "https://www.amateurvoyeurforum.com/showthread.php?t=42645"
nombre_pages = 2
liens_dropbox = scrape_dropbox_links(url_forum, nombre_pages)
print("Liens Dropbox récupérés :", liens_dropbox)

# Enregistrement dans un fichier texte avec un encodage UTF-8
with open('output.txt', 'w', encoding='utf-8') as file:
    file.write("Liens Dropbox valides :\n")

    with ThreadPoolExecutor(max_workers=3) as executor:
        valid_links = list(executor.map(verifier_lien_dropbox, liens_dropbox))
    
    for lien, est_valide in zip(liens_dropbox, valid_links):
        if est_valide:
            file.write(f"{lien}\n")

print("Liens valides enregistrés dans le fichier 'output.txt'")
