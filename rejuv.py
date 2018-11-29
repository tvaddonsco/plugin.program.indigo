import os
import shutil
import re

import xbmc
from libs import kodi
import rejuv_run

AddonID = kodi.addon.getAddonInfo('id')
AddonTitle = "Rejuvinate Kodi"


def startup_rejuv():
    if kodi.yesnoDialog("Please confirm that you wish you wipe clean your current configuration"
                        "and reconfigure Kodi with the latest Config Wizard update!",
                        "        This will result in the loss of all your current data!", '',AddonTitle):
        addonPath = kodi.addon.getAddonInfo('path')
        addonPath = xbmc.translatePath(addonPath)
        xbmcPath = os.path.join(addonPath, "..", "..")
        xbmcPath = os.path.abspath(xbmcPath)
        # Directories and sub directories not to remove but to sort through
        dir_exclude = ('addons', 'packages', 'userdata', 'Database', 'temp')
        #  Directories and sub directories Directories to ignore and leave intact
        sub_dir_exclude = ['metadata.album.universal', 'metadata.artists.universal', 'service.xbmc.versioncheck',
                           'metadata.common.musicbrainz.org', 'metadata.common.imdb.com', AddonID]
        # if kodi.yesnoDialog(AddonTitle, "Do you wish to keep %s installed for convenience after the factory restore?"
        #                     % AddonTitle, '', nolabel='No', yeslabel='Yes'):
        #     sub_dir_exclude.extend([AddonID])
        #  Files to ignore and not to be removed
        file_exclude = ('kodi.log')  # , 'Textures13.db','Addons26.db',  'Addons27.db')
        db_vers = max(re.findall('Addons\d+.db', str(os.listdir(xbmc.translatePath('special://database')))))
        file_exclude += db_vers
        try:
            for (root, dirs, files) in os.walk(xbmcPath, topdown=True):
                dirs[:] = [dir for dir in dirs if dir not in sub_dir_exclude]
                files[:] = [file for file in files if file not in file_exclude]
                for folder in dirs:
                    if folder not in dir_exclude:
                        try:
                            shutil.rmtree(os.path.join(root, folder))
                        except:
                            pass
                for file_name in files:
                    try:
                        os.remove(os.path.join(root, file_name))
                    except:
                        pass
        except Exception as e:
            kodi.log("Rejuv.startup_rejuv User files partially removed - " + str(e))

        rejuv_run.JUVWIZARD()
