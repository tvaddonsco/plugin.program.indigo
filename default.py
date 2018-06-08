# -*- coding: utf-8 -*-
# import base64
import htmlentitydefs
import os
import re
import shutil
import sys
import urllib
# import urllib2

import configwizard
import textviewer
import backup
import downloader
import extract
import freshstart
import installer
import maintool

import xbmc
import xbmcgui
import xbmcplugin
from libs import requests
from libs import addon_able
from libs import dom_parser
from libs import kodi
from libs import speedtest
from libs import viewsetter

addon_id = kodi.addon_id
addon = (addon_id, sys.argv)
artwork = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'art/'))
AddonTitle = kodi.addon.getAddonInfo('name')
addon_path = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id))
packagepath = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
ART = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'art/'))
ART2 = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'art2/'))
ART3 = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'art3/'))
fanart = artwork+'fanart.jpg'
messages = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'resources', 'messages/'))
execute = xbmc.executebuiltin
hubpath = xbmc.translatePath(os.path.join('special://home', 'addons', 'repository.xbmchub'))
uploaderpath = xbmc.translatePath(os.path.join('special://home', 'addons', 'script.tvaddons.debug.log'))

oldinstaller = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.program.addoninstaller'))
oldnotify = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.program.xbmchub.notifications'))
oldmain = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.xbmchubmaintenance'))
oldwiz = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.hubwizard'))
oldfresh = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.freshstart'))
oldmain2 = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.hubmaintenance'))


def get_kversion():
    full_version_info = xbmc.getInfoLabel('System.BuildVersion')
    baseversion = full_version_info.split(".")
    # intbase = int(baseversion[0])
    return baseversion[0]
    
    
def main_menu():
    maintool.source_change()
    maintool.feed_change()
    # ########## TRY POP ########
    if len(kodi.get_setting('notify')) > 0:
        kodi.set_setting('notify', str(int(kodi.get_setting('notify')) + 1))
    else:
        kodi.set_setting('notify', "1")
    if int(kodi.get_setting('notify')) == 1:
        xbmcgui.Dialog().notification('Need Support?', 'www.tvaddons.co', artwork + 'icon.png', 3000, False)
    elif int(kodi.get_setting('notify')) == 5:
        kodi.set_setting('notify', "0")
    # ######## END POP ###########

    if kodi.get_setting('hasran') == 'false':
        kodi.set_setting('hasran', 'true')
        
    dp = xbmcgui.DialogProgress()
    try:
        if (not os.path.exists(ART)) or (not os.path.exists(ART2)) or (not os.path.exists(ART3)):
            dp.create(AddonTitle, 'Getting ' + AddonTitle + ' Ready......', 'Downloading ' + AddonTitle + ' Icons.....')
            dp.update(0)
            icons_zip = os.path.join(packagepath, AddonTitle + '_icons.zip')
            downloader.download(OPEN_URL('http://indigo.tvaddons.co/graphics/arts.txt'), icons_zip, dp)
            dp.update(0, 'Getting %s Ready........' % AddonTitle, 'Extracting %s Icons......' % AddonTitle)
            extract.all(icons_zip, addon_path, dp)
            dp.close()
    except:
        pass
    # Check for old version of hubrepo and remove it
    try:
        if os.path.exists(hubpath):
            with open(hubpath, 'r') as content:
                if 'AG' in content:
                    shutil.rmtree(hubpath)
    except:
        pass
    # # Check for HUBRepo and install it
    try:
        if not os.path.exists(hubpath):
            installer.HUBINSTALL('repository.xbmchub', 'http://github.com/tvaddonsco/tva-release-repo/raw/master/'
                                                       'repository.xbmchub/', 'repository.xbmchub')
            xbmc.executebuiltin("XBMC.InstallAddon(%s)" % 'repository.xbmchub')
            addon_able.set_enabled("repository.xbmchub")
            xbmc.executebuiltin("XBMC.UpdateAddonRepos()")
    except:
        pass
    # Check for Log Uploader and install it
    try:
        if not os.path.exists(uploaderpath):
            installer.HUBINSTALL('script.tvaddons.debug.log', 'http://github.com/tvaddonsco/tva-release-repo/raw/master'
                                                              '/script.tvaddons.debug.log/', 'script.tvaddons.debug.log')
            addon_able.set_enabled('script.tvaddons.debug.log')
            # xbmc.executebuiltin("InstallAddon(%s)" % 'script.tvaddons.debug.log')
            xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
    except:
        pass
   
    # Check for old maintenance tools and remove them
    old_maintenance = (oldinstaller, oldnotify, oldmain, oldwiz, oldfresh)
    for old_file in old_maintenance:
        if os.path.exists(old_file):
            shutil.rmtree(old_file)

    # Notification Status
    if kodi.get_setting("notifications-on-startup") == "false":
        note_status = '(Opt Out)'
        note_art = 'notification_optout.png'
        note_description = 'Unsubscribe'
    else:
        note_status = '(Opt In)'
        note_art = 'notification_in.png'
        note_description = 'Subscribe'

    if kodi.get_setting('wizardran') == 'false':
        kodi.addItem("Config Wizard", '', 'call_wizard', artwork+'config_wizard.png',
                     description="Automatically configure Kodi with the best addons and goodies in seconds!")
    kodi.addDir("Addon Installer", '', 'call_installer', artwork + 'addon_installer.png',
                description="It’s like an App Store for Kodi addons!")
    kodi.addDir("Maintenance Tools", '', 'call_maintool', artwork + 'maintool.png',
                description="Keep your Kodi setup running at optimum performance!")
    # kodi.addDir("Kodi Librtmp Files", '', 'get_libs', artwork +'librtmp_files.png')
    kodi.addItem("Rejuvenate Kodi", '', 'call_rejuv', artwork + 'rejuvinate.png',
                 description="Wipe and reconfigure Kodi with the latest Config Wizard setup!")
    kodi.addDir("Factory Restore", '', 'call_restore', artwork + 'factory_restore.png',
                description="Start off fresh, wipe your Kodi setup clean!")
    if os.path.exists(uploaderpath):
        kodi.addItem("Log Uploader", '', 'log_upload', artwork + 'log_uploader.png',
                     description="Easily upload your error logs for troubleshooting!")
    kodi.addDir("Network Speed Test", '', 'runspeedtest', artwork + 'speed_test.png',
                description="How fast is your internet?")
    kodi.addDir("System Information", '', 'system_info', artwork + 'system_info.png',
                description="Useful information about your Kodi setup!")
    kodi.addDir("Sports Listings", '', 'call_sports', artwork + 'sports_list.png',
                description="Who’s playing what today?")
    kodi.addDir('Backup / Restore', '', 'backup_restore', artwork + 'backup_restore.png',
                description="Backup or restore your Kodi configuration in minutes!")
    kodi.addItem("Log Viewer", '', 'log_view', artwork + 'log_viewer.png',
                 description="Easily view your error log without leaving Kodi!")
    kodi.addItem("Notifications " + note_status, '', 'toggle_notify', artwork + note_art,
                 description="%s to important TV ADDONS notifications on startup!" % note_description)
    kodi.addItem("Show Notification", '', 'show_note', artwork + 'notification.png',
                 description="Show TVA Notification. To get Important News, Tips, and Giveaways from TV ADDONS")
    viewsetter.set_view("sets")


def do_log_uploader():
    xbmc.executebuiltin("RunAddon(script.tvaddons.debug.log)")


def what_sports():
    link = OPEN_URL('http://www.wheresthematch.com/tv/home.asp').replace('\r', '').replace('\n', '').replace('\t', '')
    match = re.compile('href="http://www.wheresthematch.com/fixtures/(.+?).asp.+?class="">(.+?)</em> <em class="">v</'
                       'em> <em class="">(.+?)</em>.+?time-channel ">(.+?)</span>').findall(link)
    for game, name1, name2, gametime in match:
        kodi.addItem('[COLOR gold][B]%s[/COLOR][/B][COLOR white] - %s vs %s - %s[/COLOR]'
                     % (game, name1, name2, gametime), '', '', artwork+'icon.png',
                     description='[COLOR gold][B]%s[/COLOR][/B][COLOR white] - %s vs %s - %s[/COLOR]'
                                 % (game, name1, name2, gametime))
        xbmc.executebuiltin("Container.SetViewMode(55)")

    # #######  AMERICAN  ###############
    link = OPEN_URL('http://www.tvguide.com/sports/live-today/').replace('\r', '').replace('\n', '').replace('\t', '')
    sections = dom_parser.parse_dom(link, 'div', {'class': "listings-program-content"})
    # listings = dom_parser.parse_dom(sections, 'span', {'class': "listings-program-link"})
    for stuff in sections:
        match = re.compile('class="listings-program-link">(.+?)</span></h3>.+?class="listings-program-link">.+?listings'
                           '-program-airing-info">(.+?)</p><p.+?description">(.+?)</p>').findall(stuff)
        for name, time, description in match:
            kodi.addItem('[COLOR gold][B]%s[/COLOR][/B][COLOR white] - %s[/COLOR]'
                         % (name_cleaner(name), time), '', '', artwork+'icon.png',
                         description='[COLOR gold][B]%s[/COLOR][/B][COLOR white] - %s[/COLOR]'
                                     % (name_cleaner(name), time))
    # viewsetter.set_view("files")


def rtmp_lib():
    liblist = "http://indigo.tvaddons.co/librtmp/rtmplist.txt"
    try:
        link = OPEN_URL(liblist).replace('\n', '').replace('\r', '')
    except:
        kodi.addItem('[COLOR gold][B]This service is currently unavailable.[/COLOR][/B]', '', 100, '', '', '')
        return
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?ersion="(.+?)"').findall(link)
    kodi.addItem('[COLOR gold][B]Files Will Be Donwloaded to the Kodi Home directory,'
                 'You Will Need To Manually Install From There.[/COLOR][/B]', '', 100, '', '', '')
    # kodi.addItem('[COLOR gold]---------------------------------------------------------[/COLOR]', '', 100, '',' ', '')
    for name, url, description in match:
        kodi.addDir(name, url, "lib_installer", artwork + 'icon.png')
    viewsetter.set_view("sets")


def toggle_notify():
    if kodi.get_setting('notifications-on-startup') == "false":
        option = 'OPT-out'
        sub = 'Un-'
        status = 'Disabled'
    else:
        option = 'OPT-in'
        sub = ''
        status = 'Enabled'
    confirm = xbmcgui.Dialog()
    if confirm.yesno('Community Notifications',
                     'Please confirm that you wish to %s of community notifications!' % option, " "):
        if status == 'Enabled':
            kodi.set_setting('notifications-on-startup', "false")
        else:
            kodi.set_setting('notifications-on-startup', "true")
        kodi.logInfo(status + "notifications")
        dialog = xbmcgui.Dialog()
        dialog.ok("Notifications " + status, "                     You have %ssubscribed to notifications!" % sub)
        xbmc.executebuiltin("Container.Refresh()")
    else:
        return


def system_info():
    systime = xbmc.getInfoLabel('System.Time ')
    dns1 = xbmc.getInfoLabel('Network.DNS1Address')
    gateway = xbmc.getInfoLabel('Network.GatewayAddress')
    ipaddy = xbmc.getInfoLabel('Network.IPAddress')
    linkstate = xbmc.getInfoLabel('Network.LinkState').replace("Link:", "")
    freespace, totalspace = maintool.get_free_space_mb(os.path.join(xbmc.translatePath('special://home')))
    freespace = maintool.convert_size(freespace) + ' Free'
    totalspace = maintool.convert_size(totalspace) + ' Total'
    screenres = xbmc.getInfoLabel('system.screenresolution')
    freemem = xbmc.getInfoLabel('System.FreeMemory')
    
    # FIND WHAT VERSION OF KODI IS RUNNING
    xbmc_version = xbmc.getInfoLabel("System.BuildVersion")
    versioni = xbmc_version[:4]
    VERSIONS = {10: 'Dharma', 11: 'Eden', 12: 'Frodo', 13: 'Gotham',
                14: 'Helix', 15: 'Isengard', 16: 'Jarvis', 17: 'Krypton'}
    codename = VERSIONS.get(int(xbmc_version[:2]))

    # Get External IP Address
    try:
        ext_ip = ("blue", requests.get('https://api.ipify.org').text)
    except Exception:
        ext_ip = ("red", "IP Check Not Available")

    # Get Python Version
    pv = sys.version_info
    
    # System Information Menu
    kodi.addItem('[COLOR ghostwhite]Version: [/COLOR][COLOR lime] %s %s[/COLOR]' % (codename, versioni),
                 '', 100, artwork + 'icon.png', "", description=" ")
    kodi.addItem('[COLOR ghostwhite]System Time: [/COLOR][COLOR lime] %s[/COLOR]' % systime,
                 '', 100, artwork + 'icon.png', "", description=" ")
    kodi.addItem('[COLOR ghostwhite]Gateway: [/COLOR][COLOR blue] %s[/COLOR]' % gateway,
                 '', 100, artwork + 'icon.png', "", description=" ")
    kodi.addItem('[COLOR ghostwhite]Local IP: [/COLOR][COLOR blue] %s[/COLOR]' % ipaddy,
                 '', 100, artwork+'icon.png', "", description=" ")
    kodi.addItem('[COLOR ghostwhite]External IP: [/COLOR][COLOR %s] %s[/COLOR]' % ext_ip,
                 '', 100, artwork + 'icon.png', "", description=" ")
    kodi.addItem('[COLOR ghostwhite]DNS 1: [/COLOR][COLOR blue] %s[/COLOR]' % dns1,
                 '', 100, artwork + 'icon.png', "", description=" ")
    kodi.addItem('[COLOR ghostwhite]Network: [/COLOR][COLOR gold] %s[/COLOR]' % linkstate,
                 '', 100, artwork + 'icon.png', "", description=" ")
    kodi.addItem('[COLOR ghostwhite]Disc Space: [/COLOR][COLOR gold] %s[/COLOR]' % totalspace,
                 '', 100, artwork + 'icon.png', "", description=" ")
    kodi.addItem('[COLOR ghostwhite]Disc Space: [/COLOR][COLOR gold] %s[/COLOR]' % freespace,
                 '', 100, artwork + 'icon.png', "", description=" ")
    kodi.addItem('[COLOR ghostwhite]Free Memory: [/COLOR][COLOR gold] %s[/COLOR]' % freemem,
                 '', 100, artwork + 'icon.png', "", description=" ")
    kodi.addItem('[COLOR ghostwhite]Resolution: [/COLOR][COLOR gold] %s[/COLOR]' % screenres,
                 '', 100, artwork + 'icon.png', "", description=" ")
    kodi.addItem('[COLOR ghostwhite]Python Version: [/COLOR][COLOR lime] %d.%d.%d[/COLOR]' % (pv[0], pv[1], pv[2]),
                 '', 100, artwork + 'icon.png', "", description=" ")
    viewsetter.set_view("files")


def fullspeedtest():
    # speed_test = base64.b64decode("aHR0cDovL2luZGlnby50dmFkZG9ucy5hZy9zcGVlZHRlc3Qvc3BlZWR0ZXN0ZmlsZS50eHQ=")
    speed_test = 'http://www.engineerhammad.com/2015/04/Download-Test-Files.html'
    try:
        link = OPEN_URL(speed_test)
        match = re.findall('href="([^"]*)".+src="([^"]*)".+\n.+?(\d+\s[^b]*b)', link)
        for url, iconimage, name in reversed(match):
            iconimage = artwork + str(name).replace(' ', '').lower() + '.png'
            if 'mb'in iconimage and not os.path.isfile(iconimage):
                iconimage = iconimage.replace('mb', '')
            kodi.addItem('[COLOR ghostwhite]' + name + '[/COLOR]', url, "runtest", iconimage,
                         description='Test with a ' + name + ' file')
    except:
        kodi.addItem('[COLOR ghostwhite]Speed Test is unavailable[/COLOR]', '', "", artwork + 'speed_test.png',
                     description='')
    viewsetter.set_view("sets")


def name_cleaner(c_name):
    c_name = c_name.replace('&#8211;', '')
    c_name = c_name.replace("&#8217;", "")
    c_name = c_name.replace("&#039;s", "'s")
    c_name = c_name.replace('&uacute;', 'u')
    c_name = c_name.replace('&eacute;', 'e')
    # c_name = c_name.replace('<', '&lt;'),
    # c_name = c_name.replace('&', '&amp;')
    # c_name = unicode(c_name, errors='ignore')
    return c_name


def cleanse_title(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass

        # replace nbsp with a space
        text = text.replace(u'\xa0', u' ')
        return text

    if isinstance(text, str):
        try:
            text = text.decode('utf-8')
        except:
            pass

    return re.sub("&#?\w+;", fixup, text.strip())


def OPEN_URL(url):
    headers = {'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTB Build/JDQ39) AppleWebKit/534.30'
                             '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == requests.codes.ok:
            return r.text
    except:
        return ''


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if params[len(params)-1] == '/':
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


params = get_params()
url = None
name = None
mode = None
thumb = None

try:
    iconimage = urllib.unquote_plus(params["iconimage"])
except:
    pass
try:
    thumb = urllib.unquote_plus(params["thumb"])
except:
    pass
try:
    fanart = urllib.unquote_plus(params["fanart"])
except:
    pass
try:
    description = urllib.unquote_plus(params["description"])
except:
    description = None
try:
    filetype = urllib.unquote_plus(params["filetype"])
except:
    filetype = None
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = urllib.unquote_plus(params["mode"])
except:
    pass
try:
    repourl = urllib.unquote_plus(params["repourl"])
except:
    repourl = None
try:
    xmlurl = urllib.unquote_plus(params["xmlurl"])
except:
    pass
try:
    dataurl = urllib.unquote_plus(params["dataurl"])
except:
    pass

# ext = addon.queries.get('ext', '')

if kodi.get_setting('debug') == "true":
    print "Mode: "+str(mode)
    print "URL: "+str(url)
    print "Name: "+str(name)
    print "Thumb: "+str(thumb)


if mode is None:
    main_menu()

elif mode == 'system_info':
    system_info()

elif mode == 'get_libs':
    rtmp_lib()

elif mode == 'call_sports':
    what_sports()

elif mode == 'log_upload':
    do_log_uploader()

elif mode == 'log_view':
    textviewer.window()
    # TextViewer.text_view('log')

elif mode == 'show_note':
    import notification
    # notification.note()

    # import common as Common
    TypeOfMessage = "t"
    notification.check_news2(TypeOfMessage, override_service=True)
    # (NewImage, NewMessage) = Common.FetchNews()

    # Common.CheckNews(TypeOfMessage, NewImage, NewMessage, False)

# #####MAIN TOOL
elif mode == 'call_maintool':
    maintool.tool_menu()
        
elif mode == 'wipe_addons':
        maintool.wipe_addons()
        
elif mode == 'clear_cache':
    maintool.delete_cache()
        
elif mode == 'clear_thumbs':
    maintool.delete_thumbnails()
        
elif mode == 'purge_packages':
    maintool.delete_packages()

elif mode == 'crashlogs':
    maintool.delete_crash_logs()

elif mode == 'deletetextures':
    maintool.delete_textures()

elif mode == 'autoclean':
    maintool.auto_clean()

elif mode == 'debug_onoff':
    maintool.debug_toggle()

elif mode == 'toggleblocker':
    maintool.toggle_setting('Script Blocker', 'scriptblock', restart=False)
    
elif mode == 'togglemain':
    maintool.toggle_setting('Automatic Maintenance ', 'automain', restart=True)
    
elif mode == 'autocleanstartup':
    maintool.toggle_setting('Auto maintenance at startup', 'acstartup')

elif mode == 'autocleanweekly':
    maintool.auto_weekly_clean_on_off()

elif mode == 'reloadskin':
    if xbmcgui.Dialog().yesno(AddonTitle, 'Please confirm that you wish to reload the skin cache immediately.'):
        xbmc.executebuiltin("ReloadSkin()")
    else:
        quit()
    
elif mode == 'updateaddons':
    choice = xbmcgui.Dialog().yesno(AddonTitle, 'Please confirm that you wish to force update all addons and '
                                                'repositories immediately.')
    if choice == 1:
        xbmc.executebuiltin("UpdateAddonRepos")
        xbmc.executebuiltin("UpdateLocalAddons")    
    else:
        quit()

elif mode == 'customkeys':
    installer.keymaps()

# ##############  SPEEDTEST  #################
elif mode == "runspeedtest":
    fullspeedtest()

elif mode == "runtest":
    speedtest.runfulltest(url)

elif mode == 'call_restore':
        freshstart.startup_freshstart()
        
# #########  NOTIFICATIONS  ##############
elif mode == 'toggle_notify':
    toggle_notify()

# ######   WIZARD   #########################
elif mode == 'call_wizard':
    configwizard.HELPCATEGORIES()

elif mode == 'helpwizard':
    configwizard.HELPWIZARD(name, url, description, filetype)

# elif mode == "wizardstatus":
#     print "" + url
#     items = configwizard.WIZARDSTATUS(url)

# ####  KEYMAPS  ###################################################################
elif mode == 'install_keymap':
    installer.install_keymap(name, url)

elif mode == 'uninstall_keymap':
    installer.uninstall_keymap()

# #############  Installer  ##########################################################
elif mode == 'call_installer':
    installer.MAININDEX()

elif mode == 'lib_installer':
    installer.libinstaller(name, url)

elif mode == 'addoninstall':
    # kodi.log("TRYING MODES")
    installer.ADDONINSTALL(name, url, description, filetype, repourl)

# elif mode == 'interrepolist':
#     items = installer.List_Inter_Addons(url)

elif mode == 'interrepos':
    items = installer.INTERNATIONAL_REPOS()

elif mode == 'interaddons':
    items = installer.INTERNATIONAL_ADDONS()

elif mode == 'interaddonslist':
    items = installer.INTERNATIONAL_ADDONS_LIST(url)

elif mode == 'interlist':
    items = installer.INTERNATIONAL_ADDONS()

elif mode == 'addonlist':
    items = installer.List_Addons(url)

elif mode == 'splitlist':
    installer.Split_List(name, url)

elif mode == 'addopensub':
    installer.OPENSUBINSTALL(url)

elif mode == 'searchaddon':
    installer.SEARCHADDON(url)

elif mode == 'github_main':
    installer.github_main(url)

# elif mode == 'github_history':
#     installer.github_history(url)
#
# elif mode == 'github_search':
#     installer.github_search(url)
#
# elif mode == 'github_results':
#     installer.github_results(url)
#
# elif mode == 'github_install':
#     installer.github_install(url)
#
# elif mode == 'github_instructions':
#     installer.github_instructions()
#
# elif mode == 'github_update':
#     installer.github_update()

elif mode == 'getaddoninfo':
    installer.getaddoninfo(url, description, filetype)

elif mode == 'urlzip':
    # kodi.log("TRYING MODES")
    installer.install_from_url()

elif mode == 'adultlist':
    items = installer.List_Adult(url)

# #######################################################################################
elif mode == 'EnableRTMP':
    installer.EnableRTMP()

# ######  REJUVINATE  ###########
elif mode == 'call_rejuv':
    import rejuv
    rejuv.startup_rejuv()

elif mode == 'juvwizard':
    import rejuv_run
    rejuv_run.JUVWIZARD()

elif mode == 'BrowseUrl':
    xbmc.executebuiltin("XBMC.System.Exec(%s)" % url)

elif mode == 'enableall':
    addon_able.setall_enable()

# elif mode == 'teststuff':
#     freshstart.remove_db()
#######################################

elif mode == 'backup_restore':
    backup.backup_menu()

elif mode == 'full_backup':
    backup.full_backup()

elif mode == 'small_backup':
    backup.no_data_backup()

elif mode == 'do_backup_restore':
    backup.restore()

elif mode == 'display_backup_settings':
    kodi.openSettings(addon_id, id1=0, id2=0)

elif mode == 'read_zip':
    backup.read_zip(url)

elif mode == 'del_backup':
    backup.ListBackDel()

elif mode == 'do_del_backup':
    backup.DeleteBackup(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
