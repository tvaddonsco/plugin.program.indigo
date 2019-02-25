# TVADDONS.CO / TVADDONS.CO - Addon Installer - Module By: Blazetamer (2013-2016)

# import base64
import downloader
import extract
import os
import re
# import ssl
import string
import sys
import time
import urllib
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import traceback
from itertools import izip_longest

from libs import addon_able
from libs import aiapi
from libs import kodi
from libs import viewsetter


# if kodi.get_kversion() > 16.5:
#     ssl._create_default_https_context = ssl._create_unverified_context
# else:
#     pass

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
# dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
# <<<<<<<<<Common Variables>>>>>>>>>>>>>>>
# Keymaps_URL = base64.b64decode("aHR0cDovL2luZGlnby50dmFkZG9ucy4va2V5bWFwcy9jdXN0b21rZXlzLnR4dA==")
Keymaps_URL = 'http://indigo.tvaddons.co/keymaps/customkeys.txt'
KEYBOARD_FILE = xbmc.translatePath(os.path.join('special://home/userdata/keymaps/', 'keyboard.xml'))
openSub = "https://github.com/tvaddonsco/tva-release-repo/raw/master/service.subtitles.opensubtitles_by_opensubtitles/"
burst_url = "http://burst.surge.sh/release/script.quasar.burst-0.5.8.zip"
# tvpath = "https://oldgit.com/tvaresolvers/tva-common-repository/raw/master/zips/"
tvpath = "https://github.com/tvaddonsco/tva-resolvers-repo/raw/master/zips"
tva_repo = 'https://github.com/tvaddonsco/tva-release-repo/tree/master/'
kodi_url = "http://mirrors.kodi.tv/addons/" + kodi.get_codename().lower() + '/'
api = aiapi
CMi = []


# ****************************************************************
def get_params():
    param = []
    # dialog.ok('', str(sys.argv), str(addon))
    # if sys.argv == ['']:
    #     sys.argv = ['plugin://' + addon_id + '/', '2', '?content_type=video']
    try:
        paramstring = sys.argv[2]
    except Exception as e:
        kodi.log(str(e))
        paramstring = '?content_type=video'
    # paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = paramstring  # sys.argv[2]
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


params = get_params()
# url = None
# name = None
# mode = None
# year = None
# imdb_id = None


# ****************************************************************
def MAININDEX():
    xbmc.executebuiltin("UpdateAddonRepos")
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
    if keyboard.isConfirmed():
        return keyboard.getText().decode('utf-8')  # unicode(keyboard.getText(), "utf-8")
    return default


def SEARCHADDON(url):  # Start Search Function
    vq = _get_keyboard(heading="Search add-ons")
    if not vq:
        return False, 0
    title = urllib.quote_plus(vq)
    Get_search_results(title)


def Get_search_results(title):
    link = api.search_addons(title)
    # my_list = sorted(link, key=lambda k: k['name'].upper())
    # for e in my_list:
    for e in link:
        name = e['name']
        repourl = e['repodlpath']
        path = e['addon_zip_path']
        description = e['description']
        icon = path.rsplit('/', 1)[0] + '/icon.png'
        l_fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'

        if e['extension_point'] != 'xbmc.addon.repository':
            try:
                addHELPDir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', repourl, '', '', CMi,
                           contextreplace=False)
            except Exception as e:
                kodi.log(str(e))


viewsetter.set_view("sets")


def github_main(url):
    try:
        kodi.log('github_main ' + str(xbmc.getCondVisibility('System.HasAddon(repository.xbmchub)')))
        if not xbmc.getCondVisibility('System.HasAddon(plugin.git.browser)'):
            if kodi.get_kversion() > 16:
                xbmc.executebuiltin("InstallAddon(plugin.git.browser)")
                timeout = time.time() + 15
                while not xbmc.getCondVisibility('System.HasAddon(plugin.git.browser)'):
                    xbmc.sleep(1000)
                    if time.time() > timeout:
                        break
                xbmc.executebuiltin("RunAddon(plugin.git.browser)")
            else:
                xbmc.executebuiltin("XBMC.RunPlugin(plugin://plugin.git.browser)")
        else:
            xbmc.executebuiltin("XBMC.Container.Update(plugin://plugin.git.browser)")
    except:
        traceback.print_exc(file=sys.stdout)


# ********************************************************************
def INTERNATIONAL():
    kodi.addDir('International Repos', '', 'interrepos',
                'https://www.tvaddons.co/kodi-addons/images/categories/international.png',
                description="Foreign language repos from across the globe!")
    kodi.addDir('International Addons', '', 'interaddons',
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
            l_fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'
            try:
                addHELPDir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', repourl, '', '', CMi,
                           contextreplace=False)
            except Exception as e:
                kodi.log(str(e))


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
            for key in sorted(l_vert.items(), key=lambda key: key[1]):
                kodi.addDir(key[1], key[0], 'interaddonslist', imurl + key[1].lower() + '.png',
                            description="Foreign language addons from across the globe!")
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
            l_fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'

            try:
                addHELPDir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', repourl, '', '', CMi,
                           contextreplace=False)
            except Exception as e:
                kodi.log(str(e))


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
                l_fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'
                try:
                    addHELPDir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', repourl, '', '', CMi,
                               contextreplace=False)
                except Exception as e:
                    kodi.log(str(e))

    if url in easyreg:
        link = api.get_types(url)
        my_list = sorted(link, key=lambda k: k['name'])
        for e in my_list:
            name = e['name']
            repourl = e['repodlpath']
            path = e['addon_zip_path']
            description = e['description']
            icon = path.rsplit('/', 1)[0] + '/icon.png'
            l_fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'
            try:
                addHELPDir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', repourl, '', '', CMi,
                           contextreplace=False)
            except Exception as e:
                kodi.log(str(e))

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
            # repourl = e['repodlpath']
            path = e['addon_zip_path']
            description = e['description']
            icon = path.rsplit('/', 1)[0] + '/icon.png'
            l_fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'
            try:
                addHELPDir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', 'None', '', '', CMi,
                           contextreplace=False)
            except Exception as e:
                kodi.log(str(e))
    if url == 'skins':
        link = api.get_all_addons()
        my_list = sorted(link, key=lambda k: k['name'])
        for e in my_list:
            if e['extension_point'] == 'xbmc.gui.skin':
                name = e['name']
                # repourl = e['repodlpath']
                path = e['addon_zip_path']
                description = e['description']
                icon = path.rsplit('/', 1)[0] + '/icon.png'
                l_fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'
                try:
                    addHELPDir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', 'None', '', '', CMi,
                               contextreplace=False)
                except Exception as e:
                    kodi.log(str(e))
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
            l_fanart = path.rsplit('/', 1)[0] + '/fanart.jpg'
            if letter == "Others":
                alpha = string.ascii_letters
                if name.startswith(tuple(alpha)) is False:
                    try:
                        addHELPDir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', repourl, '', '',
                                   CMi, contextreplace=False)
                    except Exception as e:
                        kodi.log(str(e))
            else:
                if name.lower().startswith(letter) or name.upper().startswith(letter):
                    try:
                        addHELPDir(name, path, 'addoninstall', icon, fanart, description, 'addon', repourl, '', '', CMi,
                                   contextreplace=False)
                    except Exception as e:
                        kodi.log(str(e))


# ##<<<<<<<<<<<<<<ADULT SECTIONS>>>>>>>>>>>>>>>>>>>>>
def List_Adult(url):
    if settings.getSetting('adult') == 'true':
        confirm = xbmcgui.Dialog().yesno("Please Confirm",
                                         "                Please confirm that you are at least 18 years of age.",
                                         "                                       ", "              ", "NO (EXIT)",
                                         "YES (ENTER)")
        if confirm:
            url = 'https://indigo.tvaddons.co/installer/sources/xxx.php'
            link = kodi.open_url(url).replace('\r', '').replace('\n', '').replace('\t', '')
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
    link = kodi.open_url(url).replace('\r', '').replace('\n', '').replace('\t', '')
    match = re.compile('<addon id="(.+?)".+?ame="(.+?)".+?ersion="(.+?)"').findall(link)
    for adid, name, version in match:
        dload = dataurl + adid + "/" + adid + "-" + version + ".zip"
        addHELPDir(name + ' (' + lang + ')', dload, 'addoninstall', '', fanart, '', 'addon', repourl, '', '')
        viewsetter.set_view("sets")
    # ****************************************************************


def EnableRTMP():
    try:
        addon_able.set_enabled("inputstream.adaptive")
    except Exception as e:
        kodi.log(str(e))
    time.sleep(0.5)
    try:
        addon_able.set_enabled("inputstream.rtmp")
    except Exception as e:
        kodi.log(str(e))
    time.sleep(0.5)
    xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
    dialog.ok("Operation Complete!", "Live Streaming has been Enabled!",
              "    Brought To You By %s " % siteTitle)


# ****************************************************************
def HUBINSTALL(name, url, script):
    a_list = []
    script_url = url
    link = kodi.open_url(script_url)
    matcher = script + '-(.+?).zip'
    match = re.compile(matcher).findall(link)
    for version in match:
        a_list.append(version)
    a_list.sort(cmp=ver_cmp, reverse=True)
    newest_v = script + '-' + a_list[0]
    newest_v_url = script_url + script + '-' + a_list[0] + '.zip'
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
    except IOError as e:
        kodi.message("Failed to open required files", "Error is: ", str(e))
        return False
    # except IOError, (errno, strerror):
    #     kodi.message("Failed to open required files", "Error code is:", strerror)
    #     return False

# ****************************************************************


def OPENSUBINSTALL(url):
    path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("Please Wait", " ", '', 'Installing Official OpenSubtitles Addon')
    lib = os.path.join(path, 'opensubtitlesOfficial.zip')
    try:
        os.remove(lib)
    except OSError:
        pass
    page = kodi.open_url(url)
    url += re.search('''title="([^z]*zip)''', page).group(1)
    downloader.download(url, lib, dp, timeout=120)
    addonfolder = xbmc.translatePath(os.path.join('special://', 'home', 'addons'))
    time.sleep(2)
    try:
        extract.all(lib, addonfolder, '')
    except IOError as e:
        kodi.message("Failed to open required files", "Error is: ", str(e))
        return False
    # except IOError, (errno, strerror):
    #     kodi.message("Failed to open required files", "Error code is:", strerror)
    #     return False
    #
    xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
    addon_able.set_enabled("service.subtitles.opensubtitles_by_opensubtitles")
    xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
    dialog.ok("Installation Complete!", "    We hope you enjoy your Kodi addon experience!",
              "    Brought To You By %s " % siteTitle)


# #################################################################


# #****************************************************************
def set_content(content):
    xbmcplugin.setContent(int(sys.argv[1]), content)


# HELPDIR**************************************************************
def addDir(name, url, mode, thumb):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    # ok = True
    liz = xbmcgui.ListItem(name, iconImage=iconart, thumbnailImage=thumb)
    # liz.setInfo(type="Video",infoLabels={"title":name,"Plot":description})
    try:
        liz.setProperty("fanart_image", fanart)
    except Exception as e:
        kodi.log(str(e))
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addHELPDir(name, url, mode, iconimage, fanart, description, filetype, repourl, version, author, contextmenuitems=[],
               contextreplace=False):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&fanart=" + urllib.quote_plus(
        fanart) + "&description=" + urllib.quote_plus(description) + "&filetype=" + urllib.quote_plus(
        filetype) + "&repourl=" + urllib.quote_plus(repourl) + "&author=" + urllib.quote_plus(
        author) + "&version=" + urllib.quote_plus(version)
    # ok = True
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
    # ok = True
    liz = xbmcgui.ListItem(name, iconImage=iconart, thumbnailImage=iconimage)
    # if len(contextmenuitems) > 0:
    liz.addContextMenuItems(contextmenuitems, replaceItems=contextreplace)
    liz.setInfo(type="Video", infoLabels={"title": name, "Plot": description})
    liz.setProperty("fanart_image", fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


# ##################### KEYMAP INSTALLER ####################
def keymaps():
    try:
        link = kodi.open_url(Keymaps_URL).replace('\n', '').replace('\r', '')
    except IOError:
        kodi.addDir("No Keymaps Available", '', '', artwork + 'unkeymap.png')
        kodi.log('Could not open keymaps URL')
        return
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?ash="(.+?)"').findall(
        link)
    if os.path.isfile(KEYBOARD_FILE):
        kodi.addDir("Remove Current Keymap Configuration", '', 'uninstall_keymap', artwork + 'unkeymap.png')
    for name, url, iconimage, fanart, version, description in match:
        name = "[COLOR white][B]" + name + "[/B][/COLOR]"
        kodi.addDir(name, url, 'install_keymap', artwork + 'keymapadd.png')
    viewsetter.set_view("files")


def install_keymap(name, url):
    if os.path.isfile(KEYBOARD_FILE):
        try:
            os.remove(KEYBOARD_FILE)
        except OSError:
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
    except OSError:
        pass

    downloader.download(url, lib, dp, timeout=120)
    addonfolder = xbmc.translatePath(os.path.join('special://', 'home'))
    time.sleep(2)
    dp.update(0, "", "Installing Please wait..", "")
    try:
        extract.all(lib, addonfolder, dp)
    except IOError as e:
        kodi.message("Failed to open required files", "Error is: ", str(e))
        return False
    # except IOError, (errno, strerror):
    #     kodi.message("Failed to open required files", "Error code is:", strerror)
    #     return False

    time.sleep(1)
    try:
        os.remove(lib)
    except OSError:
        pass

    xbmc.executebuiltin("Container.Refresh")
    dialog.ok("Custom Keymap Installed!", "     We hope you enjoy your Kodi addon experience!",
              "    Brought To You By %s " % siteTitle)


def uninstall_keymap():
    try:
        os.remove(KEYBOARD_FILE)
    except OSError:
        pass

    dialog.ok(AddonTitle, "[B][COLOR white]Success, we have removed the keyboards.xml file.[/COLOR][/B]",
              '[COLOR white]Thank you for using %s[/COLOR]' % AddonTitle)


# xbmc.executebuiltin("Container.Refresh")


def libinstaller(name, url=None):
    if "Android" in name:
        if not xbmc.getCondVisibility('system.platform.android'):

            dialog.ok(AddonTitle + " - Android",
                      "[B][COLOR white]Sorry, this file is only for Android devices[/COLOR][/B]", '')
            sys.exit(1)
        else:
            name = "librtmp.so"
            path = xbmc.translatePath(os.path.join('special://home', ''))
            make_lib(path, name, url)

    if "Windows" in name:
        if not xbmc.getCondVisibility('system.platform.windows'):

            dialog.ok(AddonTitle + " -Windows",
                      "[B][COLOR white]Sorry, this file is only for Windows devices[/COLOR][/B]", '')
            return
        else:
            name = "librtmp.dll"
            path = xbmc.translatePath(os.path.join('special://home', ''))
            make_lib(path, name, url)

    if "Linux" in name:
        if not xbmc.getCondVisibility('system.platform.linux'):

            dialog.ok(AddonTitle + " - Linux", "[B][COLOR white]Sorry, this file is only for Linux devices[/COLOR][/B]",
                      '')
            return
        else:
            name = "librtmp.so.1"
            path = xbmc.translatePath(os.path.join('special://home', ''))
            make_lib(path, name, url)

    if "OSX" in name:
        if not xbmc.getCondVisibility('system.platform.osx'):

            dialog.ok(AddonTitle + " - MacOSX",
                      "[B][COLOR white]Sorry, this file is only for MacOSX devices[/COLOR][/B]", '')
            return
        else:
            name = "librtmp.1.dylib"
            path = xbmc.translatePath(os.path.join('special://home', ''))
            make_lib(path, name, url)

    if "TV" in name:
        if not xbmc.getCondVisibility('system.platform.atv2'):

            dialog.ok(AddonTitle + " - ATV", "[B][COLOR white]Sorry, this file is only for ATV devices[/COLOR][/B]", '')
            return
        else:
            name = "librtmp.1.dylib"
            path = xbmc.translatePath(os.path.join('special://home', ''))
            make_lib(path, name, url)

    if "iOS" in name:
        if not xbmc.getCondVisibility('system.platform.ios'):

            dialog.ok(AddonTitle + " - iOS", "[B][COLOR white]Sorry, this file is only for iOS devices[/COLOR][/B]", '')
            return
        else:
            name = "librtmp.1.dylib"
            path = xbmc.translatePath(os.path.join('special://home', ''))
            make_lib(path, name, url)

    if "RPi" in name:
        if not xbmc.getCondVisibility('system.platform.rpi'):

            dialog.ok(AddonTitle + " - RPi", "[B][COLOR white]Sorry, this file is only for RPi devices[/COLOR][/B]", '')
            return
        else:
            name = "librtmp.1.so"
            path = xbmc.translatePath(os.path.join('special://home', ''))
            make_lib(path, name, url)


def make_lib(path, name, url=None):
    addon_title = AddonTitle + " Installer"
    dp = xbmcgui.DialogProgress()
    dp.create(addon_title, "", "", "")
    lib = os.path.join(path, name)
    try:
        os.remove(lib)
    except OSError:
        pass
    downloader.download(url, lib, dp)
    dialog.ok(addon_title, "[COLOR gold]Download complete, File can be found at: [/COLOR][COLOR blue]" + lib +
              "[/COLOR]")


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
            a_list = []
            link = kodi.open_url(tvpath)
            if script in link:
                script_url = tvpath + script + '/'
                link = kodi.open_url(script_url)
                matcher = script + '-(.+?).zip'
                match = re.compile(matcher).findall(link)
                for version in match:
                    a_list.append(version)
                a_list.sort(cmp=ver_cmp, reverse=True)
                orglist = script_url + script + '-' + a_list[0] + '.zip'
                kodi.log(' DOWNLOADING TVA FILE to ' + script + '.zip')
                DEPENDINSTALL(script, orglist)
            else:
                link = kodi.open_url(kodi_url)
                if script in link:
                    script_url = kodi_url + script + '/'
                    link = kodi.open_url(script_url)
                    matcher = script + '-(.+?).zip'
                    match = re.compile(matcher).findall(link)
                    for version in match:
                        a_list.append(version)
                    a_list.sort(cmp=ver_cmp, reverse=True)
                    orglist = script_url + script + '-' + a_list[0] + '.zip'
                    kodi.log(' DOWNLOADING ORG FILE to ' + script + '.zip')
                    DEPENDINSTALL(script, orglist)
                else:
                    orglist = dataurl + script + '/' + script + '-'
                    try:
                        script_urls = dataurl + script + '/'
                        link = kodi.open_url(script_urls)
                        if not link:
                            script_url = script_urls.replace("raw.", "").replace("/master/", "/tree/master/")
                            link = kodi.open_url(script_url)
                        if "Invalid request" in link:
                            kodi.log("DEAD REPO LOCATION = " + dataurl)
                        else:
                            matcher = script + '-(.+?).zip'
                            match = re.compile(matcher).findall(link)
                            for version in match:
                                a_list.append(version)
                            a_list.sort(cmp=ver_cmp, reverse=True)
                            orglist += a_list[0] + '.zip'
                            kodi.log(' DOWNLOADING NATIVE to ' + script + '.zip')
                            DEPENDINSTALL(script, orglist)
                    except Exception as e:
                        kodi.log(str(e))
                        kodi.log("No local depend found = " + script + " Unfound URL is " + orglist)
        except Exception as e:
            kodi.log(str(e))
            kodi.log("FAILED TO GET DEPENDS")
            traceback.print_exc(file=sys.stdout)


def GITHUBGET(script, dataurl):
    try:
        fix_urls = dataurl + script + '/'
        fixed_url = fix_urls.replace("raw/", "").replace("/master/", "/blob/master/")\
            .replace("githubusercontent", "github")
        a_list = []
        link = kodi.open_url(tvpath)
        if script in link:
            script_url = tvpath + script + '/'
            link = kodi.open_url(script_url)
            matcher = script + '-(.+?).zip'
            match = re.compile(matcher).findall(link)
            for version in match:
                a_list.append(version)
            a_list.sort(cmp=ver_cmp, reverse=True)
            orglist = script_url + script + '-' + a_list[0] + '.zip'
            kodi.log(' DOWNLOADING TVA FILE to ' + script + '.zip')
            DEPENDINSTALL(script, orglist)
        else:
            link = kodi.open_url(kodi_url)
            if script in link:
                script_url = kodi_url + script + '/'
                link = kodi.open_url(script_url)
                matcher = script + '-(.+?).zip'
                match = re.compile(matcher).findall(link)
                for version in match:
                    a_list.append(version)
                a_list.sort(cmp=ver_cmp, reverse=True)
                orglist = script_url + script + '-' + a_list[0] + '.zip'
                kodi.log(' DOWNLOADING ORG FILE to ' + script + '.zip')
                # kodi.log('From: '+orglist)
                DEPENDINSTALL(script, orglist)
            else:
                try:
                    link = kodi.open_url(fixed_url)
                    if link:
                        matcher = script + '-(.+?).zip'
                        match = re.compile(matcher).findall(link)
                        for version in match:
                            a_list.append(version)
                        # a_list.sort(cmp=ver_cmp, reverse=True)
                        a_list.sort(reverse=True)
                        orglist = dataurl + script + '/' + script + '-' + a_list[0] + '.zip'
                        # kodi.log(' DOWNLOADING to ' + script + '.zip')
                        DEPENDINSTALL(script, orglist)
                        kodi.log("TRYING NATIVE LOCATION")
                    if "Invalid request" in link:
                        kodi.log("DEAD REPO LOCATION = " + dataurl)
                    else:
                        matcher = script + '-(.+?).zip'
                        match = re.compile(matcher).findall(link)
                        for version in match:
                            a_list.append(version)
                        # a_list.sort(cmp=ver_cmp, reverse=True)
                        a_list.sort(reverse=True)
                        orglist = dataurl + script + '/' + script + '-' + a_list[0] + '.zip'
                        kodi.log(' DOWNLOADING NATIVE to ' + script + '.zip')
                        DEPENDINSTALL(script, orglist)
                except Exception as e:
                    kodi.log("Could not find required files " + str(e))
                    traceback.print_exc(file=sys.stdout)
    except Exception as e:
        kodi.log("Failed to find required files " + str(e))
        traceback.print_exc(file=sys.stdout)


def DEPENDINSTALL(name, url):
    path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
    lib = os.path.join(path, name + '.zip')
    addonfolder = xbmc.translatePath(os.path.join('special://', 'home', 'addons'))
    try:
        os.remove(lib)
    except OSError:
        pass
    download(url, lib, addonfolder, name)
    addon_able.set_enabled(name)
    xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
#################################################################


def ADDONINSTALL(name, url, description, filetype, repourl, Auto=False, v='', vO=''):
    try:
        name = name.split('[COLOR FF0077D7]Install [/COLOR][COLOR FFFFFFFF]')[1].split('[/COLOR][COLOR FF0077D7] (v')[0]
    except Exception as e:
        kodi.log(str(e))
        traceback.print_exc(file=sys.stdout)
    kodi.log("Installer: Installing: " + name)
    addonname = '-'.join(url.split('/')[-1].split('-')[:-1])
    addonname = str(addonname).replace('[', '').replace(']', '').replace('"', '').replace('[', '').replace("'", '')
    try:
        addonname = re.search('(.+?)($|-\d+\.)', addonname).group(1)
    except Exception as e:
        kodi.log(str(e))
        traceback.print_exc(file=sys.stdout)
    path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
    if xbmcgui.Dialog().yesno("Please Confirm", "                Do you wish to install the chosen add-on and",
                              "                        its respective repository if needed?",
                              "                            ", "Cancel", "Install"):
        if 'tva-release-repo' in url:
            url = get_max_version(addonname, url, tva_repo)
        dp = xbmcgui.DialogProgress()
        dp.create("Download Progress:", "", '', 'Please Wait')
        lib = os.path.join(path, name + '.zip')
        try:
            os.remove(lib)
        except OSError:
            pass
        addonfolder = xbmc.translatePath(os.path.join('special://', 'home', 'addons'))
        download(url, lib, addonfolder, name)
        addon_able.set_enabled(addonname)
        try:
            dataurl = repourl.split("repository", 1)[0]

            # Start Addon Depend Search ==================================================================
            depends = xbmc.translatePath(os.path.join('special://home', 'addons', addonname, 'addon.xml'))
            source = open(depends, mode='r')
            link = source.read()
            source.close()
            dmatch = re.compile('import addon="(.+)"').findall(link)
            for requires in dmatch:
                if 'xbmc.python' not in requires:
                    if 'xbmc.gui' not in requires:
                        dependspath = xbmc.translatePath(os.path.join('special://home/addons', requires))
                        if not os.path.exists(dependspath):
                            NEW_Depend(dataurl, requires)
                            Deep_Depends(dataurl, requires)
        except Exception as e:
            kodi.log(str(e))
            traceback.print_exc(file=sys.stdout)
        # # End Addon Depend Search ======================================================================

        kodi.log("STARTING REPO INSTALL")
        kodi.log("Installer: Repo is : " + repourl)
        if repourl:
            if 'None' not in repourl:
                path = xbmc.translatePath(os.path.join('special://home/addons', 'packages'))
                repo_name = str(repourl.split('/')[-1:]).split('-')[:-1]
                repo_name = str(repo_name).replace('[', '').replace(']', '').replace('"', '').replace('[', '')\
                    .replace("'", '').replace(".zip", '')
                if 'tva-release-repo' in repourl:
                    repourl = get_max_version(repo_name, repourl, tva_repo)
                lib = os.path.join(path, repo_name + '.zip')
                try:
                    os.remove(lib)
                except Exception as e:
                    kodi.log(str(e))
                addonfolder = xbmc.translatePath(os.path.join('special://', 'home/addons'))
                download(repourl, lib, addonfolder, repo_name)
                kodi.log("REPO TO ENABLE IS  " + repo_name)
                addon_able.set_enabled(repo_name)

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
        if 'xbmc.python' not in requires:
            dependspath = xbmc.translatePath(os.path.join('special://home/addons', requires))
            if not os.path.exists(dependspath):
                NEW_Depend(dataurl, requires)


def install_from_url():
    zip_url = ''
    if not zip_url:
        zip_url = _get_keyboard(zip_url, 'Enter the URL of the addon/repository ZIP file you wish to install',
                                hidden=False)
    if zip_url:
        name = os.path.basename(zip_url)
        ADDONINSTALL(name, zip_url, '', '', '', True, '', '')

# ****************************************************************


def download(url, dest, addonfolder, name):
    kodi.log(' DOWNLOADING FILE:' + name + '.zip')
    kodi.log('From: ' + url)
    dp = xbmcgui.DialogProgress()
    dp.create("Downloading: " + name)
    dp.update(0, "Downloading: " + name, '', 'Please Wait')
    urllib.urlretrieve(url, dest, lambda nb, bs, fs, url=url: _pbhook(nb, bs, fs, url, dp))
    kodi.log("DOWNLOAD IS DONE  " + name)
    extract.all(dest, addonfolder, dp=None)



def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
        percent = min((numblocks * blocksize * 100) / filesize, 100)
    except Exception as e:
        kodi.log(str(e))
        percent = 100
    dp.update(percent)
    if dp.iscanceled():
        dp.close()
        raise Exception("Canceled")
        
        # def chunks(data, SIZE=10000):
        #     it = iter(data)
        #     for i in xrange(0, len(data), SIZE):
        #         yield {k:data[k] for k in islice(it, SIZE)}


def get_max_version(repo_name, repourl, tree_url):
    version = re.search(repo_name + '(-.+?).zip', repourl).group(1)
    version_max = max(re.findall(repo_name + '(-.+?).zip', kodi.read_file(tree_url + repo_name)))
    return repourl.replace(version, version_max)
