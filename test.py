import os
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, unquote

def process_link(link):
    if pattern.match(link['href']):
        video_id = re.search(r'\?v=(\d+)', link['href']).group(1)
        new_url = "https://monsnode.com/twjn.php?v=" + video_id
        new_response = requests.get(new_url)
        new_soup = BeautifulSoup(new_response.text, 'html.parser')
        
        # Extract links starting with "https://video.twimg.com/ext_tw_video"
        video_links = new_soup.find_all('a', href=re.compile(r'https://video.twimg.com/ext_tw_video'), string=re.compile(r'https://video.twimg.com/ext_tw_video'))
        
        for video_link in video_links:
            with open('output.txt', 'a') as output_file:
                output_file.write(video_link['href'] + '\n')

def download_video(link, output_folder='videos'):
    try:
        response = requests.get(link, stream=True)
        response.raise_for_status()

        parsed_url = urlparse(link)
        filename = os.path.join(output_folder, unquote(os.path.basename(parsed_url.path)))

        with open(filename, 'wb') as video_file:
            for chunk in response.iter_content(chunk_size=8192):
                video_file.write(chunk)

        print(f"Video downloaded successfully: {filename}")

    except Exception as e:
        print(f"Error downloading video: {e}")

def download_videos(input_file='output.txt', output_folder='videos'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(input_file, 'r') as file:
        links = file.readlines()

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_video, links, [output_folder]*len(links))

if __name__ == "__main__":
    num_pages = int(input("Enter the number of pages to save: "))
    
    for page in range(num_pages):
        url = f'https://monsnode.com/search.php?search=teen&page={page}'
        print(f"Processing page {page}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a', href=True)
        pattern = re.compile(r'https://monsnode.com/redirect.php\?v=')

        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(process_link, links)

    download_videos()
