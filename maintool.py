import datetime
import os
import shutil
import sys
import re
import traceback
import xbmc
import xbmcgui
from libs import kodi
from libs import viewsetter

addon_id = kodi.addon_id
addon = (addon_id, sys.argv)
AddonName = kodi.addon.getAddonInfo('name') + " for Kodi"
artwork = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'art/'))
fanart = artwork + 'fanart.jpg'
messages = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'resources', 'messages/'))
execute = xbmc.executebuiltin
dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()

userdata_path = xbmc.translatePath('special://userdata/')
database_path = xbmc.translatePath('special://userdata/Database')
addon_data = xbmc.translatePath('special://userdata/addon_data')
thumbnail_path = xbmc.translatePath('special://userdata/Thumbnails')
cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
temp_path = os.path.join(xbmc.translatePath('special://home'), 'temp')
addons_path = os.path.join(xbmc.translatePath('special://home'), 'addons')
packages_path = os.path.join(xbmc.translatePath('special://home/addons'), 'packages')


def tool_menu():
    menu_cache_path = cache_path
    if not os.path.exists(temp_path) and not os.path.exists(cache_path):
        os.makedirs(temp_path)
    if os.path.exists(temp_path):
        menu_cache_path = temp_path
    if not os.path.exists(packages_path):
        os.makedirs(packages_path)
    cache_size = ''
    thumb_size = ''
    packages_size = ''
    paths = {menu_cache_path: cache_size, thumbnail_path: thumb_size, packages_path: packages_size}
    if kodi.get_setting("maint_check_folders") == "true":
        for path in paths:
            try:
                paths[path] = ' - [COLOR blue]' + convert_size(get_size(path)) + '[/COLOR]'
            except Exception as e:
                kodi.log(str(e))
                paths[path] = ' - [COLOR red]Error reading thumbnails[/COLOR]'
    startup_clean = kodi.get_setting("acstartup")
    if startup_clean == "false":
        startup_onoff = "Enable"
        su_art = 'enable_am_startup.png'
    else:
        startup_onoff = "Disable"
        su_art = 'disable_am_startup.png'
    su_desc = startup_onoff + " maintenance on Kodi launch!"
    weekly_clean = kodi.get_setting("clearday")
    if weekly_clean == "7":
        weekly_onoff = "Enable"
        acw_art = 'enable_am_week.png'
        acw_desc = "Set your device to perform maintenance on a given day each week!"
    else:
        weekly_onoff = "Disable"
        acw_art = 'disable_am_week.png'
        acw_desc = weekly_onoff + " weekly maintenance on Kodi launch!"
    if kodi.get_setting('scriptblock') == 'false':
        scb_onoff = 'Enable'
        # scb_mode = 'toggleblocker'
        scb_art = 'enable_MSB.png'
    else:
        scb_onoff = 'Disable'
        # scb_mode = 'toggleblocker'
        scb_art = 'enable_MSB.png'
    scb_desc = scb_onoff + " protection against malicious scripts!"

    if not _is_debugging():
        debug_onoff = 'Enable'
        debug_art = 'enabledebug.png'
    else:
        debug_onoff = 'Disable'
        debug_art = 'disabledebug.png'
    debug_desc = debug_onoff + " Debugging!"
    
    # Maintenance Tool Menu
    kodi.addItem("Clear Cache " + str(paths[menu_cache_path]), '', 'clear_cache', artwork + 'currentcache.png',
                 description="Clear your device cache!")
    kodi.addItem("Delete Thumbnails " + str(paths[thumbnail_path]), '', 'clear_thumbs', artwork + 'currentthumbs.png',
                 description="Delete your Thumbnail cache!")
    kodi.addItem("Delete Packages " + str(paths[packages_path]), '', 'purge_packages', artwork + 'currentpackages.png',
                 description="Delete your addon installation files!")
    kodi.addItem("Delete Crash Logs", '', 'crashlogs', artwork + 'clearcrash.png',
                 description="Clear all crash logs from your device!")
    kodi.addItem("Delete Textures13.db", '', 'deletetextures', artwork + 'currentthumbs.png',
                 description="This will delete the Textures13 database")
    kodi.addDir("Wipe Addons", '', 'wipe_addons', artwork + 'wipe_addons.png',
                description="Erase all your Kodi addons in one shot!")
    kodi.addItem("Run Auto Maintenance", '', 'autoclean', artwork + 'run_am.png',
                 description="Clear your cache, thumbnails and delete addon packages in one click!")
    kodi.addItem(startup_onoff + ' Auto Maintenance on Startup', '', 'autocleanstartup', artwork + su_art,
                 description=su_desc)
    kodi.addItem(weekly_onoff + ' Weekly Auto Maintenance', '', 'autocleanweekly', artwork + acw_art,
                 description=acw_desc)
    kodi.addItem(debug_onoff + " Debugging Mode", '', 'debug_onoff', artwork + debug_art,
                 description=debug_desc)
    kodi.addItem(scb_onoff + " Malicious Scripts Blocker", '', 'toggleblocker', artwork + scb_art,
                 description=scb_desc)
    kodi.addItem("Force Update Addons", '', 'updateaddons', artwork + 'forceupdateaddons.png',
                 description="Force a reload of all Kodi addons and repositories!")
    kodi.addDir("Install Custom Keymaps", '', 'customkeys', artwork + 'custom_keymaps.png',
                description="Get the best experience out of your device-specific remote control!")
    kodi.addItem("Reload Current Skin", '', 'reloadskin', artwork + 'reloadskin.png',
                 description="Reload the skin!")
    viewsetter.set_view("sets")


def delete_cache(auto_clear=False):
    if not auto_clear:
        if not xbmcgui.Dialog().yesno("Please Confirm",
                                      "                        Please confirm that you wish to clear",
                                      "                              your Kodi application cache!",
                                      "                             ", "Cancel", "Clear"):
            return
    cache_paths = [cache_path, temp_path]
    if xbmc.getCondVisibility('system.platform.ATV2'):
        cache_paths.extend([os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other'),
                            os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')])
    file_types = ['log', 'db', 'dat', 'socket']
    # if kodi.get_setting('acdb') == 'true':
    #     file_types.remove('db')
    directories = ('temp', 'archive_cache')
    for directory in cache_paths:
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for f in files:
                    try:
                        if f.split('.')[1] not in file_types:
                            os.unlink(os.path.join(root, f))
                    except OSError:
                        pass
                for d in dirs:
                    try:
                        if d not in directories:
                            shutil.rmtree(os.path.join(root, d))
                    except OSError:
                        pass
    if not auto_clear:
        xbmcgui.Dialog().ok(AddonName, "Done Clearing Cache files")
        xbmc.executebuiltin("Container.Refresh")


def delete_thumbnails(auto_clear=False):
    if not auto_clear:
        if not xbmcgui.Dialog().yesno("Delete Thumbnails", "This option deletes all thumbnails",
                                      "Are you sure you want to do this?"):
            return
    status = 'have been'
    if os.path.exists(thumbnail_path):
        file_types = ('db', 'dat', 'socket')
        for root, dirs, files in os.walk(thumbnail_path):
            for f in files:
                if f.split('.')[1] not in file_types:
                    try:
                        os.unlink(os.path.join(root, f))
                    except OSError:
                        status = 'could not all be'
    if not auto_clear:
        xbmcgui.Dialog().ok(AddonName, 'Thumbnails %s deleted.' % status)
        xbmc.executebuiltin("Container.Refresh")


def delete_packages(auto_clear=False):
    if not auto_clear:
        if not xbmcgui.Dialog().yesno('Delete Packages', "Delete Package Cache Files?"):
            return
    for root, dirs, files in os.walk(xbmc.translatePath('special://home/addons/packages')):
        try:
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        except OSError:
            pass
    if not auto_clear:
        xbmcgui.Dialog().ok(AddonName, "Deleting Packages all done")
        xbmc.executebuiltin("Container.Refresh")


def delete_crash_logs(auto_clear=False):
    if not auto_clear:
        if not xbmcgui.Dialog().yesno(AddonName, 'Delete Crash Logs', "Do you want to delete old crash logs?"):
            return
    cache_directories = (xbmc.translatePath('special://home'),
                         os.path.join(xbmc.translatePath('special://home'), 'cache'),
                         xbmc.translatePath('special://temp'))
    for cache_directory in cache_directories:
        if os.path.exists(cache_directory):
            file_types = ('*.dmp', '*.txt')
            import glob
            for file_type in file_types:
                for infile in glob.glob(cache_directory + file_type):
                    os.remove(infile)
    if not auto_clear:
        xbmcgui.Dialog().ok(AddonName, "Crash logs deleted")


def delete_textures():
    if not xbmcgui.Dialog().yesno(AddonName, 'Delete Textures13 Database', "Do you want to delete the Database?"):
        return
    status = "has been"
    try:
        os.unlink(os.path.join(database_path, "Textures13.db"))
    except OSError:
        status = 'could not be'
    xbmcgui.Dialog().ok(AddonName, 'Textures13.db %s deleted.' % status,
                        'Kodi will now shut down for database to rebuild')
    xbmc.executebuiltin('ShutDown')


def wipe_addons():
    # kodi.logInfo('WIPE ADDONS ACTIVATED')
    if xbmcgui.Dialog().yesno("Please Confirm",
                              "                     Please confirm that you wish to uninstall",
                              "                              all addons from your device!",
                              "              ", nolabel='Cancel', yeslabel='Uninstall'):
        try:
            for root, dirs, files in os.walk(addons_path, topdown=False):
                if root != addons_path:
                    if addon_id not in root:
                        if 'metadata.album.universal' not in root:
                            if 'metadata.artists.universal' not in root:
                                if 'service.xbmc.versioncheck' not in root:
                                    if 'metadata.common.musicbrainz.org' not in root:
                                        shutil.rmtree(root)
            xbmcgui.Dialog().ok(AddonName, "Addons Wiped Successfully!",
                                "Click OK to exit Kodi and then restart to complete.")
            xbmc.executebuiltin('ShutDown')
        except Exception as e:
            kodi.log(str(e))
            xbmcgui.Dialog().ok(AddonName, "Error Wiping Addons please visit TVADDONS.CO forums")


def debug_toggle():
    xbmc.executebuiltin("ToggleDebug")
    xbmc.executebuiltin("Container.Refresh")
    xbmcgui.Dialog().notification('Debugging', 'Setting Changed!', sound=False)


def toggle_setting(setting_title, setting, restart=False, silent=False):
    # kodi.log('TOGGLE SETTING')
    if not silent:
        if kodi.get_setting(setting) == "true":
            status_on_off = 'OFF'
        else:
            status_on_off = 'ON'
        if not xbmcgui.Dialog().yesno(setting_title,
                                      'Please confirm that you wish to TURN %s %s' % (status_on_off, setting_title),
                                      '', '', 'Cancel', 'Confirm'):
                return
    if kodi.get_setting(setting) == 'true':
        kodi.set_setting(setting, 'false')
    else:
        kodi.set_setting(setting, 'true')
    kodi.log('Toggled setting for ' + setting_title)
    if not silent and not restart:
        xbmcgui.Dialog().notification('', 'Setting Changed!', sound=False)
        xbmc.executebuiltin("Container.Refresh")
    if restart:
        xbmcgui.Dialog().notification('', 'Kodi is shutting down for changes to take effect', sound=False)
        xbmc.executebuiltin('ShutDown')
    

def auto_weekly_clean_on_off():
    if kodi.get_setting("clearday") == '7':
        if xbmcgui.Dialog().yesno(AddonName, 'Please confirm that you wish to enable weekly automated maintenance.'):
            kodi.set_setting("clearday", datetime.datetime.today().weekday())
            kodi.openSettings(addon_id, id1=5, id2=3)
            available_space, total_space = get_free_space_mb(xbmc.translatePath('special://home'))
            if str(available_space) == '0 B Free' and str(total_space) == '0 B Total':
                xbmcgui.Dialog().ok('Auto Maintenance Error',
                                    'Auto Maintenance encountered a problem and can not be run',
                                    'Maintenace can still be done individually')
                return
            mb_settings = (0, 25, 50, 75, 100)
            while True:
                allotted_space = 0
                for value in ('cachemb', 'thumbsmb', 'packagesmb'):
                    allotted_space += mb_settings[int(kodi.get_setting(value))] * 10**6
                if (allotted_space >= available_space) and not kodi.get_setting("automb"):
                    xbmcgui.Dialog().ok("Your settings sizes for Kodi to use are larger than the available drive space",
                                        'Please try lower settings, uninstall uneeded apps and addons,',
                                        'or set kodi size to "Auto" to use the automated settings based on free space')
                    kodi.openSettings(addon_id, id1=5, id2=3)
                else:
                    break
    else:
        if xbmcgui.Dialog().yesno(AddonName, 'Please confirm that you wish to disable weekly automated maintenance.'):
            kodi.set_setting("clearday", '7')
    xbmc.executebuiltin("Container.Refresh")


def auto_clean(auto_clear=False):
    if not auto_clear:
        if not xbmcgui.Dialog().yesno(AddonName, 'Selecting Yes runs maintenance based on your settings.',
                                      'Do you wish to continue?', yeslabel='Yes', nolabel='No'):
            return
    available_space, total_space = get_free_space_mb(xbmc.translatePath('special://home'))
    err_default = (0, '0 B', '0M', '0 MB', '0 MB Free', '0 MB Total', '0M Free', '0M Total')
    if str(available_space) in err_default or str(total_space) in err_default:
        if not auto_clear:
            if xbmcgui.Dialog().yesno('Auto Maintenance Error',
                                      'Auto Maintenance encountered a problem and was not ran',
                                      'Maintenace can still be done now or individually',
                                      'Would you like to just clear the cache, packages, and thumbnails',
                                      yeslabel='Yes', nolabel='No'):
                delete_cache(auto_clear=True)
                delete_packages(auto_clear=True)
                delete_thumbnails(auto_clear=True)
                delete_crash_logs(auto_clear=True)
                xbmc.executebuiltin("Container.Refresh")
                xbmcgui.Dialog().ok(AddonName, 'Auto Maintenance has been run successfully')
        return
    mb_settings = (0, 25, 50, 75, 100)
    for value in ('cachemb', 'thumbsmb', 'packagesmb'):
        available_space += mb_settings[int(kodi.get_setting(value))] * 10**6
    automb = kodi.get_setting("automb")
    cachemb = float((mb_settings[int(kodi.get_setting("cachemb"))]) * 10**6)  # 35%
    for path in (cache_path, temp_path):
        if os.path.exists(path):
            try:
                if (automb and (cachemb >= float(available_space) * .35)) or \
                        ((cachemb == 0 and kodi.get_setting("accache") == 'true')
                         or (cachemb != 0 and (get_size(cache_path) >= int(cachemb)))):
                    delete_cache(auto_clear=True)
            except Exception as e:
                kodi.log(str(e))
    thumbsmb = float((mb_settings[int(kodi.get_setting("thumbsmb"))]) * 10**6)  # 35%
    try:
        if (automb and (thumbsmb >= int(available_space) * .35)) or \
                ((thumbsmb == 0 and kodi.get_setting("acthumbs") == 'true')
                 or (thumbsmb != 0 and (get_size(thumbnail_path) >= int(thumbsmb)))):
            delete_thumbnails(auto_clear=True)
    except Exception as e:
        kodi.log(str(e))
    packagesmb = float((mb_settings[int(kodi.get_setting("packagesmb"))]) * 10**6)  # 10%
    try:
        if (automb and (packagesmb >= int(available_space) * .10)) or \
                ((packagesmb == 0 and kodi.get_setting("acpackages") == 'true')
                 or (packagesmb != 0 and (get_size(packages_path) >= int(packagesmb)))):
            delete_packages(auto_clear=True)
    except Exception as e:
        kodi.log(str(e))
    if kodi.get_setting("accrash") == 'true':
        delete_crash_logs(auto_clear=True)

    if not auto_clear:
        xbmc.executebuiltin("Container.Refresh")
        xbmcgui.Dialog().ok(AddonName, 'Auto Maintenance has been run successfully')


def get_free_space_mb(dirname):
    try:
        if xbmc.getCondVisibility('system.platform.windows'):
            import ctypes
            total_bytes = ctypes.c_int64()
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, ctypes.pointer(total_bytes),
                                                       ctypes.pointer(free_bytes))
            if free_bytes.value != '0 MB Free':
                return free_bytes.value, total_bytes.value
        else:
            import subprocess
            df = subprocess.Popen(['df', dirname], stdout=subprocess.PIPE)
            output = df.communicate()[0].encode('utf-8').split('\n')[1].split()
            try:
                return int(output[3]) * 1024, int(output[1]) * 1024
            except Exception as e:
                kodi.log(str(e))
                return revert_size(output[3]), revert_size(output[1])
    except Exception as e:
        kodi.log(str(e))
        traceback.print_exc(file=sys.stdout)
    return get_kodi_size('System.FreeSpace'), get_kodi_size('System.TotalSpace')


def get_kodi_size(sys_space):
    try:
        space = xbmc.getInfoLabel(sys_space)
        try:
            space = revert_size(space)
        except Exception as e:
            kodi.log(str(e))
            traceback.print_exc(file=sys.stdout)
    except Exception as e:
        kodi.log(str(e))
        traceback.print_exc(file=sys.stdout)
        space = 0
    return space


def revert_size(size):
    for size, multi in re.findall('(\d+\.?\d+?) ?([A-z])', size):
        label = {"": 0, "B": 0, "K": 3, "M": 6, "G": 9, "T": 12, "P": 15, "E": 18, "Z": 21, "Y": 24}
        for key in label:
            if key.lower() == multi.lower():
                size = int(float(size) * 10**label[key])
    return size


def convert_size(size):
    err_defaults = (0, 'Unavailable', 'None', '0B', '0M', '0 MB Free', '0 MB Total', '0M Free', '0M Total')
    if size in err_defaults:
        return '0 B'
    import math
    labels = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    try:
        i = int(math.floor(math.log(int(size), 1000)))
    except Exception as e:
        kodi.log(str(e))
        i = int(0)
    s = round(int(size) / math.pow(1000, i), 2)
    return '%s %s' % (str(s), labels[i])


def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            total_size += os.path.getsize(os.path.join(dirpath, f))
    return total_size


def _is_debugging():
    command = {'jsonrpc': '2.0', 'id': 1, 'method': 'Settings.getSettings',
               'params': {'filter': {'section': 'system', 'category': 'logging'}}}
    js_data = kodi.execute_jsonrpc(command)
    for item in js_data.get('result', {}).get('settings', {}):
        if item['id'] == 'debug.showloginfo':
            return item['value']
    return False


def source_change():
    new_source = userdata_path + "/sources.xml"
    try:
        with open(new_source) as fi:
            a = fi.read()
            if 'fusion.tvaddons.ag' in a:
                b = a.replace('http://www.fusion.tvaddons.ag', 'http://fusion.tvaddons.co')
            elif 'https://code.sourcecode.ag' in a:
                b = a.replace('https://code.sourcecode.ag', 'http://fusion.tvaddons.co')
            else:
                return
            with open(new_source, "w") as fil:
                fil.write(str(b))
    except Exception as e:
        kodi.log(str(e))


def feed_change():
    new_feed = userdata_path + "/RssFeeds.xml"
    try:
        with open(new_feed) as fi:
            a = fi.read()
            if 'TVADDONS' in a:
                b = a.replace('TVADDONS', 'TVADDONSCO')
            else:
                return
            with open(new_feed, "w") as fil:
                fil.write(str(b))
    except Exception as e:
        kodi.log(str(e))
