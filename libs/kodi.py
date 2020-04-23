"""
    Kodi Addon
    Copyright (C) 2015 Blazetamer
    Thanks to tknorris
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import json
import os
import re
import sys
import urllib
import traceback
import zipfile
# import urlparse

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

try:
    import strings
except ImportError:
    import string as strings

try:
    from urllib.request import urlopen, Request  # python 3.x
except ImportError:
    from urllib2 import urlopen, Request  # python 2.x

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

try:
    quote_plus = urllib.quote
except AttributeError:
    quote_plus = urllib.parse.quote_plus


addon = xbmcaddon.Addon()

ICON_PATH = os.path.join(addon.getAddonInfo('path'), 'icon.png')

get_setting = addon.getSetting

show_settings = addon.openSettings

AddonTitle = addon.getAddonInfo('name')

addon_id = addon.getAddonInfo('id')

ADDON = xbmcaddon.Addon(id=addon_id)

execute = xbmc.executebuiltin

addonInfo = xbmcaddon.Addon().getAddonInfo

dialog = xbmcgui.Dialog()

progressDialog = xbmcgui.DialogProgress()

windowDialog = xbmcgui.WindowDialog()

artwork = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'art/'))

fanart = artwork + 'fanart.jpg'


def get_path():
    return addon.getAddonInfo('path')


def get_profile():
    return addon.getAddonInfo('profile')


def set_setting(sid, val):
    # print "SETTING IS =" +val
    # if not isinstance(val, basestring): val = str(val)
    val = str(val) if not isinstance(val, str) else val
    addon.setSetting(sid, val)


def get_version():
    return addon.getAddonInfo('version')


def get_id():
    return addon.getAddonInfo('id')


def get_name():
    return addon.getAddonInfo('name')


def get_plugin_url(queries):
    try:
        query = urllib.urlencode(queries)
    except UnicodeEncodeError:
        for k in queries:
            if isinstance(queries[k], str):
                queries[k] = queries[k].encode('utf-8')
        query = urllib.urlencode(queries)
    return sys.argv[0] + '?' + query


def end_of_directory(cache_to_disc=True):
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=cache_to_disc)


def log_notify(title, msg, times, icon):
    xbmc.executebuiltin("XBMC.Notification(" + title + "," + msg + "," + times + "," + icon + ")")


def add_dir(name, url, mode, thumb, cover=None, fan_art=fanart, meta_data=None, is_folder=None, is_playable=None,
            menu_items=None, replace_menu=False, description=None):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode) + "&name=" + quote_plus(name) + "&thumb=" + \
            quote_plus(thumb)
    ok = True
    fan_art = fan_art if fan_art else cover
    # START METAHANDLER
    if meta_data is None:
        thumb = thumb
    else:
        thumb = meta_data['cover_url']
        fan_art = meta_data['backdrop_url']
    print(u if ADDON.getSetting('debug') == "true" else '')
    menu_items = [] if not menu_items else menu_items

    if is_folder is None:
        is_folder = False if is_playable else True

    if is_playable is None:
        playable = 'false' if is_folder else 'true'
    else:
        playable = 'true' if is_playable else 'false'
    list_item = xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
    list_item.setProperty('fanart_image', fan_art)
    if meta_data is None:
        list_item.setInfo('video', {'title': list_item.getLabel(), 'plot': description})
        list_item.setArt({'poster': thumb, 'fanart_image': fan_art, 'banner': 'banner.png'})
    else:
        list_item.setInfo('video', u)
    list_item.setProperty('isPlayable', playable)
    # list_item.addContextMenuItems(menu_items)
    list_item.addContextMenuItems(menu_items, replaceItems=replace_menu)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, list_item, isFolder=is_folder)
    return ok


# #NON CLICKABLE####

def add_item(name, url, mode, iconimage, fan_art=fanart, description=None):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode) + "&name=" + quote_plus(
        name) + "&fanart=" + quote_plus(fan_art)

    # u = (sys.argv[0] + "?url=" + url + "&mode=" + str(mode) + "&name=" +
    #      name + "&fanart=" + (fan_art) + "&type=" + "video").replace(' ', '+')

    # dialog.ok('', u)'

    liz = xbmcgui.ListItem(name, u, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo('video', {'title': liz.getLabel(), 'plot': description})
    liz.setProperty("fanart_image", fan_art)
    liz.setArt({'poster': iconimage, 'fanart_image': fan_art, 'banner': 'banner.png'})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok


def create_item(queries, label, thumb='', fan_art='', is_folder=None, is_playable=None, total_items=0, menu_items=None,
                replace_menu=False):
    list_item = xbmcgui.ListItem(label, iconImage=thumb, thumbnailImage=thumb)
    add_item2(queries, list_item, fan_art, is_folder, is_playable, total_items, menu_items, replace_menu)


def add_item2(queries, list_item, fan_art='', is_folder=None, is_playable=None, total_items=0, menu_items=None,
              replace_menu=False):
    menu_items = [] if menu_items is None else menu_items
    if is_folder is None:
        is_folder = False if is_playable else True

    if is_playable is None:
        playable = 'false' if is_folder else 'true'
    else:
        playable = 'true' if is_playable else 'false'

    liz_url = get_plugin_url(queries)
    list_item.setProperty('fanart_image', fan_art) if fan_art else ''
    list_item.setInfo('video', {'title': list_item.getLabel()})
    list_item.setProperty('isPlayable', playable)
    list_item.addContextMenuItems(menu_items, replaceItems=replace_menu)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, list_item, isFolder=is_folder, totalItems=total_items)


def parse_query(query):
    q = {'mode': 'main'}
    query = query[1:] if query.startswith('?') else query
    queries = urlparse.parse_qs(query)
    for key in queries:
        if len(queries[key]) == 1:
            q[key] = queries[key][0]
        else:
            q[key] = queries[key]
    return q


def notify(header=None, msg='', duration=2000, sound=None):
    header = get_name() if header is None else header
    if sound is None:
        sound = get_setting('mute_notifications')
        if sound == 'true':
            sound = False
        else:
            sound = True
    xbmcgui.Dialog().notification(header, msg, ICON_PATH, duration, sound)


def dl_notify(header=None, msg='', icon=None, duration=2000, sound=None):
    header = get_name() if header is None else header
    if sound is None:
        sound = get_setting('mute_notifications')
        if sound == 'true':
            sound = False
        else:
            sound = True
    xbmcgui.Dialog().notification(header, msg, icon, duration, sound)


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    if minutes > 60:
        hours, minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
    else:
        return "%02d:%02d" % (minutes, seconds)


def addon_icon():
    return artwork + 'icon.png'


def message(text1, text2="", text3=""):
    if text3 == "":
        xbmcgui.Dialog().ok(text1, text2)
    elif text2 == "":
        xbmcgui.Dialog().ok("", text1)
    else:
        xbmcgui.Dialog().ok(text1, text2, text3)


def info_dialog(msg, heading=addonInfo('name'), icon=addon_icon(), time=3000):
    try:
        dialog.notification(heading, msg, icon, time, sound=False)
    except Exception as e:
        execute("Notification(%s,%s, %s, %s)" % (heading, msg, time, icon))
        log(str(e))


def yesno_dialog(line1, line2, line3, heading=addonInfo('name'), nolabel='', yeslabel=''):
    return dialog.yesno(heading, line1, line2, line3, nolabel, yeslabel)


def ok_dialog(line1, line2, line3, heading=addonInfo('name')):
    return dialog.ok(heading, line1, line2, line3)


def select_dialog(lst, heading=addonInfo('name')):
    return dialog.select(heading, lst)


def version():
    num = ''
    try:
        # ver = addon('xbmc.addon').getAddonInfo('version')
        ver = addonInfo('version')
    except NameError:
        ver = '999'
    for i in ver:
        if i.isdigit():
            num += i
        else:
            break
    return int(num)


def refresh():
    return execute('Container.Refresh')


def idle():
    return execute('Dialog.Close(busydialog)')


def queue_item():
    return execute('Action(Queue)')


def open_playlist():
    return execute('ActivateWindow(VideoPlaylist)')


def open_settings(addons_id, id1=None, id2=None):
    execute('Addon.OpenSettings(%s)' % addons_id)
    if id1 is not None:
        execute('SetFocus(%i)' % (id1 + 200))
    if id2 is not None:
        execute('SetFocus(%i)' % (id2 + 100))


def set_content(content):
    xbmcplugin.setContent(int(sys.argv[1]), content)


def auto_view(content):
    view = 'default-view'
    if get_setting('auto-view') == 'true':
        if content in ('files', 'songs', 'artists', 'albums', 'movies', 'tvshows', 'episodes', 'musicvideos'):
            view = str(content + '-view')
    else:
        content = 'movies'
    xbmcplugin.setContent(int(sys.argv[1]), content)
    xbmc.executebuiltin("Container.SetViewMode(%s)" % get_setting(view))  # 'default-view'))


def log(msg, level=xbmc.LOGNOTICE):
    name = str(AddonTitle) + ' NOTICE'
    # override message level to force logging when addon logging turned on
    # level = xbmc.LOGNOTICE

    try:
        xbmc.log('%s: %s' % (name, msg), level)
    except Exception as e:
        try:
            xbmc.log('Logging Failure', level)
            log(str(e))
        except TypeError as e:
            log(str(e))  # just give up


def log_info(msg, level=xbmc.LOGNOTICE):
    name = AddonTitle + ' INFORMATION'
    # override message level to force logging when addon logging turned on
    # level = xbmc.LOGNOTICE
    try:
        xbmc.log('%s: %s' % (name, msg), level)
    except Exception as e:
        try:
            xbmc.log('Logging Failure', level)
            log(str(e))
        except Exception as e:
            log(str(e))  # just give up


def get_kversion():
    full_version_info = xbmc.getInfoLabel('System.BuildVersion')
    baseversion = full_version_info.split(".")
    intbase = int(baseversion[0])
    # if intbase > 16.5:
    # 	log('HIGHER THAN 16.5')
    # if intbase < 16.5:
    # 	log('LOWER THAN 16.5')
    return intbase


def get_codename():
    codename = 'Unknown'
    xbmc_version = xbmc.getInfoLabel("System.BuildVersion")
    versions = {10: 'Dharma', 11: 'Eden', 12: 'Frodo', 13: 'Gotham', 14: 'Helix', 15: 'Isengard', 16: 'Jarvis',
                17: 'Krypton', 18: 'Leia', 19: 'Matrix'}
    try:
        codename = versions.get(int(xbmc_version[:2]))
    except Exception as e:
        log(str(e))
    if codename == 'Leia' and sys.version_info[0] > 2:
        return 'Migration'
    return codename


def i18n(string_id):
    try:
        return addon.getLocalizedString(strings.STRINGS[string_id]).encode('utf-8', 'ignore')
    except Exception as e:
        xbmc.log('%s: Failed String Lookup: %s (%s)' % (get_name(), string_id, e), xbmc.LOGWARNING)
        return string_id


def open_url(url, link=''):
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 '
                  'Safari/537.1',
                  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
                  'Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1')
    try:
        import random
        req = Request(url)
        req.add_header('User-Agent', random.choice(user_agent))
        response = urlopen(req)
        link = response.read().decode('utf-8')
        response.close()
    except Exception as e:
        log(str(e))
        traceback.print_exc(file=sys.stdout)
    return link


def read_file(path, contents='', headers=''):  # , params=None,  verify_ssl=False, timeout = 10):
    headers = headers if headers else {}
    try:
        if path.startswith('http'):  # Internet File or Page
            if 'User-Agent' not in headers or 'user-agent' not in headers:
                import random
                header = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                         'like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'},
                          {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) '
                                         'Chrome/21.0.1180.75 Safari/537.1'},
                          {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                                         'Chrome/41.0.2228.0 Safari/537.36'},
                          {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'})
                # headers.update(random.choice(header))
                headers = (random.choice(header))
            response = urlopen(Request(path, headers=headers))
            # import requests
            # ## verify = True does not work on all https websites
            # r = requests.get(path, params=params, headers=headers, verify=verify_ssl, allow_redirects=True,
            #                  timeout=timeout)
            # if r.status_code == requests.codes.ok:
            #     return r.text
        elif os.path.isfile(path):  # Local File
            response = open(path, 'rb')
        else:
            return contents
        contents = response.read().decode('utf-8')
        response.close()
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        log('ERROR read_file: ' + str(e))
    return contents


def translate_path(path):
    return xbmc.translatePath(path).decode('utf-8')


def execute_jsonrpc(command):
    # if not isinstance(command, basestring):
    if not isinstance(command, str):
        command = json.dumps(command)
    response = xbmc.executeJSONRPC(command)
    return json.loads(response)


def get_var(path, name):
    with open(path, 'r') as content:
        var = re.search(name + '''.+?(\w+|'[^']*'|"[^"]*")''', content.read()).group(1)
    return var.replace("'", '').replace('"', '')


def find_all_paths(file_name, path):
    paths = []
    for root, dirs, files in os.walk(path):
        if file_name in files:
            paths.append(os.path.join(root, file_name))
    return paths


def ext_all(_in, _out, dp=None):
    # extract_all(_in, _out, dp)
    # return
    _in = _in.replace('/storage/emulated/0/', '/sdcard/')
    _out = _out.replace('/storage/emulated/0/', '/sdcard/')
    zin = None
    log('\t_in= ' + _in + '\t_out= ' + _out)

    # #####     read zip     #####
    try:
        zin = zipfile.ZipFile(_in, 'r', allowZip64=True)
    except Exception as e:
        log(str(e))
        traceback.print_exc(file=sys.stdout)
        for path in find_all_paths(os.path.basename(_in), os.path.abspath(os.sep)):  # '/storage')
            log('\t trying source path: ' + path)
            try:
                zin = zipfile.ZipFile(path, 'r', allowZip64=True)
                if zin:
                    break
            except Exception as e:
                log(str(e))
                traceback.print_exc(file=sys.stdout)

    # #####    extract zip     #####
    try:
        if not dp:
            zin.extractall(_out)
        else:
            n_files = float(len(zin.infolist()))
            count = 0
            for item in zin.infolist():
                if dp:
                    count += 1
                    update = count / n_files * 100
                    dp.update(int(update))  # , '', '', '[COLOR dodgerblue][B]' + str(item.filename) + '[/B][/COLOR]')
                zin.extract(item, _out)
        return True
    except Exception as e:
        log(str(e))
        traceback.print_exc(file=sys.stdout)
        try:
            xbmc.executebuiltin("Extract(%s, %s)" % (_in, _out))
            xbmc.sleep(1800)
            return True
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            # all(_in, _out, dp=None)
            ok_dialog(str(e), 'Please try again later', 'Attempting to continue...', "There was an error:")
            return False


def extract_all(_in, _out, dp=None):
    _in = _in.replace('/storage/emulated/0/', '/sdcard/')
    _out = _out.replace('/storage/emulated/0/', '/sdcard/')
    log('\t_in= ' + _in + '\t_out= ' + _out)
    try:
        zin = zipfile.ZipFile(_in, 'r')  # , allowZip64=True)
        if not dp:
            zin.extractall(_out)
        else:
            n_files = float(len(zin.infolist()))
            count = 0
            for item in zin.infolist():
                count += 1
                update = count / n_files * 100
                dp.update(int(update))  # , '', '', '[COLOR dodgerblue][B]' + str(item.filename) + '[/B][/COLOR]')
                zin.extract(item, _out)
        return True
    except Exception as e:
        log(str(e))
        traceback.print_exc(file=sys.stdout)
        try:
            # Built-in cant follow symlinks for the source file
            xbmc.executebuiltin("Extract(%s, %s)" % (_in, _out))
            xbmc.sleep(1800)
            return True
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            ok_dialog(str(e), 'Please try again later', 'Attempting to continue...', "There was an error:")
            return False
