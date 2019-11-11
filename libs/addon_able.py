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


def set_enabled(newaddon, data=None):
    if kodi.get_kversion() > 16.5:
        kodi.log("Enabling " + newaddon)
        setit = 1
        if data is None:
            data = ''
        now = datetime.datetime.now()
        date_time = str(now).split('.')[0]
        # sql = 'REPLACE INTO installed (addonID,enabled) VALUES(?,?)'
        sql = 'REPLACE INTO installed (addonID,enabled,installDate) VALUES(?,?,?)'
        conn.execute(sql, (newaddon, setit, date_time,))
        conn.commit()
        # xbmc.executebuiltin("InstallAddon(%s)" % newaddon)
        # xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
    else:
        pass


def setall_enable():
    if kodi.get_kversion() > 16.5:
        addonfolder = xbmc.translatePath(os.path.join('special://home', 'addons'))
        contents = os.listdir(addonfolder)
        kodi.log(contents)
        conn.executemany('update installed set enabled=1 WHERE addonID = (?)', ((val,) for val in contents))
        conn.commit()

    else:
        pass
