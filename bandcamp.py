from selenium.webdriver import Firefox
from selenium.webdriver import Chrome
import sys, os


#change for a headless connection
URL = "https://bandcamp.com/"
FF_PATH = "./drivers/geckodriver.exe"
CHR_PATH = "./drivers/chromedriver.exe"
EDG_PATH = "./drivers/msedgedriver.exe"#requires extra care
HEADLESS = not os.access('YES', os.R_OK)
ff = None

print(f'HEADLESS:{HEADLESS}')
#print(sys.argv)
print('setting up!')
browser = sys.argv[1].lower()
if browser == "firefox":
    from selenium.webdriver.firefox.options import Options
    options = Options()
    if sys.argv[-1].lower() == 'android':
        options.add_argument('androidPackage', 'com.android.chrome')
        print('run on android')
    options.headless = HEADLESS
    ff = Firefox(executable_path=FF_PATH, options=options)
elif browser == "chrome":
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.headless = HEADLESS
    ff = Chrome(executable_path=CHR_PATH,options=options)
else :
    print(f"unsupported {browser} browser")
    exit(1)

print('Opening site...')
ff.get(URL)
print("Site opened!")
#+++++++++++++++++++++Prot
#parent holders
try:
    discover = ff.find_element_by_id('discover')
except Exception as e:
    print('failed to load page (probably a network issue)')
    exit(0)

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
#selected elements
s_genre = genre_bar.find_element_by_class_name('selected')
s_subgenre = None
s_music = None

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
    global s_genre
    if g in getGenresNames():
        s_genre = g
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


def setSubGenre(s):
    subs = getSubGenres()
    global s_subgenre,s_genre
    if len(subs)<=0:
        print(f"{s_genre} has no subgenre")
    else:
        if s in subs.keys():
            try:
                subs[s].click()
                s_subgenre = s
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


def destroy():
    ff.close()


def updateData():
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


def refresh():
    ff.refresh()
    updateData() 


## creates or deletes a YES file
def changemode(mode):
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
    m_list = dict(list( zip( getMusicListNames(), getMusicList()) ))
    if music in m_list.keys():
        m_list[music].click()
    else:
        print(f"{music} not found!" )


###Main LOOP
HELP = f"""
        help                                for help
        exit                                to exit
        play [music_name]                   to play a music

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
        {"changemode [mode]                 headless or graphical mode (add or delete a YES file with no extensions to enable/disable headless mode)"*0}
       """  
print(HELP)


while True:
    try:
        command = input(">>")
        command_parts = command.split(' ')
        parameters = ' '.join(command_parts[1:])
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
        else:
            print(f"**unkown command '{command_parts[0]}'")
    except Exception as e:
        print('Error\n',e,'Error\n')
        print('Exiting...')
        destroy()