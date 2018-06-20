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
import urlparse

import strings
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

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


def set_setting(id, value):
    # print "SETTING IS =" +value
    if not isinstance(value, basestring): value = str(value)
    addon.setSetting(id, value)


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
            if isinstance(queries[k], unicode):
                queries[k] = queries[k].encode('utf-8')
        query = urllib.urlencode(queries)
    return sys.argv[0] + '?' + query


def end_of_directory(cache_to_disc=True):
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=cache_to_disc)


def LogNotify(title, message, times, icon):
    xbmc.executebuiltin("XBMC.Notification(" + title + "," + message + "," + times + "," + icon + ")")


def addDir(name, url, mode, thumb, cover=None, fanart=fanart, meta_data=None, is_folder=None,
           is_playable=None,
           menu_items=None, replace_menu=False, description=None):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(
        mode) + "&name=" + urllib.quote_plus(
        name) + "&thumb=" + urllib.quote_plus(thumb)

    ok = True
    if fanart is None:
        fanart = ''
    contextMenuItems = []
    # START METAHANDLER
    if meta_data is None:
        # meta_data =[]
        thumb = thumb
    else:
        thumb = meta_data['cover_url']
        fanart = meta_data['backdrop_url']
    if ADDON.getSetting('debug') == "true":
        print u
    if menu_items is None: menu_items = []

    if is_folder is None:
        is_folder = False if is_playable else True

    if is_playable is None:
        playable = 'false' if is_folder else 'true'
    else:
        playable = 'true' if is_playable else 'false'
    list_item = xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
    list_item.setProperty('fanart_image', fanart)
    if meta_data is None:
        list_item.setInfo('video', {'title': list_item.getLabel(), 'plot': description})
        list_item.setArt({'poster': thumb, 'fanart_image': fanart, 'banner': 'banner.png'})
    else:
        list_item.setInfo('video', meta_data)
    list_item.setProperty('isPlayable', playable)
    list_item.addContextMenuItems(menu_items)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, list_item, isFolder=is_folder)
    return ok


# #NON CLICKABLE####

def addItem(name, url, mode, iconimage, fanart=fanart, description=None):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&fanart=" + urllib.quote_plus(fanart)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo('video', {'title': liz.getLabel(), 'plot': description})
    liz.setProperty("fanart_image", fanart)
    liz.setArt({'poster': iconimage, 'fanart_image': fanart, 'banner': 'banner.png'})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def create_item(queries, label, thumb='', fanart='', is_folder=None, is_playable=None, total_items=0, menu_items=None,
                replace_menu=False):
    list_item = xbmcgui.ListItem(label, iconImage=thumb, thumbnailImage=thumb)
    add_item(queries, list_item, fanart, is_folder, is_playable, total_items, menu_items, replace_menu)


def add_item(queries, list_item, fanart='', is_folder=None, is_playable=None, total_items=0, menu_items=None,
             replace_menu=False):
    if menu_items is None: menu_items = []
    if is_folder is None:
        is_folder = False if is_playable else True

    if is_playable is None:
        playable = 'false' if is_folder else 'true'
    else:
        playable = 'true' if is_playable else 'false'

    liz_url = get_plugin_url(queries)
    if fanart: list_item.setProperty('fanart_image', fanart)
    list_item.setInfo('video', {'title': list_item.getLabel()})
    list_item.setProperty('isPlayable', playable)
    list_item.addContextMenuItems(menu_items, replaceItems=replace_menu)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, list_item, isFolder=is_folder, totalItems=total_items)


def parse_query(query):
    q = {'mode': 'main'}
    if query.startswith('?'): query = query[1:]
    queries = urlparse.parse_qs(query)
    for key in queries:
        if len(queries[key]) == 1:
            q[key] = queries[key][0]
        else:
            q[key] = queries[key]
    return q


def notify(header=None, msg='', duration=2000, sound=None):
    if header is None: header = get_name()
    if sound is None:
        sound = get_setting('mute_notifications')
        if sound == 'true':
            sound = False
        else:
            sound = True
    xbmcgui.Dialog().notification(header, msg, ICON_PATH, duration, sound)


def dl_notify(header=None, msg='', icon=None, duration=2000, sound=None):
    if header is None: header = get_name()
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


def addonIcon():
    return artwork + 'icon.png'


def message(text1, text2="", text3=""):
    if text3 == "":
        xbmcgui.Dialog().ok(text1, text2)
    elif text2 == "":
        xbmcgui.Dialog().ok("", text1)
    else:
        xbmcgui.Dialog().ok(text1, text2, text3)


def infoDialog(message, heading=addonInfo('name'), icon=addonIcon(), time=3000):
    try:
        dialog.notification(heading, message, icon, time, sound=False)
    except:
        execute("Notification(%s,%s, %s, %s)" % (heading, message, time, icon))


def yesnoDialog(line1, line2, line3, heading=addonInfo('name'), nolabel='', yeslabel=''):
    return dialog.yesno(heading, line1, line2, line3, nolabel, yeslabel)


def okDialog(line1, line2, line3, heading=addonInfo('name')):
    return dialog.ok(heading, line1, line2, line3)


def selectDialog(list, heading=addonInfo('name')):
    return dialog.select(heading, list)


def version():
    num = ''
    try:
        version = addon('xbmc.addon').getAddonInfo('version')
    except:
        version = '999'
    for i in version:
        if i.isdigit():
            num += i
        else:
            break
    return int(num)


def refresh():
    return execute('Container.Refresh')


def idle():
    return execute('Dialog.Close(busydialog)')


def queueItem():
    return execute('Action(Queue)')


def openPlaylist():
    return execute('ActivateWindow(VideoPlaylist)')


def openSettings(addon_id, id1=None, id2=None):
    execute('Addon.OpenSettings(%s)' % addon_id)
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
    xbmc.executebuiltin("Container.SetViewMode(%s)" % get_setting('default-view'))


def log(msg, level=xbmc.LOGNOTICE):
    name = str(AddonTitle) + ' NOTICE'
    # override message level to force logging when addon logging turned on
    level = xbmc.LOGNOTICE

    try:
        xbmc.log('%s: %s' % (name, msg), level)
    except:
        try:
            xbmc.log('Logging Failure', level)
        except:
            pass  # just give up


def logInfo(msg, level=xbmc.LOGNOTICE):
    name = AddonTitle + ' INFORMATION'
    # override message level to force logging when addon logging turned on
    level = xbmc.LOGNOTICE

    try:
        xbmc.log('%s: %s' % (name, msg), level)
    except:
        try:
            xbmc.log('Logging Failure', level)
        except:
            pass  # just give up


def get_kversion():
    full_version_info = xbmc.getInfoLabel('System.BuildVersion')
    baseversion = full_version_info.split(".")
    intbase = int(baseversion[0])
    # if intbase > 16.5:
    # 	log('HIGHER THAN 16.5')
    # if intbase < 16.5:
    # 	log('LOWER THAN 16.5')
    return intbase


def i18n(string_id):
    try:
        return addon.getLocalizedString(strings.STRINGS[string_id]).encode('utf-8', 'ignore')
    except Exception as e:
        xbmc.log('%s: Failed String Lookup: %s (%s)' % (get_name(), string_id, e), xbmc.LOGWARNING)
        return string_id


def translate_path(path):
    return xbmc.translatePath(path).decode('utf-8')


def execute_jsonrpc(command):
    if not isinstance(command, basestring):
        command = json.dumps(command)
    response = xbmc.executeJSONRPC(command)
    return json.loads(response)


def get_var(path, name):
    with open(path, 'r') as content:
        try:
            var = re.search(name + '''.+?(\w+|'[^']*'|"[^"]*")''', content.read()).group(1)
        except Exception as e:
            xbmc.log('%s: Failed Variable Match: %s (%s)' % (addon_id, path, e), xbmc.LOGWARNING)
            var = ''
    return var.replace("'", '').replace('"', '')
