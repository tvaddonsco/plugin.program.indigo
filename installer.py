# TVADDONS.CO / TVADDONS.CO - Addon Installer - Module By: Blazetamer (2013-2016)

import base64
import downloader
import extract
import os
import re
import ssl
import string
import sys
import time
import traceback
import urllib
import urllib2
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
from itertools import izip_longest

from libs import addon_able
from libs import aiapi
from libs import kodi
from libs import viewsetter

if kodi.get_kversion() > 16.5:
    ssl._create_default_https_context = ssl._create_unverified_context
else:
    pass

siteTitle = "TVADDONS.CO"
AddonTitle = kodi.AddonTitle
addon_id = kodi.addon_id
addon = (addon_id, sys.argv)
settings = xbmcaddon.Addon(id=addon_id)
ADDON = xbmcaddon.Addon(id=addon_id)
artPath = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'resources', 'art2/'))
artwork = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'art2/'))
mainPath = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id))
fanart = xbmc.translatePath(os.path.join(mainPath, 'fanart.jpg'))
iconart = xbmc.translatePath(os.path.join(mainPath, 'icon.png'))
dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
# <<<<<<<<<Common Variables>>>>>>>>>>>>>>>
Keymaps_URL = base64.b64decode("aHR0cDovL2luZGlnby50dmFkZG9ucy4va2V5bWFwcy9jdXN0b21rZXlzLnR4dA==")
Keymaps_URL = 'http://indigo.tvaddons.co/keymaps/customkeys.txt'
KEYBOARD_FILE = xbmc.translatePath(os.path.join('special://home/userdata/keymaps/', 'keyboard.xml'))
openSub = "https://github.com/stsrfbim/facial-recog/raw/master/development/service.subtitles.opensubtitles_by_opensubtitles/service.subtitles.opensubtitles_by_opensubtitles-5.1.14.zip"
burst_url = "http://burst.surge.sh/release/script.quasar.burst-0.5.8.zip"
# tvpath = "https://oldgit.com/tvaresolvers/tva-common-repository/raw/master/zips/"
tvpath = "https://github.com/zqfaen/tva-common/raw/master/zips/"
krypton_url = "http://mirrors.kodi.tv/addons/krypton/"
api = aiapi
CMi = []


# ****************************************************************
def get_params():
    param = [];
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2];
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'): params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&');
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {};
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2: param[splitparams[0]] = splitparams[1]
    return param


params = get_params()
url = None
name = None
mode = None
year = None
imdb_id = None


# ****************************************************************
def MAININDEX():
    kodi.addItem("Git Browser", '', 'github_main', artwork + 'github_browser.png',
                 description="Search for repositories hosted on GitHub.")
    kodi.addDir('Search by: Addon/Author', '', 'searchaddon', artwork + 'search.png',
                description="Search for addons by Name or Author")
    if settings.getSetting('featured') == 'true':
        kodi.addDir('Featured Addons', 'featured', 'addonlist', artwork + 'featured.png',
                    description="The most popular Kodi addons!")
    # if settings.getSetting('livetv') == 'true':
    #     kodi.addDir('Live TV Addons', 'live', 'addonlist', artwork + 'livetv.png',
    #                 description="The most popular live TV addons!")
    # if settings.getSetting('sports') == 'true':
    #     kodi.addDir('Sports Addons', 'sports', 'addonlist', artwork + 'sports.png',
    #                 description="The most popular sports addons!")
    if settings.getSetting('video') == 'true':
        kodi.addDir('Video Addons', 'video', 'addonlist', artwork + 'video.png',
                    description="Every video addon in existence!")
    if settings.getSetting('audio') == 'true':
        kodi.addDir('Audio Addons', 'audio', 'addonlist', artwork + 'audio.png',
                    description="Find addons to listen to music!")
    if settings.getSetting('program') == 'true':
        kodi.addDir('Program Addons', 'executable', 'addonlist', artwork + 'program.png',
                    description="Every program addon you can imagine!")
    # if settings.getSetting('playlist') == 'true':
    #     kodi.addDir('Playlist Addons', 'playlists', 'addonlist', artwork + 'playlists.png',
    #                 description="The most popular playlist addons!")
    if settings.getSetting('services') == 'true':
        kodi.addDir('Service Addons', 'service', 'addonlist', artwork + 'service.png')
    if settings.getSetting('skincat') == 'true':
        kodi.addDir('Kodi Skins', 'skins', 'addonlist', artwork + 'kodi_skins.png',
                    description="Change up your look!")
    if settings.getSetting('world') == 'true':
        kodi.addDir('International Addons', 'international', 'interlist', artwork + 'world.png',
                    description="Foreign language addons and repos from across the globe!")
    if settings.getSetting('adult') == 'true':
        kodi.addDir('Adult Addons', 'xxx', 'adultlist', artwork + 'adult.png',
                    description="Must be 18 years or older! This menu can be disabled from within Add-on Settings.")
    # if settings.getSetting('repositories') == 'true':
    # 	kodi.addDir('Repositories','repositories', 'addonlist', artwork + 'repositories.png',
    # 				description="Browse addons by repository!")
    # kodi.addItem('Enable Live Streaming', 'None', 'EnableRTMP', artwork + 'enablertmp.png',
    # 			 description="Enable RTMP InputStream and InputStream Adaptive modules for Live Streaming.")
    kodi.addItem('Official OpenSubtitles Addon', openSub, 'addopensub', artwork + 'opensubicon.png',
                 description="Install Official OpenSubtitles Addon!")
    kodi.addDir('Install ZIP from Online Link', '', 'urlzip', artwork + 'onlinesource.png',
                description='Manually download and install addons or repositories from the web.')
    viewsetter.set_view("sets")
# ****************************************************************


def _get_keyboard(default="", heading="", hidden=False):  # Start Ketboard Function
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        return unicode(keyboard.getText(), "utf-8")
    return default


def SEARCHADDON(url):  # Start Search Function
    vq = _get_keyboard(heading="Search add-ons")
    if (not vq):
        return False, 0
    title = urllib.quote_plus(vq)
    Get_search_results(title)


def Get_search_results(title):
    link = api.search_addons(title)
    my_list = sorted(link, key=lambda k: k['name'].upper())
    for e in link:
        name = e['name']
        repourl = e['repodlpath']
        path = e['addon_zip_path']
        description = e['description']
        icon = path.rsplit('/', 1)[0] + '/icon.png'
        fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'
        
        if e['extension_point'] != 'xbmc.addon.repository':
            try:
                addHELPDir(name, path, 'addoninstall', icon, fanart, description, 'addon', repourl, '', '', CMi,
                           contextreplace=False)
            except:
                pass
viewsetter.set_view("sets")

def github_main(url):
    if not xbmc.getCondVisibility('System.HasAddon(plugin.git.browser)'):
        if kodi.get_kversion() > 16:
            xbmc.executebuiltin("XBMC.InstallAddon(plugin.git.browser)")
        else:
            xbmc.executebuiltin("XBMC.RunPlugin(plugin://plugin.git.browser)")
    else:
        xbmc.executebuiltin("XBMC.Container.Update(plugin://plugin.git.browser)")

# ********************************************************************
def INTERNATIONAL():
    kodi.addDir('International Repos', '', 'interrepos',
                'https://www.tvaddons.co/kodi-addons/images/categories/international.png',
                description="Foreign language repos from across the globe!")
    kodi.addDir('International Addonss', '', 'interaddons',
                'https://www.tvaddons.co/kodi-addons/images/categories/international.png',
                description="Foreign language addons from across the globe!")


def INTERNATIONAL_REPOS():
    link = api.get_all_addons()
    for e in link:
        if e['repository_type'] == 'international' and e['extension_point'] == 'xbmc.addon.repository':
            # if e['extension_Point'] == 'xbmc.addon.repository':
            name = e['name']
            repourl = e['repodlpath']
            path = e['addon_zip_path']
            description = e['description']
            icon = path.rsplit('/', 1)[0] + '/icon.png'
            fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'
            try:
                addHELPDir(name, path, 'addoninstall', icon, fanart, description, 'addon', repourl, '', '', CMi,
                           contextreplace=False)
            except:
                pass


def INTERNATIONAL_ADDONS():
    imurl = 'https://www.tvaddons.co/kodi-addons/images/categories/international/'
    link = api.get_langs()
    if link:
        # for e in link:
            # name=e['languages']
            # kodi.log(name)
            l_vert = {"af": "African",
                      "ar": "Arabic",
                      # "cn": "Chinese",
                      "zh": "Chinese",
                      "cs": "Czech",
                      "da": "Danish",
                      "nl": "Dutch",
                      "ph": "Filipino",
                      "fi": "Finnish",
                      "fr": "French",
                      "de": "German",
                      "el": "Greek",
                      # "iw": "Hebrew",
                      "he": "Hebrew",
                      "hu": "Hungarian",
                      "is": "Icelandic",
                      "hi": "Indian",
                      "ga": "Irish",
                      "it": "Italian",
                      "ja": "Japanese",
                      "ko": "Korean",
                      "mn": "Mongolian",
                      "ne": "Nepali",
                      "no": "Norwegian",
                      "ur": "Pakistani",
                      "pl": "Polish",
                      "pt": "Portuguese",
                      "ro": "Romanian",
                      "ru": "Russian",
                      "ms": "Singapore",
                      "es": "Spanish",
                      "sv": "Swedish",
                      "ta": "Tamil",
                      "th": "Thai",
                      "tr": "Turkish",
                      "vi": "Vietnamese"}
            # for key in l_vert:
            #     if e['languages'] == key:
            #         full_name = l_vert[key]
            #         name = e['languages']
            #         try:
            #             kodi.addDir(full_name, name, 'interaddonslist', imurl + full_name.lower() + '.png',
            #                         description="Foreign language addons from across the globe!")
            #         except:
            #             pass
            #         viewsetter.set_view("sets")

            for key in sorted(l_vert.items(), key=lambda key: key[1]):
                try:
                    kodi.addDir(key[1], key[0], 'interaddonslist', imurl + key[1].lower() + '.png',
                                description="Foreign language addons from across the globe!")
                except:
                    pass
                viewsetter.set_view("sets")



def INTERNATIONAL_ADDONS_LIST(url):
    link = api.get_all_addons()
    my_list = sorted(link, key=lambda k: k['name'])
    for e in my_list:
        if url in e['languages']:
            name = e['name']
            repourl = e['repodlpath']
            path = e['addon_zip_path']
            description = e['description']
            icon = path.rsplit('/', 1)[0] + '/icon.png'
            fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'
            
            try:
                addHELPDir(name, path, 'addoninstall', icon, fanart, description, 'addon', repourl, '', '', CMi,
                           contextreplace=False)
            except:
                pass


def List_Addons(url):
    specials = ('featured', 'live', 'sports', 'playlists')
    regulars = ('video', 'executable')
    easyreg = ('audio', 'image', 'service', 'skins')
    if url in specials:
        query = url
        link = api.get_all_addons()
        feat = api.special_addons(query)
        my_list = sorted(link, key=lambda k: k['name'])
        for e in my_list:
            if e['id'] in feat:
                name = e['name']
                repourl = e['repodlpath']
                path = e['addon_zip_path']
                description = e['description']
                icon = path.rsplit('/', 1)[0] + '/icon.png'
                fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'
                try:
                    addHELPDir(name, path, 'addoninstall', icon, fanart, description, 'addon', repourl, '', '', CMi,
                               contextreplace=False)
                except:
                    pass
    
    if url in easyreg:
        link = api.get_types(url)
        my_list = sorted(link, key=lambda k: k['name'])
        for e in my_list:
            name = e['name']
            repourl = e['repodlpath']
            path = e['addon_zip_path']
            description = e['description']
            icon = path.rsplit('/', 1)[0] + '/icon.png'
            fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'
            try:
                addHELPDir(name, path, 'addoninstall', icon, fanart, description, 'addon', repourl, '', '', CMi,
                           contextreplace=False)
            except:
                pass
            
            # Split into ABC Menus
    if url in regulars:
        d = dict.fromkeys(string.ascii_uppercase, 0)
        my_list = sorted(d)
        for e in my_list:
            kodi.addDir(e, url, 'splitlist', artwork + e + '.png', description="Starts with letter " + e)
        kodi.addDir('Others', url, 'splitlist', artwork + 'symbols.png', description="Starts with another character")
    
    if url == 'repositories':
        link = api.get_repos()
        for e in link:
            name = e['name']
            repourl = e['repodlpath']
            path = e['addon_zip_path']
            description = e['description']
            icon = path.rsplit('/', 1)[0] + '/icon.png'
            fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'
            try:
                addHELPDir(name, path, 'addoninstall', icon, fanart, description, 'addon', 'None', '', '', CMi,
                           contextreplace=False)
            except:
                pass
    if url == 'skins':
        link = api.get_all_addons()
        my_list = sorted(link, key=lambda k: k['name'])
        for e in my_list:
            if e['extension_point'] == 'xbmc.gui.skin':
                name = e['name']
                repourl = e['repodlpath']
                path = e['addon_zip_path']
                description = e['description']
                icon = path.rsplit('/', 1)[0] + '/icon.png'
                fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'
                try:
                    addHELPDir(name, path, 'addoninstall', icon, fanart, description, 'addon', 'None', '', '', CMi,
                               contextreplace=False)
                except:
                    pass
    viewsetter.set_view("sets")


def Split_List(name, url):
    regulars = ('video', 'audio', 'image', 'service', 'executable', 'skins')
    letter = name
    if url in regulars:
        link = api.get_types(url)
        my_list = sorted(link, key=lambda k: k['name'])
        for e in my_list:
            name = e['name']
            repourl = e['repodlpath']
            path = e['addon_zip_path']
            description = e['description']
            icon = path.rsplit('/', 1)[0] + '/icon.png'
            fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'
            if letter == "Others":
                ALPHA = string.ascii_letters
                if name.startswith(tuple(ALPHA)) == False:
                    try:
                        addHELPDir(name, path, 'addoninstall', icon, fanart, description, 'addon', repourl, '', '', CMi,
                                   contextreplace=False)
                    except:
                        pass
            else:
                if name.lower().startswith(letter) or name.upper().startswith(letter):
                    try:
                        addHELPDir(name, path, 'addoninstall', icon, fanart, description, 'addon', repourl, '', '', CMi,
                                   contextreplace=False)
                    except:
                        pass


###<<<<<<<<<<<<<<ADULT SECTIONS>>>>>>>>>>>>>>>>>>>>>
def List_Adult(url):
    if settings.getSetting('adult') == 'true':
        confirm = xbmcgui.Dialog().yesno("Please Confirm",
                                         "                Please confirm that you are at least 18 years of age.",
                                         "                                       ", "              ", "NO (EXIT)",
                                         "YES (ENTER)")
        if confirm:
            url = 'https://indigo.tvaddons.co/installer/sources/xxx.php'
            link = OPEN_URL(url).replace('\r', '').replace('\n', '').replace('\t', '');
            match = re.compile(
                "'name' => '(.+?)'.+?dataUrl' => '(.+?)'.+?xmlUrl' => '(.+?)'.+?downloadUrl' => '(.+?)'").findall(link)
            for name, dataurl, url, repourl in match:
                lang = 'Adults Only'
                add2HELPDir(name + ' (' + lang + ')', url, 'getaddoninfo', '', fanart, dataurl, repourl)
                if len(match) == 0:
                    return
        else:
            kodi.set_setting('adult', 'false')
            return
        viewsetter.set_view("sets")


def getaddoninfo(url, dataurl, repourl):
    lang = 'Adults Only'
    link = OPEN_URL(url).replace('\r', '').replace('\n', '').replace('\t', '')
    match = re.compile('<addon id="(.+?)".+?ame="(.+?)".+?ersion="(.+?)"').findall(link)
    for adid, name, version in match:
        dload = dataurl + adid + "/" + adid + "-" + version + ".zip"
        addHELPDir(name + ' (' + lang + ')', dload, 'addoninstall', '', fanart, '', 'addon', repourl, '', '')
        viewsetter.set_view("sets")
    # ****************************************************************


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTB Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link


def EnableRTMP():
    try:
        addon_able.set_enabled("inputstream.adaptive")
    except:
        pass
    time.sleep(0.5)
    try:
        addon_able.set_enabled("inputstream.rtmp")
    except:
        pass
    time.sleep(0.5)
    xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
    dialog.ok("Operation Complete!", "Live Streaming has been Enabled!",
              "    Brought To You By %s " % siteTitle)


# ****************************************************************
def HUBINSTALL(name, url, script):
    aList = []
    script_url = url
    link = OPEN_URL(script_url)
    matcher = script + '-(.+?).zip'
    match = re.compile(matcher).findall(link)
    for version in match:
        aList.append(version)
    aList.sort(cmp=ver_cmp, reverse=True)
    newest_v = script + '-' + aList[0]
    newest_v_url = script_url + script + '-' + aList[0] + '.zip'
    kodi.log("Looking for : " + newest_v_url)
    path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("Starting up", "Initializing ", '', 'Please Stand By....')
    # lib = os.path.join(path, name + '.zip')
    lib = os.path.join(path, newest_v + '.zip')
    addonfolder = xbmc.translatePath(os.path.join('special://', 'home', 'addons'))
    if os.path.exists(lib):
        os.remove(lib)
    downloader.download(newest_v_url, lib, dp, timeout=120)
    try:
        # xbmc.executebuiltin("InstallAddon(%s)" % newest_v)
        extract.all(lib, addonfolder, '')
        time.sleep(2)
    except IOError, (errno, strerror):
        kodi.message("Failed to open required files", "Error code is:", strerror)
        return False

# ****************************************************************


def OPENSUBINSTALL(url):
    path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
    dp = xbmcgui.DialogProgress();
    dp.create("Please Wait", " ", '', 'Installing Official OpenSubtitles Addon')
    lib = os.path.join(path, 'opensubtitlesOfficial.zip')
    try:
        os.remove(lib)
    except:
        pass
    downloader.download(url, lib, dp, timeout=120)
    addonfolder = xbmc.translatePath(os.path.join('special://', 'home', 'addons'))
    time.sleep(2)
    try:
        extract.all(lib, addonfolder, '')
    except IOError, (errno, strerror):
        kodi.message("Failed to open required files", "Error code is:", strerror)
        return False
    xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
    addon_able.set_enabled("service.subtitles.opensubtitles_by_opensubtitles")
    dialog.ok("Installation Complete!", "    We hope you enjoy your Kodi addon experience!",
              "    Brought To You By %s " % siteTitle)


# #################################################################


# #****************************************************************
def set_content(content):
    xbmcplugin.setContent(int(sys.argv[1]), content)


# HELPDIR**************************************************************
def addDir(name, url, mode, thumb):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name);
    ok = True;
    liz = xbmcgui.ListItem(name, iconImage=iconart, thumbnailImage=thumb);
    # liz.setInfo(type="Video",infoLabels={"title":name,"Plot":description})
    try:
        liz.setProperty("fanart_image", fanart)
    except:
        pass
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True);
    return ok


def addHELPDir(name, url, mode, iconimage, fanart, description, filetype, repourl, version, author, contextmenuitems=[],
               contextreplace=False):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&fanart=" + urllib.quote_plus(
        fanart) + "&description=" + urllib.quote_plus(description) + "&filetype=" + urllib.quote_plus(
        filetype) + "&repourl=" + urllib.quote_plus(repourl) + "&author=" + urllib.quote_plus(
        author) + "&version=" + urllib.quote_plus(version)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=iconart, thumbnailImage=iconimage)  # "DefaultFolder.png"
    # if len(contextmenuitems) > 0:
    liz.addContextMenuItems(contextmenuitems, replaceItems=contextreplace)
    liz.setInfo(type="Video", infoLabels={"title": name, "plot": description})
    liz.setProperty("fanart_image", fanart)
    liz.setProperty("Addon.Description", description)
    liz.setProperty("Addon.Creator", author)
    liz.setProperty("Addon.Version", version)
    # properties={'Addon.Description':meta["plot"]}
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def add2HELPDir(name, url, mode, iconimage, fanart, description, filetype, contextmenuitems=[], contextreplace=False):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&fanart=" + urllib.quote_plus(
        fanart) + "&description=" + urllib.quote_plus(description) + "&filetype=" + urllib.quote_plus(filetype)
    ok = True;
    liz = xbmcgui.ListItem(name, iconImage=iconart, thumbnailImage=iconimage)
    # if len(contextmenuitems) > 0:
    liz.addContextMenuItems(contextmenuitems, replaceItems=contextreplace)
    liz.setInfo(type="Video", infoLabels={"title": name, "Plot": description})
    liz.setProperty("fanart_image", fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

###################### KEYMAP INSTALLER ####################
def keymaps():
    try:
        link = OPEN_URL(Keymaps_URL).replace('\n', '').replace('\r', '')
    except:
        kodi.addDir("No Keymaps Available", '', '', artwork + 'unkeymap.png')
        kodi.log('Could not open keymaps URL')
        return
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?ash="(.+?)"').findall(
        link)
    if os.path.isfile(KEYBOARD_FILE):
        kodi.addDir("Remove Current Keymap Configuration", '', 'uninstall_keymap', artwork + 'unkeymap.png')
    for name, url, iconimage, fanart, version, description in match:
        kodi.addDir(name, url, 'install_keymap', artwork + 'keymapadd.png')
        name = "[COLOR white][B]" + name + "[/B][/COLOR]"
    viewsetter.set_view("files")


def install_keymap(name, url):
    if os.path.isfile(KEYBOARD_FILE):
        try:
            os.remove(KEYBOARD_FILE)
        except:
            pass
    # Check is the packages folder exists, if not create it.
    path = xbmc.translatePath(os.path.join('special://home/addons', 'packages'))
    if not os.path.exists(path):
        os.makedirs(path)
    path_key = xbmc.translatePath(os.path.join('special://home/userdata', 'keymaps'))
    if not os.path.exists(path_key):
        os.makedirs(path_key)
    buildname = name
    dp = xbmcgui.DialogProgress()
    dp.create("Keymap Installer", "", "", "[B]Keymap: [/B]" + buildname)
    buildname = "customkeymap"
    lib = os.path.join(path, buildname + '.zip')
    
    try:
        os.remove(lib)
    except:
        pass
    
    downloader.download(url, lib, dp, timeout=120)
    addonfolder = xbmc.translatePath(os.path.join('special://', 'home'))
    time.sleep(2)
    dp.update(0, "", "Installing Please wait..", "")
    try:
        extract.all(lib, addonfolder, dp)
    except IOError, (errno, strerror):
        kodi.message("Failed to open required files", "Error code is:", strerror)
        return False
    time.sleep(1)
    try:
        os.remove(lib)
    except:
        pass
    
    xbmc.executebuiltin("Container.Refresh")
    dialog.ok("Custom Keymap Installed!", "     We hope you enjoy your Kodi addon experience!",
              "    Brought To You By %s " % siteTitle)


def uninstall_keymap():
    try:
        os.remove(KEYBOARD_FILE)
    except:
        pass
    
    dialog.ok(AddonTitle, "[B][COLOR white]Success, we have removed the keyboards.xml file.[/COLOR][/B]",
              '[COLOR white]Thank you for using %s[/COLOR]' % AddonTitle)


# xbmc.executebuiltin("Container.Refresh")


def libinstaller(name, url):
    if "Android" in name:
        if not xbmc.getCondVisibility('system.platform.android'):
            
            dialog.ok(AddonTitle + " - Android",
                      "[B][COLOR white]Sorry, this file is only for Android devices[/COLOR][/B]", '')
            sys.exit(1)
        else:
            name = "librtmp.so"
            path = xbmc.translatePath(os.path.join('special://home', ''))
            make_lib(path, name)
    
    if "Windows" in name:
        if not xbmc.getCondVisibility('system.platform.windows'):
            
            dialog.ok(AddonTitle + " -Windows",
                      "[B][COLOR white]Sorry, this file is only for Windows devices[/COLOR][/B]", '')
            return
        else:
            name = "librtmp.dll"
            path = xbmc.translatePath(os.path.join('special://home', ''))
            make_lib(path, name)
    
    if "Linux" in name:
        if not xbmc.getCondVisibility('system.platform.linux'):
            
            dialog.ok(AddonTitle + " - Linux", "[B][COLOR white]Sorry, this file is only for Linux devices[/COLOR][/B]",
                      '')
            return
        else:
            name = "librtmp.so.1"
            path = xbmc.translatePath(os.path.join('special://home', ''))
            make_lib(path, name)
    
    if "OSX" in name:
        if not xbmc.getCondVisibility('system.platform.osx'):
            
            dialog.ok(AddonTitle + " - MacOSX",
                      "[B][COLOR white]Sorry, this file is only for MacOSX devices[/COLOR][/B]", '')
            return
        else:
            name = "librtmp.1.dylib"
            path = xbmc.translatePath(os.path.join('special://home', ''))
            make_lib(path, name)
    
    if "TV" in name:
        if not xbmc.getCondVisibility('system.platform.atv2'):
            
            dialog.ok(AddonTitle + " - ATV", "[B][COLOR white]Sorry, this file is only for ATV devices[/COLOR][/B]", '')
            return
        else:
            name = "librtmp.1.dylib"
            path = xbmc.translatePath(os.path.join('special://home', ''))
            make_lib(path, name)
    
    if "iOS" in name:
        if not xbmc.getCondVisibility('system.platform.ios'):
            
            dialog.ok(AddonTitle + " - iOS", "[B][COLOR white]Sorry, this file is only for iOS devices[/COLOR][/B]", '')
            return
        else:
            name = "librtmp.1.dylib"
            path = xbmc.translatePath(os.path.join('special://home', ''))
            make_lib(path, name)
    
    if "RPi" in name:
        if not xbmc.getCondVisibility('system.platform.rpi'):
            
            dialog.ok(AddonTitle + " - RPi", "[B][COLOR white]Sorry, this file is only for RPi devices[/COLOR][/B]", '')
            return
        else:
            name = "librtmp.1.so"
            path = xbmc.translatePath(os.path.join('special://home', ''))
            make_lib(path, name)


def make_lib(path, name):
    addon_title = AddonTitle + " Installer"
    dp = xbmcgui.DialogProgress()
    dp.create(addon_title, "", "", "")
    lib = os.path.join(path, name)
    try:
        os.remove(lib)
    except:
        pass
    downloader.download(url, lib, dp)
    dialog.ok(addon_title, "[COLOR gold]Download complete, File can be found at: [/COLOR][COLOR blue]" + lib + "[/COLOR]")


##############
def ver_cmp(x, y):
    for i, j in izip_longest(*[x.split('.'), y.split('.')], fillvalue=0):
        if int(i) < int(j):
            return -1
        elif int(i) > int(j):
            return 1
    return 0


# New Dependency Routine #####################
def NEW_Depend(dataurl, script):
    kodi.log("SCRIPT LOOKED FOR IS : " + script)
    if "github" in dataurl:
        kodi.log("Is Github Repo")
        GITHUBGET(script, dataurl)
    else:
        kodi.log("Is Private Repo")
        try:
            aList = []
            link = OPEN_URL(tvpath)
            if script in link:
                script_url = tvpath + script + '/'
                link = OPEN_URL(script_url)
                matcher = script + '-(.+?).zip'
                match = re.compile(matcher).findall(link)
                for version in match:
                    aList.append(version)
                aList.sort(cmp=ver_cmp, reverse=True)
                orglist = script_url + script + '-' + aList[0] + '.zip'
                kodi.log(' DOWNLOADING TVA FILE to ' + script + '.zip')
                DEPENDINSTALL(script, orglist)
            else:
                link = OPEN_URL(krypton_url)
                if script in link:
                    script_url = krypton_url + script + '/'
                    link = OPEN_URL(script_url)
                    matcher = script + '-(.+?).zip'
                    match = re.compile(matcher).findall(link)
                    for version in match:
                        aList.append(version)
                    aList.sort(cmp=ver_cmp, reverse=True)
                    orglist = script_url + script + '-' + aList[0] + '.zip'
                    kodi.log(' DOWNLOADING ORG FILE to ' + script + '.zip')
                    DEPENDINSTALL(script, orglist)
                else:
                    try:
                        script_urls = dataurl + script + '/'
                        link = OPEN_URL(script_urls)
                        if not link:
                            script_url = script_urls.replace("raw.", "").replace("/master/", "/tree/master/")
                            link = OPEN_URL(script_url)
                        if "Invalid request" in link:
                            kodi.log("DEAD REPO LOCATION = " + dataurl)
                        else:
                            matcher = script + '-(.+?).zip'
                            match = re.compile(matcher).findall(link)
                            for version in match:
                                aList.append(version)
                            aList.sort(cmp=ver_cmp, reverse=True)
                            orglist = dataurl + script + '/' + script + '-' + aList[0] + '.zip'
                            kodi.log(' DOWNLOADING NATIVE to ' + script + '.zip')
                            DEPENDINSTALL(script, orglist)
                    except:
                        kodi.log("No local depend found = " + script + " Unfound URL is " + orglist)
        except:
            kodi.log("FAILED TO GET DEPENDS")


def GITHUBGET(script, dataurl):
    try:
        fix_urls = dataurl + script + '/'
        fixed_url = fix_urls.replace("raw/", "").replace("/master/", "/blob/master/").replace("githubusercontent", "github")
        aList = []
        link = OPEN_URL(tvpath)
        if script in link:
            script_url = tvpath + script + '/'
            link = OPEN_URL(script_url)
            matcher = script + '-(.+?).zip'
            match = re.compile(matcher).findall(link)
            for version in match:
                aList.append(version)
            aList.sort(cmp=ver_cmp, reverse=True)
            orglist = script_url + script + '-' + aList[0] + '.zip'
            kodi.log(' DOWNLOADING TVA FILE to ' + script + '.zip')
            DEPENDINSTALL(script, orglist)
        else:
            link = OPEN_URL(krypton_url)
            if script in link:
                script_url = krypton_url + script + '/'
                link = OPEN_URL(script_url)
                matcher = script + '-(.+?).zip'
                match = re.compile(matcher).findall(link)
                for version in match:
                    aList.append(version)
                aList.sort(cmp=ver_cmp, reverse=True)
                orglist = script_url + script + '-' + aList[0] + '.zip'
                kodi.log(' DOWNLOADING ORG FILE to ' + script + '.zip')
                # kodi.log('From: '+orglist)
                DEPENDINSTALL(script, orglist)
            else:
                try:
                    link = OPEN_URL(fixed_url)
                    if link:
                        matcher = script + '-(.+?).zip'
                        match = re.compile(matcher).findall(link)
                        for version in match:
                            aList.append(version)
                        # aList.sort(cmp=ver_cmp, reverse=True)
                        aList.sort(reverse=True)
                        orglist = dataurl + script + '/' + script + '-' + aList[0] + '.zip'
                        # kodi.log(' DOWNLOADING to ' + script + '.zip')
                        DEPENDINSTALL(script, orglist)
                        kodi.log("TRYING NATIVE LOCATION")
                    if "Invalid request" in link:
                        kodi.log("DEAD REPO LOCATION = " + dataurl)
                    else:
                        matcher = script + '-(.+?).zip'
                        match = re.compile(matcher).findall(link)
                        for version in match:
                            aList.append(version)
                        # aList.sort(cmp=ver_cmp, reverse=True)
                        aList.sort(reverse=True)
                        orglist = dataurl + script + '/' + script + '-' + aList[0] + '.zip'
                        kodi.log(' DOWNLOADING NATIVE to ' + script + '.zip')
                        DEPENDINSTALL(script, orglist)
                except:
                    kodi.log("Could not find required files ")
    except:
        kodi.log("Failed to find required files")


def DEPENDINSTALL(name, url):
    path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
    lib = os.path.join(path, name + '.zip')
    addonfolder = xbmc.translatePath(os.path.join('special://', 'home', 'addons'))
    try:
        os.remove(lib)
    except:
        pass
    download(url, lib, addonfolder, name)

    addon_able.set_enabled(name)
    xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
#################################################################


def ADDONINSTALL(name, url, description, filetype, repourl, Auto=False, v='', vO=''):
    try:
        name = name.split('[COLOR FF0077D7]Install [/COLOR][COLOR FFFFFFFF]')[1].split('[/COLOR][COLOR FF0077D7] (v')[0]
    except:
        pass
    kodi.log("Installer: Installing: " + name)
    newfile = '-'.join(url.split('/')[-1].split('-')[:-1])
    addonname = str(newfile).replace('[', '').replace(']', '').replace('"', '').replace('[', '').replace("'", '')
    path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
    confirm = xbmcgui.Dialog().yesno("Please Confirm", "                Do you wish to install the chosen add-on and",
                                     "                        its respective repository if needed?              ",
                                     "                             ", "Cancel", "Install")
    if confirm:
        dp.create("Download Progress:", "", '', 'Please Wait')
        lib = os.path.join(path, name + '.zip')
        try:
            os.remove(lib)
        except:
            pass
        addonfolder = xbmc.translatePath(os.path.join('special://', 'home', 'addons'))
        download(url, lib, addonfolder, name)
        try:
            addonname = re.match('(.+)(-\d+\.)', addonname).group(1)
        except:
            pass
        # extract.all(lib, addonfolder, '')
        addon_able.set_enabled(name)
        xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
        xbmc.executebuiltin("XBMC.UpdateAddonRepos()")
        try:
            dataurl = repourl.split("repository", 1)[0]

            # Start Addon Depend Search ==================================================================
            # Handles the addons/dependencies that have the version in the addon name
            try:
                addonname = re.match('(.+)(-\d+\.)', addonname).group(1)
            except:
                pass
            depends = xbmc.translatePath(os.path.join('special://home', 'addons', addonname, 'addon.xml'))
            source = open(depends, mode='r')
            link = source.read()
            source.close()
            dmatch = re.compile('import addon="(.+?)"').findall(link)
            for requires in dmatch:
                if not 'xbmc.python' in requires:
                    if not 'xbmc.gui' in requires:
                        dependspath = xbmc.translatePath(os.path.join('special://home/addons', requires))
                        if not os.path.exists(dependspath):
                            NEW_Depend(dataurl, requires)
                            Deep_Depends(dataurl, requires)
                        # name, url = NEW_Depend(dataurl,requires)
                        # DEPENDINSTALL(name,url)
        except:
            traceback.print_exc(file=sys.stdout)
        # # End Addon Depend Search ======================================================================

        kodi.log("STARTING REPO INSTALL")
        kodi.log("Installer: Repo is : " + repourl)
        if repourl:
            if 'None' not in repourl:
                path = xbmc.translatePath(os.path.join('special://home/addons', 'packages'))
                # lib = os.path.join(path, name + '.zip')
                files = repourl.split('/')
                dependname = files[-1:]
                dependname = str(dependname)
                reponame = dependname.split('-')
                nextname = reponame[:-1]
                nextname = str(nextname).replace('[', '').replace(']', '').replace('"', '').replace('[', '')\
                    .replace("'", '').replace(".zip", '')
                lib = os.path.join(path, nextname + '.zip')
                kodi.log("REPO TO ENABLE IS  " + nextname)
                try:
                    os.remove(lib)
                except:
                    pass
                addonfolder = xbmc.translatePath(os.path.join('special://', 'home/addons'))
                # download(repourl, lib, addonfolder, name)
                download(repourl, lib, addonfolder, nextname)
                addon_able.set_enabled(nextname)

        addon_able.set_enabled(addonname)
        xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
        xbmc.executebuiltin("XBMC.UpdateAddonRepos()")
        if not dialog.yesno(siteTitle, '                     Click Continue to install more addons or',
                            '                    Restart button to finalize addon installation',
                            "                          Brought To You By %s " % siteTitle,
                            nolabel='Restart', yeslabel='Continue'):
            xbmc.executebuiltin('ShutDown')
    else:
        return


def Deep_Depends(dataurl, addonname):
    depends = xbmc.translatePath(os.path.join('special://home', 'addons', addonname, 'addon.xml'))
    source = open(depends, mode='r')
    link = source.read()
    source.close()
    dmatch = re.compile('import addon="(.+?)"').findall(link)
    for requires in dmatch:
        if not 'xbmc.python' in requires:
            dependspath = xbmc.translatePath(os.path.join('special://home/addons', requires))
            if not os.path.exists(dependspath):
                NEW_Depend(dataurl, requires)


def install_from_url():
    zip_url = ''
    if not zip_url:
        zip_url = _get_keyboard(zip_url, 'Enter the URL of the addon/repository ZIP file you wish to install', hidden=False)
    if zip_url:
        name = os.path.basename(zip_url)
        ADDONINSTALL(name, zip_url, '', '', '', True, '', '')

# ****************************************************************


def download(url, dest, addonfolder, name):
    kodi.log(' DOWNLOADING FILE:' + name + '.zip')
    kodi.log('From: ' + url)
    dp.update(0, "Downloading: " + name, '', 'Please Wait')
    urllib.urlretrieve(url, dest, lambda nb, bs, fs, url=url: _pbhook(nb, bs, fs, url, dp))
    extract.all(dest, addonfolder, dp=None)


def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
        percent = min((numblocks * blocksize * 100) / filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled():
        raise Exception("Canceled")
        dp.close()
        
        
        # def chunks(data, SIZE=10000):
        #     it = iter(data)
        #     for i in xrange(0, len(data), SIZE):
        #         yield {k:data[k] for k in islice(it, SIZE)}
