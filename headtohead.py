import requests
import re
from bs4 import BeautifulSoup
import shutil

S = requests.Session()

URL = "https://liquipedia.net/starcraft2/api.php"
HEADER = {'User-Agent': 'Head To Head Matchup Generation (beomulf@gmail.com)'}
sc2_url = 'https://www.liquidpedia.net/starcraft2/'
default_url = 'https://www.liquidpedia.net/'




def get_page_names(player_list):
    page_names = []

    for player in player_list:
        PARAMS = {
            'action': "query",
            'format': "json",
            'list': 'search',
            'srsearch': player
        }
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        if DATA['query']['search'][0]['title'].lower() == player.lower():
            page_names.append(DATA['query']['search'][0]['title'])

    return page_names

def get_main_images(title):
    image_url = ''
    page_url = sc2_url + title
    page = requests.get(page_url).text
    soup = BeautifulSoup(page, 'html.parser')
    for raw_img in soup.find_all('img'):
        link = raw_img.get('src')
        if re.search('commons/.*/thumb/', link) and not re.search('.svg', link) and not re.search('Icon', link):
            image_url = default_url + link
            break
    filename = 'img\\' + title + '.' + image_url.split('.')[-1]
    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retreived')