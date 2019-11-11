# Config Wizard By: Blazetamer 2013-2016
import os
import re

import downloader
import extract
import xbmc
import xbmcgui
from libs import addon_able, kodi

AddonTitle = kodi.addon.getAddonInfo('name')
SiteDomain = 'TVADDONS.CO'
dialog = xbmcgui.Dialog()

wizlink = "http://indigo.tvaddons.co/wizard/updates.txt"
cutslink = "http://indigo.tvaddons.co/wizard/shortcuts.txt"


def JUVWIZARD(filetype='main'):
    if xbmcgui.Dialog().yesno("Please Confirm",
                              "                Please confirm that you wish to automatically",
                              "            configure Kodi with all the best addons and tweaks!",
                              "              ", "Cancel", "Install"):
        filetype = filetype.lower()
        if filetype == 'main':
            addonfolder = xbmc.translatePath('special://home')
        elif filetype == 'addon':
            addonfolder = xbmc.translatePath(os.path.join('special://home', 'addons'))
        else:
            print({'filetype': filetype})
            dialog.ok("Error!", 'filetype: "%s"' % str(filetype))
            return
        link = kodi.read_file(wizlink).replace('\n', '').replace('\r', '').replace('\a', '').strip()
        # kodi.log(link)
        if '[error]' in link:
            print(link)
            dialog.ok("Error!", link)
            return
        path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
        lib = os.path.join(path, 'rejuv.zip')
        try:
            os.remove(lib)
        except:
            pass
        # ## ## ... ##
        dp = xbmcgui.DialogProgress()
        dp.create(AddonTitle, " ", 'Downloading and Configuring ', 'Please Wait')
        downloader.download(link, lib, dp)
        xbmc.sleep(4000)
        extract.all(lib, addonfolder, dp)
        xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
        addon_able.setall_enable()
        try:
            addon_able.set_enabled("inputstream.adaptive")
        except:
            pass
        xbmc.sleep(4000)
        try:
            addon_able.set_enabled("inputstream.rtmp")
        except:
            pass
        xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
        try:
            os.remove(lib)
        except:
            pass
        if filetype == 'main':
            link = kodi.read_file(cutslink)
            shorts = re.compile('shortcut="(.+?)"').findall(link)
            for shortname in shorts:
                xEB('Skin.SetString(%s)' % shortname)
                enableBG16 = "UseCustomBackground,true"
                enableBG17 = "use_custom_bg,true"
                xEB('Skin.SetBool(%s)' % enableBG16)
                xEB('Skin.SetBool(%s)' % enableBG17)

        kodi.set_setting("wizardran",'true')
        dialog.ok(AddonTitle, "Installation Complete.", "", "Click OK to exit Kodi and then restart to complete .")
        xbmc.executebuiltin('ShutDown')


def xEB(t): xbmc.executebuiltin(t)
