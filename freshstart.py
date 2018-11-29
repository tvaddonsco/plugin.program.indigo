import os
import shutil
import re

import xbmc
from libs import kodi

AddonID = kodi.addon.getAddonInfo('id')
AddonTitle = kodi.addon.getAddonInfo('name')


def startup_freshstart():
    if kodi.yesnoDialog("Please confirm that you wish to factory restore your configuration.",
                        "                This will result in the loss of all your current data!",
                        ' ', AddonTitle, nolabel='No', yeslabel='Yes'):
        home_path = xbmc.translatePath(os.path.join('special://home'))
        enableBG16 = "UseCustomBackground,false"
        enableBG17 = "use_custom_bg,false"
        xEB('Skin.SetBool(%s)' % enableBG16)
        xEB('Skin.SetBool(%s)' % enableBG17)
        try:
            win_string = xbmc.translatePath(os.path.join('special://xbmc/')).split('\\')[-2]
            win_string = win_string.split('_')
            win_string = win_string[0] + '_' + win_string[-1]
            kodi.log(win_string)
            win_path = home_path.replace('\Roaming\Kodi', '\Local\Packages\%s\LocalCache\Roaming\Kodi' % win_string)
            if win_path:
                home_path = win_path
        except:
            pass
        #  Directories and sub directories not to remove but to sort through
        dir_exclude = ('addons', 'packages', 'userdata', 'Database')
        #  Directories and sub directories Directories to ignore and leave intact
        sub_dir_exclude = ['metadata.album.universal', 'metadata.artists.universal', 'service.xbmc.versioncheck',
                           'metadata.common.musicbrainz.org', 'metadata.common.imdb.com']
        if kodi.yesnoDialog(AddonTitle, "Do you wish to keep %s installed for convenience after the factory restore?"
                            % AddonTitle, '', nolabel='No', yeslabel='Yes'):
            sub_dir_exclude.extend([AddonID])
        # Files to ignore and not to be removed
        file_exclude = ('kodi.log')  # , 'Textures13.db', 'commoncache.db', 'Addons26.db', 'Addons27.db')
        # db_vers = max(re.findall('Addons\d+.db', str(os.listdir(xbmc.translatePath('special://database')))))
        # file_exclude += db_vers
        try:
            for (root, dirs, files) in os.walk(home_path, topdown=True):
                dirs[:] = [dir for dir in dirs if dir not in sub_dir_exclude]
                files[:] = [file for file in files if file not in file_exclude]
                for folder in dirs:
                    try:
                        if folder not in dir_exclude:
                            shutil.rmtree(os.path.join(root, folder))
                    except:
                        pass
                for file_name in files:
                    try:
                        os.remove(os.path.join(root, file_name))
                    except:
                        pass
            kodi.message(AddonTitle, "Done! , You are now back to a fresh Kodi configuration!",
                         "Click OK to exit Kodi and then restart to complete .")
            xbmc.executebuiltin('ShutDown')
        except Exception as e:
            kodi.log("Freshstart User files partially removed - " + str(e))
            kodi.message(AddonTitle, 'Done! , Freshstart User files partially removed',
                         'Please check the log')


def xEB(t):
    xbmc.executebuiltin(t)
