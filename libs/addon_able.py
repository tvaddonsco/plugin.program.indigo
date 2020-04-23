import datetime
import os
from sqlite3 import dbapi2 as db_lib

import xbmc
import xbmcaddon
from libs import kodi

addon_id = kodi.addon_id
db_dir = xbmc.translatePath("special://profile/Database")
db_path = os.path.join(db_dir, 'Addons27.db')

conn = db_lib.connect(db_path)
conn.text_factory = str

ADDON = xbmcaddon.Addon(id=kodi.addon_id)


def set_enabled(newaddon):
    if kodi.get_kversion() > 16.5:
        kodi.log("Enabling " + newaddon)
        setit = 1
        now = datetime.datetime.now()
        date_time = str(now).split('.')[0]
        sql = 'REPLACE INTO installed (addonID,enabled,installDate) VALUES(?,?,?)'
        conn.execute(sql, (newaddon, setit, date_time,))
        conn.commit()
        xbmc.executebuiltin("UpdateAddonRepos") if newaddon.startswith('repo') else ''
        xbmc.executebuiltin("UpdateLocalAddons") if not newaddon.startswith('repo') else ''


def setall_enable():
    if kodi.get_kversion() > 16.5:
        addonfolder = xbmc.translatePath(os.path.join('special://home', 'addons'))
        contents = os.listdir(addonfolder)
        kodi.log(contents)
        conn.executemany('update installed set enabled=1 WHERE addonID = (?)', ((val,) for val in contents))
        conn.commit()
        xbmc.executebuiltin("UpdateAddonRepos")
        xbmc.sleep(500)
        xbmc.executebuiltin("UpdateLocalAddons")


def set_disabled(addon):
    if kodi.get_kversion() > 16.5:
        xbmc.executebuiltin("StopScript(%s)" % addon)
        conn.execute('DELETE FROM installed WHERE addonID=?', (addon,))
        conn.commit()
        xbmc.executebuiltin("Container.Update", True)
        xbmc.executebuiltin("Container.Refresh")
        xbmc.executebuiltin("UpdateAddonRepos") if addon.startswith('repo') else ''
        xbmc.executebuiltin("UpdateLocalAddons")
