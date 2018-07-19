import os
import shutil

import xbmc
from libs import kodi
import rejuv_run

AddonID = kodi.addon.getAddonInfo('id')
AddonTitle = "Rejuvinate Kodi"


def startup_rejuv():
    yes_pressed = kodi.yesnoDialog(AddonTitle, "Please confirm that you wish you wipe clean your current configuration"
                                               "and reconfigure Kodi with the latest Config Wizard update!",
                                   "                This will result in the loss of all your current data!")
    if yes_pressed:
        addonPath = AddonID.getAddonInfo('path')
        addonPath = xbmc.translatePath(addonPath)
        xbmcPath = os.path.join(addonPath, "..", "..")
        xbmcPath = os.path.abspath(xbmcPath)
        # Directories and sub directories not to remove but to sort through
        dir_exclude = ('addons', 'packages', 'userdata', 'Database')
        #  Directories and sub directories Directories to ignore and leave intact
        sub_dir_exclude = ['metadata.album.universal', 'metadata.artists.universal', 'service.xbmc.versioncheck',
                           'metadata.common.musicbrainz.org', 'metadata.common.imdb.com', AddonID]
        #  Files to ignore and not to be removed
        file_exclude = ('Addons26.db', 'kodi.log', 'Textures13.db, Addons27.db')
        try:
            for (root, dirs, files) in os.walk(xbmcPath, topdown=True):
                dirs[:] = [dir for dir in dirs if dir not in sub_dir_exclude]
                files[:] = [file for file in files if file not in file_exclude]
                for folder in dirs:
                    if folder not in dir_exclude:
                        shutil.rmtree(os.path.join(root, folder))
                for file_name in files:
                    os.remove(os.path.join(root, file_name))
        except Exception as e:
            kodi.log("Rejuv.startup_rejuv User files partially removed - " + str(e))

        rejuv_run.JUVWIZARD()
