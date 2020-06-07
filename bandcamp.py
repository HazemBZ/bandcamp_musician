from selenium.webdriver import Firefox,Chrome
from albums import start_extract
from os import system
from random import randint
## experimental
#from IPython import embed

from databases import MongoHandler
## ISSUE (extraction fails in some caises and breaks with no text for Nonetype)
## link that fails => https://therentals.bandcamp.com/album/q36?from=discover-top
import sys,os,time,subprocess
WIN_CHARS = ["/", "\\", ":", "?", "<", ">", "|"] # windows unaccepted characters

### uri !Android options does not work currently
URL = "https://bandcamp.com/"
FF_PATH = "./drivers/geckodriver"
CHR_PATH = "./drivers/chromedriver.exe"
CHRA_PATH = "./chromedriver"
EDG_PATH = "./drivers/msedgedriver.exe"#requires extra care
# config files
config_file_path = "ydl_config.txt"
mongod_conf= "mongod.conf"
download_folder= "$HOME/Desktop/ydl/"
# FLAGS
HEADLESS =  os.access('YES', os.R_OK)
DB_DIR_SET= os.access('data', os.R_OK) and os.access('data/db', os.R_OK) and os.access('data/logs', os.R_OK)
debug = False
# -----------
ff = None # browser client

print(f'HEADLESS:{HEADLESS}')
#print(sys.argv)
print('setting up!')
browser = sys.argv[1].lower()

if browser == "firefox":
    from selenium.webdriver.firefox.options import Options
    options = Options()
    options.headless = HEADLESS
    ff = Firefox(executable_path=FF_PATH, options=options)
elif browser == "chrome":
    from selenium.webdriver.chrome.options import Options
    options = Options()
    if sys.argv[-1].lower() == 'android':
        options.add_experimental_option('androidPackage', 'com.android.chrome')
        print('run on android')
        ff = Chrome(CHRA_PATH, options=options)
    else:
        options.headless = HEADLESS
        ff = Chrome(executable_path=CHR_PATH,options=options)
elif browser == "debug":
    print("Debug mode")
    print('run script in interactive mode with -i option')
    debug = True
else :
    print(f"unsupported {browser} browser")
    exit(1)
if not debug:
    print(' *Loading window...')
    ff.get(URL)
    print(" =>Site opened!")
    #+++++++++++++++++++++Prot
    #parent holders

    try:
        discover = ff.find_element_by_id('discover')
    except Exception as e:
        print('failed to load page (probably a network issue)')
        ff.close()
        exit(1)

    try:
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
        details_inner = discover.find_element_by_class_name('discover-detail-inner')
    except Exception:
        print("failed to scrape a node")
        ff.close()
        exit(1)

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
    named_music_list = None
    enum_music_list = None
    pages = None
    #selected elements
    s_genre = genre_bar.find_element_by_class_name('selected')
    s_subgenre = None
    s_music = None

    """ Databases section """
    process = None
    try:
        print(" *setting up database")
        if not DB_DIR_SET:
            print("  -creating db dir stcuture")
            subprocess.run(["bash","-c","mkdir -p data/{db,logs}"])
        process = subprocess.Popen(['/usr/bin/mongod', '-f', mongod_conf],stdout=subprocess.DEVNULL)
        db = MongoHandler()
        print(" => database all set")
    except Exception:
        print("Failed to initiate database client or server")
        ff.close()
        exit(1)
    print(f'db=> {db.db} selected')
    #Getters

    # cache
    "Cached data"
    last_current = None
    last_extract = None


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
    global s_genre
    l = [a for a in getSubGenres().keys()]
    return l if l else f"No subgenre found for {s_genre}"

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
    named_music_list = discover.find_elements_by_class_name('discover-item') #direct
    return named_music_list

def getMusicListNames():
    return [el.text for el in music_bar.find_elements_by_class_name('item-title')]

def getMusicListArtists():
    return [el.text for el in music_bar.find_elements_by_class_name('item-artist')]

def getPages():
    pages = pages_holder.find_elements_by_class_name('item-page') #direct
    return {a.text: a for a in pages }

def current():
    global details_inner, last_current
    title = details_inner.find_element_by_class_name('title').text
    album = details_inner.find_element_by_class_name('detail-album').text
    artist = details_inner.find_element_by_class_name('detail-artist').text
    location = details_inner.find_element_by_class_name('detail-loc').text
    time_el = details_inner.find_element_by_class_name('time_elapsed').text
    time_tot = details_inner.find_element_by_class_name('time_total').text
    url = details_inner.find_element_by_css_selector("span.detail-album a").get_property("href")
    last_current = {'name':title, 'album':album, 'artist':artist, 'elapsed':time_el, 'total':time_tot, 'url':url}
    return last_current

##Setters

def setGenre(g):
    #item out of sight handling
    global s_genre
    if g in getGenresNames():
        s_genre = g
        try:
            getGenres()[g].click()
            current()
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


def setSubGenre(s):
    global s_subgenre,s_genre
    subs = getSubGenres()
    if len(subs) <= 0:
        print(f"{s_genre} has no subgenre")
    else:
        if s in subs.keys():
            try:
                subs[s].click()
                s_subgenre = s
                current()
            except:
                print("element obscured try again")
                subgenre_bar.find_element_by_class_name('scroller-next').click()
        else:
            print(f"unkown {s} subgenre" )


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


def end():
    global ff, process
    try:
        if process:
            process.terminate()
            process.poll()
        ff.close()
    except Exception as exp:
        print(exp)


def updateData():
    #========globals
    global discover, pages_holder, filter_bar, genre_bar, subgenre_bar, slice_bar,location_bar, format_bar, dates_bar, music_bar, music_bar
    try:
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
    except Exception:
        print("failed to update nodes data")
    #============End


def updateMusicLists():
    global named_music_list, enum_music_list
    n_list = getMusicListNames()
    m_list = getMusicList()
    named_music_list =  dict( zip( n_list, m_list ) )   #global
    enum_music_list = dict(enumerate(m_list))   #global


def refresh():
    ff.refresh()
    updateData()


## creates or deletes a YES file
def changemode(mode):
    global HEADLESS
    if "headless" in mode:
        if HEADLESS:
            print('already in headless mode')
        else:
            try:                #try delete YES file
                os.remove('./YES')
                HEADLESS = True
                print('mode set to HEADLESS')
            except Exception as e:
                print('\n',e,'\n')
    elif "gui" in mode:
        if HEADLESS:
            with open('YES','wb'):  #create YES file
                pass
            HEADLESS = False
        else:
            print('already in gui mode')
    else:
        print(f"unknown mode {mode}")

#interaction
def play(music):
    global s_music
    if music in named_music_list.keys():
        s_music = named_music_list[music]
        try:
            s_music.click()
        except Exception:
            s_music.click()
            print("second click!")
    else:
        print(f"title: {music} not found!" )


def playindex(index):
    global s_music, enum_music_list
    if enum_music_list == None:
        updateMusicLists()
    if index.isdigit():
        dig = int(index)
        if dig in enum_music_list.keys():
            s_music = enum_music_list[dig]
            try:
                s_music.click()
            except Exception:
                s_music.click()
                print("second click!")
        else:
            print(f"{dig} index not found!")
    else:
        print(f"{index} not a digit!!")




def save_current(desc="No description", collection='no_colletion'):
    global db
    db.insert_documents([{'track_meta':current(),'description':desc, 'time':time.strftime('%Y-%m-%d %H:%M,%S')}], collection)

def toggle_playing_music():
    global s_music
    if s_music:
        s_music.click()

def playrand():
    global s_music, enum_music_list
    if enum_music_list == None:
        updateMusicLists()
    ra = randint(0, len(enum_music_list)-1)
    s_music = enum_music_list[ra]
    try:
        s_music.click()
    except Exception:
        s_music.click()
        print("second click!")
    #current()

# REFACTOR (pass ydl config options as parameters)
def update_config_file(dir_name):
    global config_file_path, download_folder
    with open(config_file_path, "w") as f:
        f.write(f"-o {download_folder}{dir_name}/%(title)s.%(ext)s")

def batch_replace(word,chars_l,replacement=""):
    copy = word
    for char in chars_l:
        copy = copy.replace(char, replacement)
    return copy

###Main LOOP
HELP = f"""
        help                                for help
        exit                                to exit
        play [music_name]                   to play music with its name
        playindex [index]                   to play music with an index
        toggle                              to pause/play selectes music

        listmusic                           to list available music
        listartist                          to list current playlist artist

        listgenres                          to list available genres
        setgenre [genre]                    to set a genre filter

        listpages                           to list available pages
        setpage [page]                      to set a page

        listsubs                            to list available subgenres
        setsub [subgenre]                   to set a subgenre

        getfilters                          {"*"*10}
        activatefilter [filter_name]        {"*"*10}

        refresh                             refresh pages (in case page not fully loaded)
        current                             selected track details
        extract                             extract an album url and returns its tracks
        album                               last extracted album
        downloadindex                       downloads with track index
        downloadalbum                       download selecred track's album
        {"changemode [mode]                 headless or graphical mode (add or delete a YES file with no extensions to enable/disable headless mode)"*0}
       """
print(HELP)


while True:
    #embed()
    try:
        command = input(">>")
        command_parts = command.split(' ')
        parameters = ' '.join(command_parts[1:])
        if "exit" in command:
            print("Goodbye!")
            end()
            exit(0)
        elif "help" in command :
            print(HELP)
        elif "listartist" in command:
            print("**", getMusicListArtists())
        elif "listmusic" in command:
            updateMusicLists()
            print("**", dict(zip(enum_music_list.keys(), named_music_list.keys())))
        elif "playindex" in command_parts:
            playindex(command_parts[-1])
            current()
            save_current(collection='music_history')
        elif "play" in command_parts:
            play(parameters)
            current()
            save_current(collection='music_history')
        elif "refresh" in command:
            refresh()
        elif "listgenres" in command:
            print("**", getGenresNames())
        elif "setgenre" in command:
            setGenre(parameters)
        elif "listpages" in command:
            print("**", list(getPages().keys()))
        elif "setpage" in command:
            setPage(parameters)
        elif "listsubs" in command:
            print(getSubGenresNames())
        elif "setsub" in command:
            setSubGenre(parameters)
        elif "changemode" in command:
            changemode(command_parts[1:])
        elif "updatedata" in command:           #dev tool
            updateData()
        # elif "dev" in command:
        #     break
        elif "current" in command:
            print(current())
        elif "save" in command:
            save_current(str.strip(parameters), 'saved_tracks')
        elif "toggle" in command:
            toggle_playing_music()
        elif "devmode" in command:
            break
        elif "extract" in command:
            if not last_current:
                last_current = current()
            last_extract = start_extract(last_current['url'])
            print(last_extract)
        elif "downloadindex" in command:# REFACTOR
            if not last_current:
                current()
            album ='"'+ batch_replace(last_current['album'], WIN_CHARS)+'"'
            subprocess.run(['mkdir', '-p', f"{download_folder}/{album}"])
            update_config_file(album)
            subprocess.Popen(["youtube-dl","-q", "--config-location", config_file_path, "--playlist-items", str(int(command_parts[-1])+1), last_current['url']])
            print(f" donwload started at {download_folder}{album}")
        elif "downloadalbum" in command:# REFACTOR
            if not last_current:
                current()
            album = '"'+batch_replace(last_current['album'], WIN_CHARS)+'"'
            subprocess.run(['mkdir', '-p', f"{download_folder}/{album}"])
            update_config_file(album)
            subprocess.Popen(["youtube-dl", "-q", "--config-location", config_file_path, last_current['url']])
            print(f" donwload started at {download_folder}{album}")
        elif "album" in command:
            print(last_extract)
        elif "playrand" in command:
            playrand()
            current()
            save_current(collection='music_history')
        elif "su" in command:
            part = command_parts[-1]
            if part.isdigit():
                subprocess.run(["_snd", "up", part])
            else:
                print(f"{part} not a digit")
        ## _snd is an alias for shell script
        elif "sd" in command:
            part = command_parts[-1]
            if part.isdigit():
                subprocess.run(["_snd", "down", part])
            else:
                print(f"{part} not a digit")
        elif "snd" in command:
            part = command_parts[-1]
            if part.isdigit():
                subprocess.run(["_snd", "set", part])
            else:
                print(f"{part} not a digit")

        else:
            print(f"**unkown command '{command_parts[0]}'")
    except Exception as e:
        print('Error\n',e)
        print('Exiting...')
        end()
