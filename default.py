# -*- coding: utf-8 -*-
# import base64
import os
import re
import shutil
import sys
import urllib

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
# from libs import requests
from libs import addon_able
from libs import kodi
from libs import speedtest
from libs import viewsetter

try:
    import htmlentitydefs  # python 2.x
except ImportError:
    import html.entities as htmlentitydefs  # python 3.x

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
            downloader.download(kodi.read_file('http://indigo.tvaddons.co/graphics/arts.txt'), icons_zip, dp)
            # downloader.download(OPEN_URL('http://indigo.tvaddons.co/graphics/arts.txt'), icons_zip, dp)
            dp.update(0, 'Getting %s Ready........' % AddonTitle, 'Extracting %s Icons......' % AddonTitle)
            extract.all(icons_zip, addon_path, dp)
            dp.close()
    except Exception as e:
        kodi.log(str(e))
    # Check for old version of hubrepo and remove it
    try:
        if os.path.exists(hubpath):
            with open(hubpath, 'r') as content:
                if 'AG' in content:
                    shutil.rmtree(hubpath)
    except Exception as e:
        kodi.log(str(e))
    # # Check for HUBRepo and install it
    try:
        if not os.path.exists(hubpath):
            installer.HUBINSTALL('repository.xbmchub', 'http://github.com/tvaddonsco/tva-release-repo/raw/master/'
                                                       'repository.xbmchub/', 'repository.xbmchub')
            # xbmc.executebuiltin("XBMC.InstallAddon(%s)" % 'repository.xbmchub')
            addon_able.set_enabled("repository.xbmchub")
            xbmc.executebuiltin("XBMC.UpdateAddonRepos()")
    except Exception as e:
        kodi.log(str(e))
        import traceback
        traceback.print_exc(file=sys.stdout)
        raise
    # Check for Log Uploader and install it
    try:
        if not os.path.exists(uploaderpath):
            installer.HUBINSTALL('script.tvaddons.debug.log',
                                 'http://github.com/tvaddonsco/tva-release-repo/raw/master'
                                 '/script.tvaddons.debug.log/', 'script.tvaddons.debug.log')
            addon_able.set_enabled('script.tvaddons.debug.log')
            # xbmc.executebuiltin("InstallAddon(%s)" % 'script.tvaddons.debug.log')
            xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
    except Exception as e:
        kodi.log(str(e))
        raise
   
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
    kodi.addItem("No-Coin Scan", '', 'nocoin', artwork + 'no_coin.png',
                 description="Scan your Kodi directory for coin mining.")
    kodi.addItem("Notifications " + note_status, '', 'toggle_notify', artwork + note_art,
                 description="%s to important TV ADDONS notifications on startup!" % note_description)
    kodi.addItem("Show Notification", '', 'show_note', artwork + 'notification.png',
                 description="Show TVA Notification. To get Important News, Tips, and Giveaways from TV ADDONS")
    viewsetter.set_view("sets")


def do_log_uploader():
    xbmc.executebuiltin("RunAddon(script.tvaddons.debug.log)")


def what_sports():
    # #######  AMERICAN  ###############
    kodi.addItem('[COLOR blue][B]US Sports[/COLOR][/B]', '', '', artwork + 'icon.png',
                 description='[COLOR gold]Sports from around the US[/COLOR]')
    link = kodi.read_file('https://www.tvguide.com/sports/live-today/')
    pattern = '(?s)program-link">([^<]*)<.+?info">([^\|]*)\| ([^<]*)<.+?description">([^<]*)'
    for m_name, m_time, m_channel, m_description in re.findall(pattern, link):
        kodi.addItem('[COLOR white][B]%s[/COLOR][/B] - [COLOR gold]%s[/COLOR][COLOR white][B] | %s[/COLOR][/B]'
                     % (m_time.lower(), name_cleaner(m_name), m_channel), '', '', artwork + 'icon.png',
                     description='[COLOR gold][B]%s - %s[/COLOR][/B][COLOR white] - %s | %s[/COLOR]'
                                 % (m_description, name_cleaner(m_name), m_time.lower(), m_channel))

    # #######  UK  ###############
    kodi.addItem('[COLOR blue][B]UK Sports[/COLOR][/B]', '', '', artwork + 'icon.png',
                 description='[COLOR gold]Sports from around the UK[/COLOR]')
    link = kodi.read_file('http://www.wheresthematch.com/').replace('\r', '').replace('\n', '').replace('\t', '')
    pattern = '(?s)fixture-details">(.+?)t-details">(.+?)-name">(.+?)l-details">(.+?).png'
    for m_game, m_time, m_league, m_channels in re.findall(pattern, link):
        g_time = re.search('<strong>([^<]*)', m_time)
        g_time = g_time.group(1).strip('0').replace(' ', '') if g_time else ''
        league = re.search('<span>([^<]*)', m_league)
        g_league = ' - ' + league.group(1) if league else ''
        g_name = ''
        for team1, team2 in re.findall('(?s).asp">[^>]*>([^<]+)<.+?asp.+?">([^<]*)', m_game):
            g_name = '- %s vs %s' % (team1, team2) if m_game else ''
        if '<strong class=' in m_game:
            game = re.search('<strong class="">([^<]*)', m_game)
            g_name = ' - ' + game.group(1) if game and league != game.group(1) else ''
        channels = ''
        for channel in re.findall('-name">([^<]*)', m_channels):
            channels += ' ' + channel if not channels else ', ' + channel
        kodi.addItem('[COLOR white][B]%s[/COLOR][/B][COLOR gold]%s %s[/COLOR][COLOR white][B] | %s[/COLOR][/B]'
                     % (g_time, g_league, g_name, channels), '', '', artwork + 'icon.png',
                     description='[COLOR gold][B]%s - %s[/COLOR][/B][COLOR white] - %s | %s[/COLOR]'
                                 % (g_time, g_name, g_league, channels))
    viewsetter.set_view("tvshows")


def rtmp_lib():
    liblist = "http://indigo.tvaddons.co/librtmp/rtmplist.txt"
    try:
        # link = OPEN_URL(liblist).replace('\n', '').replace('\r', '')
        link = kodi.read_file(liblist).replace('\n', '').replace('\r', '')
    except Exception as e:
        kodi.log(str(e))
        kodi.addItem('[COLOR gold][B]This service is currently unavailable.[/COLOR][/B]', '', 100, '', '', '')
        return
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?ersion="(.+?)"').findall(link)
    kodi.addItem('[COLOR gold][B]Files Will Be Donwloaded to the Kodi Home directory,'
                 'You Will Need To Manually Install From There.[/COLOR][/B]', '', 100, '', '', '')
    # kodi.addItem('[COLOR gold]---------------------------------------------------------[/COLOR]', '', 100, '',' ', '')
    for m_name, m_url, m_description in match:
        kodi.addDir(m_name, m_url, "lib_installer", artwork + 'icon.png')
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
    freespace = maintool.convert_size(freespace)
    totalspace = maintool.convert_size(totalspace)
    screenres = xbmc.getInfoLabel('system.screenresolution')
    freemem = maintool.convert_size(maintool.revert_size(xbmc.getInfoLabel('System.FreeMemory')))
    
    # FIND WHAT VERSION OF KODI IS RUNNING
    # xbmc_version = xbmc.getInfoLabel("System.BuildVersion")
    # versioni = xbmc_version[:4]
    # codename = kodi.get_codename()

    # Get External IP Address
    try:
        # ext_ip = ("blue", OPEN_URL('https://api.ipify.org'))
        ext_ip = ("blue", kodi.read_file('https://api.ipify.org'))
    except Exception as e:
        kodi.log(str(e))
        try:
            # link = OPEN_URL('http://whatismyip.network/')
            link = kodi.read_file('http://whatismyip.network/')
            ext_ip = ("blue", re.search('>My IP Address[^=]*[^>]*>([^<]*)', link).group(1))
        except:
            ext_ip = ("red", "IP Check Not Available")

    # Get Python Version
    pv = sys.version_info
    
    # System Information Menu
    # kodi.addItem('[COLOR ghostwhite]Version: [/COLOR][COLOR lime] %s %s[/COLOR]' % (codename, versioni),
    #              '', 100, artwork + 'icon.png', "", description=" ")
    kodi.addItem('[COLOR ghostwhite]Version: [/COLOR][COLOR lime] %s %s[/COLOR]' %
                 (kodi.get_codename(), xbmc.getInfoLabel("System.BuildVersion").split('Git')[0]),'',
                 100, artwork + 'icon.png', "", description=" ")
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
    if str(totalspace) != '0 B':
        kodi.addItem('[COLOR ghostwhite]Total Disc Space: [/COLOR][COLOR gold] %s[/COLOR]' % totalspace,
                     '', 100, artwork + 'icon.png', "", description=" ")
    if str(freespace) != '0 B':
        kodi.addItem('[COLOR ghostwhite]Free Disc Space: [/COLOR][COLOR gold] %s[/COLOR]' % freespace,
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
        # link = OPEN_URL(speed_test)
        link = kodi.read_file(speed_test)
        match = re.findall('href="([^"]*)".+src="([^"]*)".+\n.+?(\d+\s[^b]*b)', link)
        for m_url, m_iconimage, m_name in reversed(match):
            m_iconimage = artwork + str(m_name).replace(' ', '').lower() + '.png'
            if 'mb'in m_iconimage and not os.path.isfile(m_iconimage):
                m_iconimage = m_iconimage.replace('mb', '')

            kodi.addItem('[COLOR ghostwhite]' + m_name + '[/COLOR]', m_url, "runtest", m_iconimage,
                         description='Test with a ' + m_name + ' file')
    except Exception as e:
        kodi.log(str(e))
        import traceback
        traceback.print_exc(file=sys.stdout)
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
                    return chr(int(text[3:-1], 16))  # unichr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))  # unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                # text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                text = chr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        # replace nbsp with a space
        text = text.replace(u'\xa0', u' ')
        return text

    if isinstance(text, str):
        try:
            text = text.decode('utf-8')
        except Exception as e:
            kodi.log(str(e))
    return re.sub("&#?\w+;", fixup, text.strip())


# def OPEN_URL(url):
#     headers = {'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTB Build/JDQ39) AppleWebKit/534.30'
#                              '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}
#     try:
#         # r = requests.get(url, headers=headers)
#         # if r.status_code == requests.codes.ok:
#         #     return r.text
#         response = urlopen(Request(url, headers=headers))
#         link = response.read()
#         response.close()
#         return link
#     except Exception as e:
#         kodi.log(str(e))
#         import traceback
#         traceback.print_exc(file=sys.stdout)
#         return ''


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params_l = sys.argv[2]
        cleanedparams = params_l.replace('?', '')
        # if params_l[len(params_l)-1] == '/':
        #     params_l = params_l[0:len(params_l)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            # splitparams = {}
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
    # TypeError and KeyError
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
    print("Mode: "+str(mode))
    print("URL: "+str(url))
    print("Name: "+str(name))
    print("Thumb: "+str(thumb))


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
    TypeOfMessage = "t"
    notification.check_news2(TypeOfMessage, override_service=True)

elif mode == 'nocoin':
    import nocoin
    nocoin.nocoin()

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
#Update(plugin://plugin.git.browser)
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
