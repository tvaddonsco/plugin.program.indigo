import os
import shutil
import re
import datetime
from sqlite3 import dbapi2 as db_lib
import fileinput
import sys

import notification
import downloader
import extract
import time

import xbmc
import xbmcaddon
import maintool

from libs import addon_able
from libs import kodi

addon_id = kodi.addon_id
AddonTitle = kodi.addon.getAddonInfo('name')
addonspath = os.path.abspath(xbmc.translatePath('special://home')) + '/addons/'
packages_path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
datapath = os.path.abspath(xbmc.translatePath('special://home')) + '/userdata/addon_data/'
artwork = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'art/'))
BlocksUrl = 'https://indigo.tvaddons.co/blocker/blocker.txt'
script_url = 'https://github.com/tvaddonsco/tva-release-repo/raw/master/plugin.program.indigo/'
db_dir = xbmc.translatePath("special://profile/Database")
db_path = os.path.join(db_dir, 'Addons27.db')
run_once_path = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'resources', 'run_once.py'))
settings = xbmcaddon.Addon(id=addon_id)
kodi.log('STARTING ' + AddonTitle + ' SERVICE')

oldinstaller = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.program.addoninstaller'))
oldnotify = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.program.xbmchub.notifications'))
oldmain = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.xbmchubmaintool'))
oldwiz = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.hubwizard'))
oldfresh = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.freshstart'))
oldmain2 = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.hubmaintool'))


def blocker(binit_time):
    blink = settings.getSetting("blockLink")
    time_match = re.findall('exp="([^"]*)"', blink) if blink else ''
    time_match = time_match if time_match else [48]
    if not blink or datetime.datetime.now() >= binit_time + datetime.timedelta(hours=int(time_match[0])):
        xbmc.log('Checking for Malicious scripts')
        blink = kodi.read_file(BlocksUrl).replace(' ', '').replace('\r', '').replace('\n', '')
        settings.setSetting("blockLink", blink) if blink else ''
        binit_time = datetime.datetime.now() if blink else binit_time
    xbmc.log('Could not find blocked script list') if not blink else ''
    for blocked in re.findall('block="(.+?)"', blink):
        if blocked and (os.path.isdir(addonspath + blocked) or xbmc.getCondVisibility("System.HasAddon(%s)" % blocked)):
            set_disabled(blocked)
            shutil.rmtree(addonspath + blocked) if os.path.isdir(addonspath + blocked) else ''
            shutil.rmtree(datapath + blocked) if os.path.isdir(datapath + blocked) else ''
    return binit_time


def get_dir(script, source_url):
    match = re.findall(script + '(-.+?)?.zip', kodi.open_url(source_url))
    match.sort(reverse=True)
    version = match[0] if match else ''
    newest_v_url = source_url + script + version + '.zip'
    lib = os.path.join(packages_path, script + version + '.zip')
    os.remove(lib) if os.path.exists(lib) else ''
    downloader.download(newest_v_url, lib, None, timeout=120, silent=True)
    extract.extract_all(os.path.join(packages_path, lib), addonspath, None)
    addon_able.set_enabled(script)
    xbmc.executebuiltin("UpdateLocalAddons()")


def set_disabled(addon):
    conn = db_lib.connect(db_path)
    conn.text_factory = str
    if int(xbmc.getInfoLabel('System.BuildVersion').split(".")[0]) > 16.5:
        xbmc.executebuiltin("StopScript(%s)" % addon)
        conn.execute('DELETE FROM installed WHERE addonID=?', (addon,))
        conn.commit()
        conn.close()
        xbmc.executebuiltin("Container.Update", True)
        xbmc.executebuiltin("Container.Refresh")
        xbmc.executebuiltin("UpdateAddonRepos") if addon.startswith('repo') else ''
        xbmc.executebuiltin("UpdateLocalAddons")


def note(n_time, status=False):
    if not xbmc.Player().isPlaying():
        n_time = datetime.datetime.now()
        notification.check_news2("t", override_service=status)
    return n_time


block_time = datetime.datetime.now()
link = kodi.read_file(BlocksUrl).replace(' ', '').replace('\r', '').replace('\n', '')
settings.setSetting("blockLink", link) if link else ''
block_time = blocker(block_time) if kodi.get_setting('scriptblock') == 'true' else block_time
get_dir(addon_id, script_url) if not os.path.exists(addonspath + addon_id)else ''

old_maintenance = (oldinstaller, oldnotify, oldmain, oldwiz, oldfresh)
for old_file in old_maintenance:
    shutil.rmtree(old_file) if os.path.exists(old_file) else ''

if xbmc.getCondVisibility('System.HasAddon(script.service.twitter)'):
    search_string = xbmcaddon.Addon('script.service.twitter').getSetting('search_string')
    search_string = search_string.replace('from:@', 'from:')
    xbmcaddon.Addon('script.service.twitter').setSetting('search_string', search_string)
    xbmcaddon.Addon('script.service.twitter').setSetting('enable_service', 'false')

date = datetime.datetime.today().weekday()
maintool.auto_clean(True) if kodi.get_setting("acstartup") == "true" or (kodi.get_setting("clearday") == date) else ''

if kodi.get_setting('set_rtmp') == 'false':
    addon_able.set_enabled("inputstream.adaptive")
    time.sleep(0.5)
    addon_able.set_enabled("inputstream.rtmp")
    time.sleep(0.5)
    kodi.set_setting('set_rtmp', 'true')
    xbmc.executebuiltin("UpdateLocalAddons()")
    time.sleep(0.5)

note_time = datetime.datetime.now()
kodi.set_setting('sevicehasran', 'false') if kodi.get_var(run_once_path, 'hasran') == 'false' else ''
if kodi.get_setting('sevicehasran') == 'true':
    note_time = note(note_time, False)

if __name__ == '__main__':
    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        if kodi.get_setting('scriptblock') == 'true':
            block_time = blocker(block_time)
        if not os.path.exists(addonspath + addon_id):
            get_dir(addon_id, script_url)
        if datetime.datetime.now() >= note_time + datetime.timedelta(hours=6) \
                and kodi.get_setting('sevicehasran') == 'true':
            note_time = note(note_time, True)
        if kodi.get_setting('sevicehasran') == 'false':
            for line in fileinput.input(run_once_path, inplace=1):
                if 'hasran' in line and 'false' in line:
                    line = line.replace('false', 'true')
                sys.stdout.write(line)
            kodi.set_setting('sevicehasran', 'true')
        # Sleep/wait for abort for 5 seconds
        if monitor.waitForAbort(5):
            # Abort was requested while waiting. We should exit
            kodi.log('CLOSING ' + AddonTitle.upper() + ' SERVICES')
            break
