from selenium.webdriver import Firefox
from selenium.webdriver import Chrome

import sys


#change for a headless connection
URL = "https://bandcamp.com/"
FF_PATH = "./drivers/geckodriver.exe"
CHR_PATH = "./drivers/chromedriver.exe"
EDG_PATH = "./drivers/msedgedriver.exe"#requires extra care
ff = None

print('Opening site...')
#print(sys.argv)

browser = sys.argv[1].lower()
if browser == "firefox":
    ff = Firefox(executable_path=FF_PATH)
elif browser == "chrome":
    ff = Chrome(executable_path=CHR_PATH)
else :
    print(f"unsupported {browser} browser")
    exit(1)
ff.get(URL)
print("Site opened!")
#+++++++++++++++++++++Prot
#parent holders
discover = ff.find_element_by_id('discover')
pages_holder = discover.find_element_by_class_name('discover-pages')

#direct holders
filter_bar = discover.find_element_by_class_name('filter-types')
genre_bar = discover.find_element_by_class_name('genre-bar')
subgenre_bar = discover.find_element_by_class_name('subgenres-bar')
slice_bar = discover.find_element_by_class_name('slice-bar')
location_bar = discover.find_element_by_class_name('loc-bar')
format_bar = discover.find_element_by_class_name('format-bar')
dates_bar = discover.find_element_by_class_name('discover-dates')
music_bar = discover.find_element_by_class_name('result-current')

#++++++++++++++++++++categories  (useless currently)
genres = None       #independant
sub_genres = None   #dependant
filters = None      #independant
slices = None       #independant
formats = None      #dependant
times = None        #dependant
locations = None    #dependant
dates = None        #dependant
#+++++++++++++++++++interactables
music_list = None
pages = None

#Getters

def getGenres():
    span_list = genre_bar.find_elements_by_tag_name('span')
    global genres
    genres  = {a.text: a for a in span_list}
    return genres

def getGenresNames():
    return [a for a in getGenres().keys()]

def getSubGenres():
    span_list = subgenre_bar.find_elements_by_tag_name('span')
    global sub_genres
    sub_genres = {a.text: a for a in span_list}
    return sub_genres

def getSubGenresNames():
    return [a for a in getSubGenres().keys()]

def getFilters():
    span_list = filter_bar.find_elements_by_tag_name('span')
    filters = {a.text: a for a in span_list}
    return filters

def getFiltersNames():
    return [a for a in getFilters().keys()]

def getSlices():
    span_list = slice_bar.find_elements_by_tag_name('span')
    slices = {a.text: a for a in span_list}
    return slices

def getSlicesNames():
    return [a for a in getSlices().keys()]

def getFormats():
    span_list = format_bar.find_elements_by_tag_name('span')
    formats = {a.text: a for a in span_list}
    return formats

#formatsNames

def getLocations():
    span_list = location_bar.find_elements_by_tag_name('span')
    locations = {a.text: a for a in span_list}
    return locations

#locationsNames

def getTimes():
    span_list = dates_bar.find_elements_by_tag_name('span')
    dates = {a.text: a for a in span_list}
    return dates

#times names

#++++++Elements
def getMusicList():
    music_list = discover.find_elements_by_class_name('discover-item') #direct
    return music_list

def getMusicListNames():
    return [el.text for el in music_bar.find_elements_by_class_name('item-title')]

def getMusicListArtists():
    return [el.text for el in music_bar.find_elements_by_class_name('item-artist')]

def getPages():
    pages = pages_holder.find_elements_by_class_name('item-page') #direct
    return {a.text: a for a in pages }


##Setters

def setGenre(g):
    #item out of sight handling
    if g in getGenresNames():
        try:
            getGenres()[g].click()
        except Exception as e :
            print(f"Error: element obscured =) scrolling...")
            genre_bar.find_element_by_class_name('scroller-next').click()
            print("retry command")
    else:
        print(f"Unregistered genre! '{g}'")


def setPage(p):
    pages =  getPages()
    if p in pages.keys():
        pages[p].click()
    else:
        print(f"** can not find '{p}' page")


def setSubGenres():
    return "Subgenres Set!"

def setFilters():
    return "Filters Set!"

def setSlices():
    return "Slices Set!"

def setFormats():
    return "Formats Set!"

def setLocations():
    return "Locations Set!"

def setTimes():
    return "Times Set!"

def destroy():
    ff.close()

def refresh():
    ff.refresh()
    #========globals
    global discover, pages_holder, filter_bar, genre_bar, subgenre_bar, slice_bar,location_bar, format_bar, dates_bar, music_bar, music_bar
    #parent holders
    discover = ff.find_element_by_id('discover')
    pages_holder = discover.find_element_by_class_name('discover-pages')

    #direct holders
    filter_bar = discover.find_element_by_class_name('filter-types')
    genre_bar = discover.find_element_by_class_name('genre-bar')
    subgenre_bar = discover.find_element_by_class_name('subgenres-bar')
    slice_bar = discover.find_element_by_class_name('slice-bar')
    location_bar = discover.find_element_by_class_name('loc-bar')
    format_bar = discover.find_element_by_class_name('format-bar')
    dates_bar = discover.find_element_by_class_name('discover-dates')
    music_bar = discover.find_element_by_class_name('result-current')

    #============End

    pass

#interaction
def play(music):
    m_list = dict(list( zip( getMusicListNames(), getMusicList()) ))
    if music in m_list.keys():
        m_list[music].click()
    else:
        print(f"{music} not found!" )


###Main LOOP
HELP = """
        help                for help
        exit                to exit
        listartist          to list current playlist artist
        listmusic           to list available music
        listgenres          to list available genres
        setgenre [genre]    to set a genre filter
        listpages           to list available pages
        setpage [page]      to set a page
        play [music_name]   to play a music
        refresh             refresh pages (in case page not fully loaded)
       """  
print(HELP)

while True:
    command = input(">>")
    command_parts = command.split(' ')
    if "exit" in command:
        print("Goodbye!")
        ff.close()
        break
    elif "help" in command :
        print(HELP)
    elif "listartist" in command:
        print("**", getMusicListArtists())
    elif "listmusic" in command:
        print("**", getMusicListNames())
    elif "play" in command:
        play(' '.join(command_parts[1:]))
    elif "refresh" in command:
        refresh()
    elif "listgenres" in command:
        print("**", getGenresNames())
    elif "setgenre" in command:
        setGenre(' '.join(command_parts[1:]))
    elif "listpages" in command:
        print("**", list(getPages().keys()))
    elif "setpage" in command:
        setPage(' '.join(command_parts[1:]))
    else:
        print(f"**unkown command '{command_parts[0]}'")
    