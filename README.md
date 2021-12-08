> A command line bandcamp music player (for now)

# Requirements:
+ python3
+ selenium
+ navigator
+ your navigator compatible webdriver (the latest Firefox and Chrome webdrivers are pre-packaged)
# Installation:
#### Install dependencies:
```
pip install -r requirements.txt
```

#### Add latest Webdriver to drivers folder
+ [geckdriver](https://github.com/mozilla/geckodriver/releases) -> Firefox browser
+ [chrmoium](https://chromedriver.chromium.org/) -> Chromium based browsers
+ [msedgedriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) -> Edge browser

#### Run the script:
```
python bandcamp.py [navigator_name]
```
# Support:
currently supports only Firefox and Chrome
