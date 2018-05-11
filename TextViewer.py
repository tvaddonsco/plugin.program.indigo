import os
import json

import xbmc
import xbmcaddon
import xbmcgui

try:
    from urllib.request import urlopen, Request  # python 3.x
except ImportError:
    from urllib2 import urlopen, Request  # python 2.x

Addon = xbmcaddon.Addon()
addon = Addon.getAddonInfo('id')
addonName = Addon.getAddonInfo('name')
moduleName = 'Log Viewer'
dialog = xbmcgui.Dialog()
# contents = ''
# path = ''

# get actioncodes from keymap.xml
ACTION_MOVE_LEFT = 1
ACTION_MOVE_RIGHT = 2
ACTION_MOVE_UP = 3
ACTION_MOVE_DOWN = 4
ACTION_PAGE_UP = 5
ACTION_PAGE_DOWN = 6
ACTION_SELECT_ITEM = 7

ACTION_MOUSE_WHEEL_UP = 104  # Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN = 105  # Mouse wheel down
ACTION_MOUSE_DRAG = 106  # Mouse drag
ACTION_MOUSE_MOVE = 107  # Mouse move


class Viewer(xbmcgui.WindowXML):
    contents = ''
    path = ''
    mouse_controls = 4300

    def __init__(self, xml_name, fallback_path, skin_folder):
        super(Viewer, self).__init__(self, xml_name, fallback_path, skin_folder)
        self.page_up = 5
        self.page_down = 6
        self.previous_menu = 10
        self.back = 92
        self.mouse_wheel_up = 104
        self.mouse_wheel_down = 105
        self.mouse_drag = 106

        # XML id's
        self.main_window = 1100
        self.addon_title_box_control = 20301
        self.main_content_box_control = 20302
        self.list_box_control = 20303
        self.file_name_box_control = 20304
        self.line_number_box_control = 20201
        self.scroll_bar_vertical = 20212
        self.debug_on_off_control = 20296

    def onInit(self):
        self.path, self.contents = text_view(path='log')
        # title box
        addon_title_box = self.getControl(self.addon_title_box_control)
        addon_title_box.setText(str.format('%s %s') % (addonName, moduleName))
        
        # content box
        main_content_box = self.getControl(self.main_content_box_control)
        main_content_box.setText(self.contents)

        file_name_box = self.getControl(self.file_name_box_control)
        file_name_box.setLabel(self.path)

        debug_on_off_button = self.getControl(self.debug_on_off_control)
        if not _is_debugging():
            debug_on_off_button.setLabel('[B]Debug On[/B]')
        else:
            debug_on_off_button.setLabel('[B]Debug Off[/B]')

    def onAction(self, action):
        # non Display Button control
        if action == self.previous_menu:
            self.close()
        elif action == self.back:
            self.close()
        elif action == self.mouse_wheel_down:
            xbmc.executebuiltin('PageDown(20212)')
        elif action == self.mouse_wheel_up:
            xbmc.executebuiltin('PageUp(20212)')
    
    def onClick(self, control_id):
        if control_id == 20293:
            self.close()
            window()

        elif control_id == 20294:
            if xbmc.translatePath('special://logpath') not in self.path:
                self.path = get_logpath()
            if '.old.log' not in self.path:
                self.path = self.path.replace('.log', '.old.log')
            self.path, old_contents = text_view(path=self.path)
            main_content_box = self.getControl(self.main_content_box_control)
            main_content_box.setText(old_contents)
            file_name_box = self.getControl(self.file_name_box_control)
            file_name_box.setLabel(self.path)

        elif control_id == 20295:
            if xbmc.translatePath('special://logpath') not in self.path:
                self.path = get_logpath()
            if '.old.log' in self.path:
                self.path = self.path.replace('.old.log', '.log')
            self.path, contents = text_view(path=self.path)
            main_content_box = self.getControl(self.main_content_box_control)
            main_content_box.setText(contents)
            file_name_box = self.getControl(self.file_name_box_control)
            file_name_box.setLabel(self.path)

        elif control_id == self.debug_on_off_control:
            xbmc.executebuiltin("ToggleDebug")
            debug_on_off_button = self.getControl(self.debug_on_off_control)
            if not _is_debugging():
                debug_on_off_button.setLabel('Debug Off')
            else:
                debug_on_off_button.setLabel('Debug On')

        elif control_id == 20297:
            try:
                self.path, kb_contents = text_view(path='kb_input')
                main_content_box = self.getControl(self.main_content_box_control)
                main_content_box.setText(kb_contents)
                file_name_box = self.getControl(self.file_name_box_control)
                file_name_box.setLabel(self.path)
            except TypeError:
                pass

    def onFocus(self, control_id):
        pass


def _is_debugging():
    command = {'jsonrpc': '2.0', 'id': 1, 'method': 'Settings.getSettings',
               'params': {'filter': {'section': 'system', 'category': 'logging'}}}
    js_data = execute_jsonrpc(command)
    for item in js_data.get('result', {}).get('settings', {}):
        if item['id'] == 'debug.showloginfo':
            return item['value']
    return False


def execute_jsonrpc(command):
    if not isinstance(command, basestring):
        command = json.dumps(command)
    response = xbmc.executeJSONRPC(command)
    return json.loads(response)


def keyboard(default="", heading="", hidden=False):
    kb = xbmc.Keyboard(default, heading, hidden)
    kb.doModal()
    if kb.isConfirmed() and kb.getText():
        return unicode(kb.getText(), "utf-8")
    del kb


def get_logpath():
    logfile_name = xbmc.getInfoLabel('System.FriendlyName').split()[0].lower()
    path = os.path.join(xbmc.translatePath('special://logpath'), logfile_name + '.log')
    if not os.path.isfile(path):
        path = os.path.join(xbmc.translatePath('special://logpath'), 'kodi.log')
        if not os.path.isfile(path):
            pass
    return path


def text_view(path='', contents=''):
    # path can be a url to an internet file
    if (not path or path == '' or path is None) and (not contents or contents == '' or contents is None):
        return
    if path and not contents:
        if path == 'kb_input':
            path = keyboard(heading='Please enter the Url/path to the file you wish to view')
            if not path or path == '' or path is None:
                return
        if 'http' in path.lower():  # string.lower(path):
            try:
                req = Request(path)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows U Windows NT 5.1 en-GB rv:1.9.0.3) Gecko/2008092417 '
                                             'Firefox/3.0.3')
                contents = urlopen(req).read()
            except:
                contents = 'The web site seems to be having trouble or the file could not be read' \
                           '\nPlease try again later'
        else:
            if path == 'log':
                path = get_logpath()
            if not os.path.isfile(path):
                contents = 'Could not find path to file ' + path
                return path, contents
            # Open and read the file from path location
            try:
                with open(path, 'rb') as temp_file:
                    contents = temp_file.read()
            except:
                contents = 'Could not read the file'
    if not contents:
        contents = 'The file was empty'
    # Set contents for text display function
    contents = contents.replace(' ERROR: ', ' [COLOR red]ERROR[/COLOR]: ') \
        .replace(' WARNING: ', ' [COLOR gold]WARNING[/COLOR]: ')
    return path, contents


def window():
    win = Viewer('textview-skin.xml', Addon.getAddonInfo('path'), 'textviewer')
    win.doModal()
    del win
