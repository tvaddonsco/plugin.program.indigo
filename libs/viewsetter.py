# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------

import sys
import xbmc
import xbmcaddon
import xbmcplugin

addon = xbmcaddon.Addon()
get_setting = addon.getSetting

THUMBNAIL = "thumbnail"
LIST = "list"
MOVIES = "movies"
TV_SHOWS = "tvshows"
SEASONS = "seasons"
EPISODES = "episodes"
OTHER = "other"
SETS = "sets"

# Suggested view codes for each type from different skins (initial list thanks to xbmcswift2 library)
ALL_VIEW_CODES = {
    'list': {
        'skin.confluence': 50,  # List
        'skin.aeon.nox': 50,  # List
        'skin.droid': 50,  # List
        'skin.quartz': 50,  # List
        'skin.re-touched': 50,  # List
        'skin.estuary': 50,
        # 50 = List, 51 = Poster, 52 = Lists,53 = Shift, 54 = InfoWall  55 = Wide list, 500 = Wall,501= List, 502 = Fanart
    },
    'thumbnail': {
        'skin.confluence': 501,  # Thumbnail
        'skin.aeon.nox': 500,  # Wall
        'skin.droid': 51,  # Big icons
        'skin.quartz': 51,  # Big icons
        'skin.re-touched': 500,  # Thumbnail
        'skin.estuary': 500,
        # 50 = List, 51 = Poster, 52 = Lists, 53 = Shift, 54 = InfoWall  55 = Wide list, 500 = Wall,501= List, 502 = Fanart
    },
    'movies': {
        'skin.confluence': 500,  # Thumbnail 515, # Media Info 3
        'skin.aeon.nox': 500,  # Wall
        'skin.droid': 51,  # Big icons
        'skin.quartz': 52,  # Media info
        'skin.re-touched': 500,  # Thumbnail
        'skin.estuary': 52,
        # 50 = List, 51 = Poster,52 = Lists,53 = Shift, 54 = InfoWall  55 = Wide list, 500 = Wall,501= List, 502 = Fanart
    },
    'tvshows': {
        'skin.confluence': 500,  # Thumbnail 515, # Media Info 3
        'skin.aeon.nox': 500,  # Wall
        'skin.droid': 51,  # Big icons
        'skin.quartz': 52,  # Media info
        'skin.re-touched': 500,  # Thumbnail
        'skin.estuary': 54,
        # 50 = List, 51 = Poster,52 = Lists, 53 = Shift, 54 = InfoWall  55 = Wide list, 500 = Wall,501= List, 502 = Fanart
    },
    'seasons': {
        'skin.confluence': 50,  # List
        'skin.aeon.nox': 50,  # List
        'skin.droid': 50,  # List
        'skin.quartz': 52,  # Media info
        'skin.re-touched': 50,  # List
        'skin.estuary': 53,
        # 50 = List, 51 = Poster,52 = Lists, 53 = Shift, 54 = InfoWall  55 = Wide list, 500 = Wall,501= List, 502 = Fanart
    },
    'episodes': {
        'skin.confluence': 500,  # Media Info
        'skin.aeon.nox': 518,  # Infopanel
        'skin.droid': 50,  # List
        'skin.quartz': 52,  # Media info
        'skin.re-touched': 550,  # Wide
        'skin.estuary': 55.
        # 50 = List, 51 = Poster,52 = Lists,53 = Shift,54 = InfoWall  55 = Wide list, 500 = Wall,501= List, 502 = Fanart
    },
    'sets': {
        'skin.confluence': 500,  # List
        'skin.aeon.nox': 50,  # List
        'skin.droid': 50,  # List
        'skin.quartz': 50,  # List
        'skin.re-touched': 50,  # List
        'skin.estuary': 55,
        # 50 = List, 51 = Poster,52 = Lists,53 = Shift,54 = InfoWall  55 = Wide list, 500 = Wall,501= List, 502 = Fanart
    },
}


def set_view(view_mode, view_code=0):
    if get_setting('auto-view') == 'true':
        try:
            # Set the content for extended library views if needed
            xbmcplugin.setContent(int(sys.argv[1]), view_mode)
            if view_mode == MOVIES:
                xbmcplugin.setContent(int(sys.argv[1]), "movies")
            elif view_mode == TV_SHOWS:
                xbmcplugin.setContent(int(sys.argv[1]), "tvshows")
            elif view_mode == SEASONS:
                xbmcplugin.setContent(int(sys.argv[1]), "seasons")
            elif view_mode == EPISODES:
                xbmcplugin.setContent(int(sys.argv[1]), "episodes")
            elif view_mode == THUMBNAIL:
                xbmcplugin.setContent(int(sys.argv[1]), "thumbnail")
            elif view_mode == LIST:
                xbmcplugin.setContent(int(sys.argv[1]), "list")
            elif view_mode == SETS:
                xbmcplugin.setContent(int(sys.argv[1]), "sets")
        except:
            pass
        skin_name = xbmc.getSkinDir()  # Reads skin name
        try:
            if view_code == 0:
                view_codes = ALL_VIEW_CODES.get(view_mode)
                # kodi.log(view_codes)
                view_code = view_codes.get(skin_name)
                # kodi.log(view_code)
                xbmc.executebuiltin("Container.SetViewMode(" + str(view_code) + ")")
            # kodi.log("Setting First view code "+str(view_code)+" for view mode "+str(view_mode)+" and skin "+skin_name)
            else:
                xbmc.executebuiltin("Container.SetViewMode(" + str(view_code) + ")")
            # kodi.log("Setting Second view code for view mode "+str(view_mode)+" and skin "+skin_name)
        except:
            # kodi.log("Unable to find view code "+str(view_code)+" for view mode "+str(view_mode)+" and skin "+skin_name)
            pass
        # else:
        # 	xbmc.executebuiltin("Container.SetViewMode(sets)")
