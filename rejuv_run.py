# Config Wizard By: Blazetamer 2013-2016
import os
import re
import urllib2

import downloader
import extract
import xbmc
import xbmcgui
from libs import addon_able, kodi

AddonTitle = kodi.addon.getAddonInfo('name')
SiteDomain = 'TVADDONS.CO'

wizlink = "http://indigo.tvaddons.co/wizard/updates.txt"
cutslink = "http://indigo.tvaddons.co/wizard/shortcuts.txt"


def JUVWIZARD():
    filetype = 'main'
    link = OPEN_URL(wizlink).replace('\n', '').replace('\r', '').replace('\a', '').strip()
    path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
    url = link
    confirm = xbmcgui.Dialog().yesno("Please Confirm",
                                     "                Please confirm that you wish to automatically",
                                     "            configure Kodi with all the best addons and tweaks!",
                                     "              ", "Cancel", "Install")
    filetype = filetype.lower()
    if confirm:
        path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
        dp = xbmcgui.DialogProgress()
        dp.create(AddonTitle, " ", 'Downloading and Configuring ', 'Please Wait')
        lib = os.path.join(path, 'rejuv.zip')
        try:
            os.remove(lib)
        except:
            pass
        # ## ## ... ##
        # kodi.log(url)
        if str(url).endswith('[error]'):
            print url
            dialog = xbmcgui.Dialog()
            dialog.ok("Error!", url)
            return
        if '[error]' in url:
            print url
            dialog = xbmcgui.Dialog()
            dialog.ok("Error!", url)
            return
        downloader.download(url, lib, dp)
        if filetype == 'main':
            addonfolder = xbmc.translatePath('special://home')
        elif filetype == 'addon':
            addonfolder = xbmc.translatePath(os.path.join('special://home', 'addons'))
        else:
            print {'filetype': filetype}
            dialog = xbmcgui.Dialog()
            dialog.ok("Error!", 'filetype: "%s"' % str(filetype))
            return
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
        try:
            os.remove(lib)
        except:
            pass
        if filetype == 'main':
            link = OPEN_URL(cutslink)
            shorts = re.compile('shortcut="(.+?)"').findall(link)
            for shortname in shorts:
                xEB('Skin.SetString(%s)' % shortname)
                enableBG16 = "UseCustomBackground,true"
                enableBG17 = "use_custom_bg,true"
                xEB('Skin.SetBool(%s)' % enableBG16)
                xEB('Skin.SetBool(%s)' % enableBG17)

        xbmc.sleep(4000)
        xbmc.executebuiltin('XBMC_UpdateLocalAddons()')
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
        # kodi.set_setting("wizardran",'true')

        dialog = xbmcgui.Dialog()
        dialog.ok(AddonTitle, "Installation Complete.", "", "Click OK to exit Kodi and then restart to complete .")
        xbmc.executebuiltin('ShutDown')


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTB Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link


def xEB(t): xbmc.executebuiltin(t)
