from bs4 import BeautifulSoup
import urllib3

manager = urllib3.PoolManager()
tracks_data = None

def request_album(url):
    resp = manager.request("GET", url)
    print("Satus code => ", resp.status)
    return resp.data

def get_soup(data):
    soup = None
    try:
        soup = BeautifulSoup(data,'html.parser')
    except Exception as e:
        print("Failed to get soup".center(50,"*"))
        print(data)
    return soup

def start_extract(url):
    tracks_data = None
    print("Extracting => ", url)
    soup = get_soup(request_album(url))
    if soup != None:
        tracks_info = soup.find(id="trackInfoInner")
        #print("tracks_info ",tracks_info)
        tracks = tracks_info.find_all("tr", "track_row_view")
        #print("tracks========>", tracks,"*"*50)
        try:
            titles = list(map(lambda track:track.find("div", "title"), tracks))
            #print("="*80)
            #print("titles",titles)
            tracks_data = {index:link.a.text for index,link in enumerate(titles) if link.a}
        except Exception as e:
            print(e)
    return tracks_data
