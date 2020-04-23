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

from libs import addon_able
from libs import aiapi
from libs import kodi
from libs import viewsetter

try:
    from itertools import izip_longest
except ImportError:
    from itertools import zip_longest as izip_longest

    try:
        from urllib import urlretrieve as urlretrieve
    except ImportError:
        from urllib.request import urlretrieve as urlretrieve

try:
    quote_plus = urllib.quote_plus
except AttributeError:
    quote_plus = urllib.parse.quote_plus

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
artwork1 = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'art/'))
artwork = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'art2/'))
mainPath = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id))
packages_path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
addon_folder = xbmc.translatePath(os.path.join('special://', 'home', 'addons'))
fanart = xbmc.translatePath(os.path.join(mainPath, 'fanart.jpg'))
iconart = xbmc.translatePath(os.path.join(mainPath, 'icon.png'))
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
        gparams = paramstring  # sys.argv[2]
        cleanedparams = gparams.replace('?', '')
        if cleanedparams[len(cleanedparams) - 1] == '/':
            cleanedparams = cleanedparams[0:len(cleanedparams) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


params = get_params()


# ****************************************************************
def main_index():
    xbmc.executebuiltin("UpdateAddonRepos")
    kodi.add_item("Git Browser", '', 'github_main', artwork + 'github_browser.png',
                 description="Search for repositories hosted on GitHub.")
    try:
        if len(str(api.get_all_addons())) < 20:
            raise ValueError('API is less than 20')
        kodi.add_dir('Search by: Addon/Author', '', 'searchaddon', artwork + 'search.png',
                    description="Search for addons by Name or Author")
        if settings.getSetting('featured') == 'true':
            kodi.add_dir('Featured Addons', 'featured', 'addonlist', artwork + 'featured.png',
                        description="The most popular Kodi addons!")
        # if settings.getSetting('livetv') == 'true':
        #     kodi.add_dir('Live TV Addons', 'live', 'addonlist', artwork + 'livetv.png',
        #                 description="The most popular live TV addons!")
        # if settings.getSetting('sports') == 'true':
        #     kodi.add_dir('Sports Addons', 'sports', 'addonlist', artwork + 'sports.png',
        #                 description="The most popular sports addons!")
        if settings.getSetting('video') == 'true':
            kodi.add_dir('Video Addons', 'video', 'addonlist', artwork + 'video.png',
                        description="Every video addon in existence!")
        if settings.getSetting('audio') == 'true':
            kodi.add_dir('Audio Addons', 'audio', 'addonlist', artwork + 'audio.png',
                        description="Find addons to listen to music!")
        if settings.getSetting('program') == 'true':
            kodi.add_dir('Program Addons', 'executable', 'addonlist', artwork + 'program.png',
                        description="Every program addon you can imagine!")
        # if settings.getSetting('playlist') == 'true':
        #     kodi.add_dir('Playlist Addons', 'playlists', 'addonlist', artwork + 'playlists.png',
        #                 description="The most popular playlist addons!")
        if settings.getSetting('services') == 'true':
            kodi.add_dir('Service Addons', 'service', 'addonlist', artwork + 'service.png')
        if settings.getSetting('skincat') == 'true':
            kodi.add_dir('Kodi Skins', 'skins', 'addonlist', artwork + 'kodi_skins.png',
                        description="Change up your look!")
        if settings.getSetting('world') == 'true':
            kodi.add_dir('International Addons', 'international', 'interlist', artwork + 'world.png',
                        description="Foreign language addons and repos from across the globe!")
        if settings.getSetting('adult') == 'true':
            kodi.add_dir('Adult Addons', 'xxx', 'adultlist', artwork + 'adult.png',
                        description="Must be 18 years or older! This menu can be disabled from within Add-on Settings.")
        # if settings.getSetting('repositories') == 'true':
        # 	kodi.add_dir('Repositories','repositories', 'addonlist', artwork + 'repositories.png',
        # 				description="Browse addons by repository!")
    except Exception as e:
        kodi.log(str(e))
        traceback.print_exc(file=sys.stdout)
        kodi.add_item("Addon Listing Is Temporarily Unavailable", '', '', artwork1 + 'addon_installer.png',
                     description="The Addon Listing Is Temporarily Unavailable")
    # kodi.add_item('Enable Live Streaming', 'None', 'EnableRTMP', artwork + 'enablertmp.png',
    # 			 description="Enable RTMP InputStream and InputStream Adaptive modules for Live Streaming.")
    kodi.add_item('Official OpenSubtitles Addon', openSub, 'addopensub', artwork + 'opensubicon.png',
                 description="Install Official OpenSubtitles Addon!")
    kodi.add_dir('Install ZIP from Online Link', '', 'urlzip', artwork + 'onlinesource.png',
                description='Manually download and install addons or repositories from the web.')
    viewsetter.set_view("sets")
# ****************************************************************


# Start Keyboard Function
def _get_keyboard(default="", heading="", hidden=False):
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText().decode('utf-8')  # unicode(keyboard.getText(), "utf-8")
    return default


def search_addon():  # Start Search Function
    vq = _get_keyboard(heading="Search add-ons")
    if not vq:
        return False, 0
    title = quote_plus(vq)
    # title = urllib.parse.quote_plus(vq)
    get_search_results(title)


def get_search_results(title):
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
                add_help_dir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', repourl, '', '', CMi,
                             contextreplace=False)
            except Exception as e:
                kodi.log(str(e))
    viewsetter.set_view("sets")


def github_main():
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
    except Exception as e:
        kodi.log(str(e))
        traceback.print_exc(file=sys.stdout)


# ********************************************************************
def international():
    kodi.add_dir('International Repos', '', 'interrepos',
                'https://www.tvaddons.co/kodi-addons/images/categories/international.png',
                description="Foreign language repos from across the globe!")
    kodi.add_dir('International Addons', '', 'interaddons',
                'https://www.tvaddons.co/kodi-addons/images/categories/international.png',
                description="Foreign language addons from across the globe!")


def international_repos():
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
                add_help_dir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', repourl, '', '', CMi,
                             contextreplace=False)
            except Exception as e:
                kodi.log(str(e))


def international_addons():
    imurl = 'https://www.tvaddons.co/kodi-addons/images/categories/international/'
    link = api.get_langs()
    if link:
        # for e in link:
        #     name=e['languages']
        #     kodi.log(name)
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
        for lang in sorted(l_vert.items(), key=lambda key: lang[1]):
            kodi.add_dir(lang[1], lang[0], 'interaddonslist', imurl + lang[1].lower() + '.png',
                        description="Foreign language addons from across the globe!")
            viewsetter.set_view("sets")


def international_addons_list(url):
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
                add_help_dir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', repourl, '', '', CMi,
                             contextreplace=False)
            except Exception as e:
                kodi.log(str(e))


def list_addons(url):
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
                    add_help_dir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', repourl, '', '', CMi,
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
                add_help_dir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', repourl, '', '', CMi,
                             contextreplace=False)
            except Exception as e:
                kodi.log(str(e))

            # Split into ABC Menus
    if url in regulars:
        d = dict.fromkeys(string.ascii_uppercase, 0)
        my_list = sorted(d)
        for e in my_list:
            kodi.add_dir(e, url, 'splitlist', artwork + e + '.png', description="Starts with letter " + e)
        kodi.add_dir('Others', url, 'splitlist', artwork + 'symbols.png', description="Starts with another character")

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
                add_help_dir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', 'None', '', '', CMi,
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
                    add_help_dir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', 'None', '', '', CMi,
                                 contextreplace=False)
                except Exception as e:
                    kodi.log(str(e))
    viewsetter.set_view("sets")


def split_list(name, url):
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
                        add_help_dir(name, path, 'addoninstall', icon, l_fanart, description, 'addon', repourl, '', '',
                                     CMi, contextreplace=False)
                    except Exception as e:
                        kodi.log(str(e))
            else:
                if name.lower().startswith(letter) or name.upper().startswith(letter):
                    try:
                        add_help_dir(name, path, 'addoninstall', icon, fanart, description, 'addon', repourl, '', '',
                                     CMi, contextreplace=False)
                    except Exception as e:
                        kodi.log(str(e))


# ##<<<<<<<<<<<<<<ADULT SECTIONS>>>>>>>>>>>>>>>>>>>>>
def list_adult():
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
                add_2help_dir(name + ' (' + lang + ')', url, 'getaddoninfo', '', fanart, dataurl, repourl)
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
        add_help_dir(name + ' (' + lang + ')', dload, 'addoninstall', '', fanart, '', 'addon', repourl, '', '')
        viewsetter.set_view("sets")


# ****************************************************************
def enable_rtmp():
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
    dialog.ok("Operation Complete!", "Live Streaming has been Enabled!",
              "    Brought To You By %s " % siteTitle)


# ****************************************************************
def get_url(script, source_url, source):
    match = re.findall(script + '(-.+?)?.zip', source)
    match.sort(reverse=True)
    version = match[0] if match else ''
    newest_v_url = source_url + script + version + '.zip'
    return version, newest_v_url


# ****************************************************************
def hub_install(script, script_url, silent=False, dp=None):
    version, newest_v_url = get_url(script, script_url, kodi.open_url(script_url))
    kodi.log("Looking for : " + newest_v_url)
    if not silent:
        dp = xbmcgui.DialogProgress()
        dp.create("Starting up", "Initializing ", '', 'Please Stand By....')
    lib = os.path.join(packages_path, script + version + '.zip')
    os.remove(lib) if os.path.exists(lib) else ''
    downloader.download(newest_v_url, lib, dp, timeout=120)
    try:
        extract.extract_all(lib, addon_folder, None)
        time.sleep(2)
    except IOError as e:
        kodi.message("Failed to open required files", "Error is: ", str(e))
        return False


# ****************************************************************
def open_sub_install(url):
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
        extract.extract_all(lib, addonfolder, '')
    except IOError as e:
        kodi.message("Failed to open required files", "Error is: ", str(e))
        return False
    # except IOError, (errno, strerror):
    #     kodi.message("Failed to open required files", "Error code is:", strerror)
    #     return False
    #
    addon_able.set_enabled("service.subtitles.opensubtitles_by_opensubtitles")
    dialog.ok("Installation Complete!", "    We hope you enjoy your Kodi addon experience!",
              "    Brought To You By %s " % siteTitle)


# #################################################################


# #****************************************************************
def set_content(content):
    xbmcplugin.setContent(int(sys.argv[1]), content)


# HELPDIR**************************************************************
def add_dir(name, url, mode, thumb):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode) + "&name=" + quote_plus(name)
    # ok = True
    liz = xbmcgui.ListItem(name, iconImage=iconart, thumbnailImage=thumb)
    # liz.setInfo(type="Video",infoLabels={"title":name,"Plot":description})
    try:
        liz.setProperty("fanart_image", fanart)
    except Exception as e:
        kodi.log(str(e))
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def add_help_dir(name, url, mode, iconimage, art, description, filetype, repourl, version, author,
                 contextmenuitems=None, contextreplace=False):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode) + "&name=" + quote_plus(
        name) + "&iconimage=" + quote_plus(iconimage) + "&fanart=" + quote_plus(
        art) + "&description=" + quote_plus(description) + "&filetype=" + quote_plus(
        filetype) + "&repourl=" + quote_plus(repourl) + "&author=" + quote_plus(
        author) + "&version=" + quote_plus(version)
    contextmenuitems = [] if not contextmenuitems else contextmenuitems
    liz = xbmcgui.ListItem(name, iconImage=iconart, thumbnailImage=iconimage)  # "DefaultFolder.png"
    # if len(contextmenuitems) > 0:
    liz.addContextMenuItems(contextmenuitems, replaceItems=contextreplace)
    liz.setInfo(type="Video", infoLabels={"title": name, "plot": description})
    liz.setProperty("fanart_image", art)
    liz.setProperty("Addon.Description", description)
    liz.setProperty("Addon.Creator", author)
    liz.setProperty("Addon.Version", version)
    # properties={'Addon.Description':meta["plot"]}
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def add_2help_dir(name, url, mode, iconimage, art, description, filetype, contextmenuitems=None, contextreplace=False):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode) + "&name=" + quote_plus(
        name) + "&iconimage=" + quote_plus(iconimage) + "&fanart=" + quote_plus(
        art) + "&description=" + quote_plus(description) + "&filetype=" + quote_plus(filetype)
    liz = xbmcgui.ListItem(name, iconImage=iconart, thumbnailImage=iconimage)
    contextmenuitems = [] if not contextmenuitems else contextmenuitems
    liz.addContextMenuItems(contextmenuitems, replaceItems=contextreplace)
    liz.setInfo(type="Video", infoLabels={"title": name, "Plot": description})
    liz.setProperty("fanart_image", art)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


# ##################### KEYMAP INSTALLER ####################
def keymaps():
    try:
        link = kodi.open_url(Keymaps_URL).replace('\n', '').replace('\r', '')
    except IOError:
        kodi.add_dir("No Keymaps Available", '', '', artwork + 'unkeymap.png')
        kodi.log('Could not open keymaps URL')
        return
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?ash="(.+?)"').findall(
        link)
    if os.path.isfile(KEYBOARD_FILE):
        kodi.add_dir("Remove Current Keymap Configuration", '', 'uninstall_keymap', artwork + 'unkeymap.png')
    for name, url, iconimage, art, version, description in match:
        name = "[COLOR white][B]" + name + "[/B][/COLOR]"
        kodi.add_dir(name, url, 'install_keymap', artwork + 'keymapadd.png')
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
        extract.extract_all(lib, addonfolder, dp)
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


# New Dependency Routine #####################
def new_depend(dataurl, script):
    kodi.log("SCRIPT LOOKED FOR IS : " + script)
    if "github" in dataurl:
        kodi.log("Is Github Repo")
        get_github(script, dataurl)
    else:
        kodi.log("Is Private Repo")
        try:
            link = kodi.open_url(tvpath)
            if script in link:
                script_url = tvpath + script + '/'
                version, orglist = get_url(script, script_url, link)
                kodi.log(' DOWNLOADING TVA FILE to ' + script + version + '.zip')
                depend_install(script, orglist)
            else:
                link = kodi.open_url(kodi_url)
                if script in link:
                    script_url = kodi_url + script + '/'
                    version, orglist = get_url(script, script_url, link)
                    kodi.log(' DOWNLOADING Kodi FILE to ' + script + version + '.zip')
                    depend_install(script, orglist)
                else:
                    orglist = dataurl + script + '/' + script
                    try:
                        script_urls = dataurl + script + '/'
                        link = kodi.open_url(script_urls)
                        if not link:
                            script_urls = script_urls.replace("raw.", "").replace("/master/", "/tree/master/")
                            link = kodi.open_url(script_urls)
                        if link and "Invalid request" not in link:
                            version, orglist = get_url(script, script_urls, link)
                            orglist += version + '.zip'
                            kodi.log(' DOWNLOADING NATIVE to ' + script + version + '.zip')
                            depend_install(script, orglist)
                        else:
                            kodi.log("DEAD REPO LOCATION = " + dataurl)
                    except Exception as e:
                        kodi.log(str(e))
                        kodi.log("No local depend found = " + script + " Unfound URL is " + orglist)
        except Exception as e:
            kodi.log(str(e))
            kodi.log("FAILED TO GET DEPENDS")
            traceback.print_exc(file=sys.stdout)


def get_github(script, dataurl):
    try:
        link = kodi.open_url(tvpath)
        if script in link:
            script_url = tvpath + script + '/'
            version, orglist = get_url(script, script_url, link)
            kodi.log(' DOWNLOADING TVA FILE to ' + script + version + '.zip')
            depend_install(script, orglist)
        else:
            link = kodi.open_url(kodi_url)
            if script in link:
                script_url = kodi_url + script + '/'
                version, orglist = get_url(script, script_url, link)
                kodi.log(' DOWNLOADING KODI FILE to ' + script + version + '.zip')
                depend_install(script, orglist)
            else:
                fix_urls = dataurl + script + '/'
                fixed_url = fix_urls.replace("raw/", "").replace("/master/", "/blob/master/") \
                    .replace("githubusercontent", "github")
                link = kodi.open_url(fixed_url)
                if link and "Invalid request" not in link:
                    version, orglist = get_url(script, fixed_url, link)
                    kodi.log(' DOWNLOADING NATIVE to ' + script + version + '.zip')
                    depend_install(script, orglist)
                else:
                    fixed_url = fix_urls.replace("raw/", "").replace("/master/", "/tree/master/") \
                        .replace("githubusercontent", "github")
                    link = kodi.open_url(fixed_url)
                    if link and "Invalid request" not in link:
                        version, orglist = get_url(script, fixed_url, link)
                        kodi.log(' DOWNLOADING NATIVE to ' + script + version + '.zip')
                        depend_install(script, orglist)
                    else:
                        kodi.log("DEAD REPO LOCATION = " + dataurl)
    except Exception as e:
        kodi.log("Failed to find required files " + str(e))
        traceback.print_exc(file=sys.stdout)


def depend_install(name, url):
    path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
    lib = os.path.join(path, name + '.zip')
    addonfolder = xbmc.translatePath(os.path.join('special://', 'home', 'addons'))
    try:
        os.remove(lib)
    except OSError:
        pass
    download(url, lib, addonfolder, name)
    addon_able.set_enabled(name)
#################################################################


def addon_install(name, url, repourl):
    try:
        name = name.split('[COLOR FF0077D7]Install [/COLOR][COLOR FFFFFFFF]')[1].split('[/COLOR][COLOR FF0077D7] (v')[0]
    except Exception as e:
        kodi.log(str(e))
        traceback.print_exc(file=sys.stdout)
    kodi.log("Installer: Installing: " + name)
    addonname = '-'.join(url.split('/')[-1].split('-')[:-1])
    addonname = str(addonname).replace('[', '').replace(']', '').replace('"', '').replace('[', '').replace("'", '')
    try:
        addonname = re.search('(.+?)($|-)', addonname).group(1)
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
                            new_depend(dataurl, requires)
                            deep_depends(dataurl, requires)
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

        if not dialog.yesno(siteTitle, '                     Click Continue to install more addons or',
                            '                    Restart button to finalize addon installation',
                            "                          Brought To You By %s " % siteTitle,
                            nolabel='Restart', yeslabel='Continue'):
            xbmc.executebuiltin('ShutDown')
    else:
        return


def deep_depends(dataurl, addonname):
    depends = xbmc.translatePath(os.path.join('special://home', 'addons', addonname, 'addon.xml'))
    source = open(depends, mode='r')
    link = source.read()
    source.close()
    dmatch = re.compile('import addon="(.+?)"').findall(link)
    for requires in dmatch:
        if 'xbmc.python' not in requires:
            dependspath = xbmc.translatePath(os.path.join('special://home/addons', requires))
            if not os.path.exists(dependspath):
                new_depend(dataurl, requires)


def install_from_url():
    zip_url = ''
    if not zip_url:
        zip_url = _get_keyboard(zip_url, 'Enter the URL of the addon/repository ZIP file you wish to install',
                                hidden=False)
    if zip_url:
        name = os.path.basename(zip_url)
        addon_install(name, zip_url, '')

# ****************************************************************


def download(url, dest, addonfolder, name):
    kodi.log(' DOWNLOADING FILE:' + name + '.zip')
    kodi.log('From: ' + url)
    dp = xbmcgui.DialogProgress()
    dp.create("Downloading: " + name)
    dp.update(0, "Downloading: " + name, '', 'Please Wait')
    urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp))
    kodi.log("DOWNLOAD IS DONE  " + name)
    extract.extract_all(dest, addonfolder, dp=None)


def _pbhook(numblocks, blocksize, filesize, dp):
    try:
        percent = min((numblocks * blocksize * 100) / filesize, 100)
    except Exception as e:
        kodi.log(str(e))
        percent = 100
    dp.update(int(percent))
    if dp.iscanceled():
        dp.close()
        raise Exception("Canceled")


def get_max_version(repo_name, repourl, tree_url):
    version = re.search(repo_name + '(-.+?).zip', repourl).group(1)
    version_max = max(re.findall(repo_name + '(-.+?).zip', kodi.read_file(tree_url + repo_name)))
    return repourl.replace(version, version_max)
