import xbmc
import xbmcgui
import xbmcaddon
import os
from libs import kodi

Addon = xbmcaddon.Addon()
addon_id = Addon.getAddonInfo('id')
settings = xbmcaddon.Addon(id=addon_id)

ACTION_LEFT = 1  # Left arrow key
ACTION_RIGHT = 2  # Right arrow key
ACTION_UP = 3  # Up arrow key
ACTION_DOWN = 4  # Down arrow key
ACTION_PAGE_UP = 5
ACTION_PAGE_DOWN = 6
ACTION_SELECT_ITEM = 7
ACTION_PARENT_DIR = 9
ACTION_PREVIOUS_MENU = 10  # ESC action
ACTION_SHOW_INFO = 11
ACTION_NEXT_ITEM = 14
ACTION_PREV_ITEM = 15
ACTION_BACKSPACE = 110
ACTION_CONTEXT_MENU = 117

ACTION_MOUSE_WHEEL_UP = 104  # Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN = 105  # Mouse wheel down
ACTION_MOUSE_DRAG = 106  # Mouse drag
ACTION_MOUSE_MOVE = 107  # Mouse move

KEY_NAV_BACK = 92
KEY_HOME = 159
KEY_ESC = 61467


class PopupNote(xbmcgui.WindowXMLDialog):
    xbmc.executebuiltin("UpdateAddonRepos")
    contents = ''
    note = 4001
    support = 4002
    social_media = 4003
    git_browser = 4004
    remind_later = 4005
    dismiss = 4006

    def __init__(self, xml_name, addons_path, skin_folder):
        super(PopupNote, self).__init__(self, xml_name, addons_path, skin_folder)
        self.page_up = 5
        self.page_down = 6
        self.previous_menu = 10
        self.back = 92
        self.buttonClicked = None

        # XML id's
        self.title_box_control = 20301
        self.content_box_control = 20302

    def onInit(self):
        self.contents = settings.getSetting("noteMessage")
        title_box = self.getControl(self.title_box_control)
        title_box.setText("[B][COLOR lime]Unofficial Kodi Community Updates[/COLOR][/B]")
        content_box = self.getControl(self.content_box_control)
        content_box.setText(self.contents)

    def onAction(self, action):
        if action in (self.previous_menu, self.back):
            settings.setSetting("noteType", '')
            settings.setSetting("noteImage", '')
            settings.setSetting("noteMessage", '')
            self.close()

    def onClick(self, control_id):
        if control_id == self.git_browser:
            settings.setSetting("noteType", '')
            settings.setSetting("noteImage", '')
            settings.setSetting("noteMessage", '')
            #xbmc.executebuiltin("UpdateAddonRepos")
            #xbmc.sleep(50)
            self.close()
            import installer
            installer.github_main('')
            
        elif control_id == self.remind_later:
            settings.setSetting("noteType", '')
            settings.setSetting("noteImage", '')
            settings.setSetting("noteMessage", '')
            self.close()

        elif control_id == self.dismiss:
            self.close()

        elif control_id == 4007:
            xbmcgui.Dialog().ok('', str(control_id))

    def onFocus(self, control_id):
        if control_id == self.note:
            title_box = self.getControl(self.title_box_control)
            title_box.setText("[B][COLOR lime]Unofficial Kodi Community Updates[/COLOR][/B]")
            content_box = self.getControl(self.content_box_control)
            content_box.setText(self.contents)

        elif control_id == self.support:
            title_box = self.getControl(self.title_box_control)
            title_box.setText("[B][COLOR lime]Need Assistance? We're Here![/COLOR][/B]")
            contents = '\n\nPlease visit our discussion forums at [COLOR blue]www.tvaddons/forums[/COLOR] where someone is always eager to be of assistance.'
            content_box = self.getControl(self.content_box_control)
            content_box.setText(contents)

        elif control_id == self.social_media:
            title_box = self.getControl(self.title_box_control)
            title_box.setText("[B][COLOR lime]Follow us for the latest updates[/COLOR][/B]")
            contents = '\n\nTwitter: [COLOR blue]@tvaddonsco[/COLOR]' \
                       '\nFacebook: [COLOR blue]www.facebook.com/tvaddonsco[/COLOR]' \
                       '\nInstagram: [COLOR blue]@tvaddonsco[/COLOR]' \
                       '\nYouTube: [COLOR blue]www.youtube.com/c/TVADDONSCO[/COLOR]'
            content_box = self.getControl(self.content_box_control)
            content_box.setText(contents)

        elif control_id == self.git_browser:
            title_box = self.getControl(self.title_box_control)
            title_box.setText("[B][COLOR lime]Git Browser[/COLOR][/B]")
            contents = '\n\nGit Browser is the new and improved method of installing unrestricted Kodi addons, regardless of whether we approve of them or not. Connect directly to the GitHub repositories of your favourite Kodi addon developers. Search for GitHub Usernames Kodi on Google if you have trouble figuring out which ones to look up.'
            content_box = self.getControl(self.content_box_control)
            content_box.setText(contents)

        elif control_id == self.remind_later:
            title_box = self.getControl(self.title_box_control)
            title_box.setText("[B][COLOR lime]Remind Me Later[/COLOR][/B]")
            contents = '\n\nShow this notification the next time Kodi starts.'
            content_box = self.getControl(self.content_box_control)
            content_box.setText(contents)

        elif control_id == self.dismiss:
            title_box = self.getControl(self.title_box_control)
            title_box.setText("[B][COLOR lime]Dismiss Notice[/COLOR][/B]")
            contents = '\n\nHide this notification until the next update.' \
                       '\nOpt out of notices permanently within the Indigo tool.'
            content_box = self.getControl(self.content_box_control)
            content_box.setText(contents)

        elif control_id == 4007:
            xbmcgui.Dialog().ok('', str(control_id))


def art(f, fe=''):
    fe1 = ('.png', '.jpg', '.gif', '.wav', '.txt')
    for ext in fe1:
        if ext in f:
            f = f.replace(ext, '')
            fe = ext
            break
    return xbmc.translatePath(addon_path(f + fe))


def artp(f, fe='.png'):
    return art(f, fe)


def artj(f, fe='.jpg'):
    return art(f, fe)


def addon_path(f, fe=''):
    path = settings.getAddonInfo('path')
    return xbmc.translatePath(os.path.join(path, f + fe))


def check_news2(message_type, override_service=False):
    # debob(["notifications-on-startup", settings.getSetting("notifications-on-startup"), "override_service ",
    #        override_service])
    if (settings.getSetting("notifications-on-startup") == 'false') or override_service:
        info_location = "http://indigo.tvaddons.co/notifications/news.txt"
        info_location2 = addon_path("test.txt")
        info_location3 = addon_path("url.txt")
        try:
            if os.path.isfile(info_location2):
                with open(info_location2, 'rb') as temp_file:
                    html = temp_file.read()
            elif os.path.isfile(info_location3):
                with open(info_location3, 'rb') as temp_file:
                    html = kodi.read_file(temp_file.read().strip()) if temp_file.read() else ''
            else:
                # html = open_url(info_location)
                html = kodi.read_file(info_location)
        except IOError:
            html = ''
        new_image = html.split('|||')[0].strip() if '|||' in html else ''
        new_message = html.split('|||')[1].strip() if '|||' in html else html
        old_note_image = settings.getSetting("noteImage")
        old_note_message = settings.getSetting("noteMessage")
        old_note_image = old_note_image.replace(artp('blank1'), '')
        new_note = ((len(new_image) > 0) or (len(new_message) > 0))
        old_note = (len(old_note_image) > 0 or len(old_note_message) > 0)
        if ((old_note and (not new_note or (old_note_image == new_image or old_note_message == new_message)))
                or (not old_note and not new_note)) and not override_service:
            return
        if new_note and (not old_note_image == new_image) or (not old_note_message == new_message):
            settings.setSetting("noteType", message_type)
            settings.setSetting("noteImage", new_image)
            settings.setSetting("noteMessage", new_message)
        win = PopupNote('note-skin.xml', Addon.getAddonInfo('path'), 'notification')
        win.doModal()
        del win
