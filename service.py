import os
import shutil
import re
# import urllib2
import datetime
import fileinput
import sys
import base64

import notification
import time

import xbmc
import xbmcaddon
# import common as Common

from libs import addon_able
from libs import kodi


# try:
#     from urllib.request import urlopen, Request  # python 3.x
# except ImportError:
#     from urllib2 import urlopen, Request  # python 2.x

addon_id = kodi.addon_id
AddonTitle = kodi.addon.getAddonInfo('name')
kodi.log('STARTING ' + AddonTitle + ' SERVICE')

# #############################
oldinstaller = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.program.addoninstaller'))
oldnotify = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.program.xbmchub.notifications'))
oldmain = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.xbmchubmaintool'))
oldwiz = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.hubwizard'))
oldfresh = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.freshstart'))
oldmain2 = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.hubmaintool'))
# #############################

# Check for old maintenance tools and remove them
old_maintenance = (oldinstaller, oldnotify, oldmain, oldwiz, oldfresh)
for old_file in old_maintenance:
    if os.path.exists(old_file):
        try:
            shutil.rmtree(old_file)
        except OSError:
            pass

# #############################
if xbmc.getCondVisibility('System.HasAddon(script.service.twitter)'):
    search_string = xbmcaddon.Addon('script.service.twitter').getSetting('search_string')
    search_string = search_string.replace('from:@', 'from:')
    xbmcaddon.Addon('script.service.twitter').setSetting('search_string', search_string)
    xbmcaddon.Addon('script.service.twitter').setSetting('enable_service', 'false')

# ################################################## ##
date = datetime.datetime.today().weekday()
if  (kodi.get_setting("clearday") == date) or kodi.get_setting("acstartup") == "true":
    import maintool
    maintool.auto_clean(True)

# ################################################## ##
if kodi.get_setting('set_rtmp') == 'false':
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
    kodi.set_setting('set_rtmp', 'true')
    time.sleep(0.5)

# ################################################## ##
run_once_path = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'resources', 'run_once.py'))
if kodi.get_var(run_once_path, 'hasran') == 'false':
    kodi.set_setting('sevicehasran', 'false')

# Start of notifications
if kodi.get_setting('sevicehasran') == 'true':
    TypeOfMessage = "t"
    notification.check_news2(TypeOfMessage, override_service=False)
# ################################################## ##


if __name__ == '__main__':
    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds 12 hours is 43200   1 hours is 3600
        if monitor.waitForAbort(1800):
            # Abort was requested while waiting. We should exit
            kodi.log('CLOSING ' + AddonTitle.upper() + ' SERVICES')
            break
        if kodi.get_setting('scriptblock') == 'true':
            kodi.log('Checking for Malicious scripts')
            BlocksUrl = base64.b64decode('aHR0cDovL2luZGlnby50dmFkZG9ucy5jby9ibG9ja2VyL2Jsb2NrZXIudHh0')
            BlocksUrl = 'http://indigo.tvaddons.co/blocker/blocker.txt'
            try:
                link = kodi.read_file(BlocksUrl)
                # req = Request(BlocksUrl)
                # req.add_header('User-Agent', 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTB Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
                # response = = urlopen(req)
                # link = response.read()
                # response.close()
            except:
                kodi.log('Could not perform blocked script. invalid URL')
                break
            #     continue
            link = link.replace('\n', '').replace('\r', '').replace('\a', '')

            match = re.compile('block="(.+?)"').findall(link)
            for blocked in match:
                    addonPath = xbmcaddon.Addon(id=addon_id).getAddonInfo('path')
                    addonPath = xbmc.translatePath(addonPath)
                    xbmcPath = os.path.join(addonPath, "..", "..")
                    xbmcPath = os.path.abspath(xbmcPath)

                    addonpath = xbmcPath + '/addons/'
                    try:
                        for root, dirs, files in os.walk(addonpath, topdown=False):
                            if root != addonpath:
                                if blocked in root:
                                    shutil.rmtree(root)
                    except:
                        kodi.log('Could not find blocked script')

for line in fileinput.input(run_once_path, inplace=1):
    if "hasran" in line:
        line = line.replace('false', 'true')
    sys.stdout.write(line)
kodi.set_setting('sevicehasran', 'true')
