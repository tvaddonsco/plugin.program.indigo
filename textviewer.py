import os
import json

import xbmc
import xbmcaddon
import xbmcgui

from libs import kodi

# try:
#     from urllib.request import urlopen, Request  # python 3.x
# except ImportError:
#     from urllib2 import urlopen, Request  # python 2.x


Addon = xbmcaddon.Addon()
addon = Addon.getAddonInfo('id')
addonName = Addon.getAddonInfo('name')
moduleName = 'Log Viewer'
dialog = xbmcgui.Dialog()
path = 'log'
content = ''
mode = 'log'

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

        self.first_button = 20294
        self.second_button = 20295
        self.third_button = 20296
        self.fourth_button = 20290
        self.fifth_button = 20297

        self.mode = mode
        self.path, self.contents = text_view(t_path='log')
        self.button_1 = '[B]Kodi Log[/B]'
        self.button_2 = '[B]Old Kodi Log[/B]'
        if not _is_debugging():
            self.button_3 = '[B]Debug On[/B]'
        else:
            self.button_3 = '[B]Debug Off[/B]'
        self.button_4 = '[B]Upload Log[/B]'

    def onInit(self):
        # xbmcgui.Dialog().ok('', path, content)
        if mode == 'nocoin':
            self.path, self.contents = text_view(t_path=path)
            self.button_1 = '[B]NoCoin Log[/B]'
            self.button_2 = '[B]NCError Log[/B]'
            self.button_3 = '[B]Options[/B]'
            self.button_4 = '[B]No Action[/B]'
        elif mode == content:  # content and not path:
            self.contents = content
            self.button_1 = '[B]Contents[/B]'

        # Set Button Labels
        first_button = self.getControl(self.first_button)
        first_button.setLabel(self.button_1)
        second_button = self.getControl(self.second_button)
        second_button.setLabel(self.button_2)
        third_button = self.getControl(self.third_button)
        third_button.setLabel(self.button_3)
        fourth_button = self.getControl(self.fourth_button)
        fourth_button.setLabel(self.button_4)

        # title box
        addon_title_box = self.getControl(self.addon_title_box_control)
        addon_title_box.setText(str.format('%s %s') % (addonName, moduleName))
        
        # content box
        main_content_box = self.getControl(self.main_content_box_control)
        main_content_box.setText(self.contents)
        # main_content_box.setText(contents)

        # file path box
        file_name_box = self.getControl(self.file_name_box_control)
        file_name_box.setLabel(self.path)

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
            if mode == 'nocoin':
                self.path = path
            else:
                if xbmc.translatePath('special://logpath') not in self.path:
                    self.path = get_logpath()
                if '.old.log' in self.path:
                    self.path = self.path.replace('.old.log', '.log')
            self.path, self.contents = text_view(t_path=self.path)
            main_content_box = self.getControl(self.main_content_box_control)
            main_content_box.setText(self.contents)
            file_name_box = self.getControl(self.file_name_box_control)
            file_name_box.setLabel(self.path)

        elif control_id == 20295:
            if mode == 'nocoin':
                if 'nocoin.log' in path:
                    self.path = path.replace('nocoin.log', 'nocoin_error.log')
            else:
                if xbmc.translatePath('special://logpath') not in self.path:
                    self.path = get_logpath()
                if '.old.log' not in self.path:
                    self.path = self.path.replace('.log', '.old.log')
            self.path, old_contents = text_view(t_path=self.path)
            main_content_box = self.getControl(self.main_content_box_control)
            main_content_box.setText(old_contents)
            file_name_box = self.getControl(self.file_name_box_control)
            file_name_box.setLabel(self.path)

        elif control_id == 20296:
            if mode == 'nocoin':
                #  make function to handle options
                import nocoin
                nocoin.nc_options(path)

            else:
                xbmc.executebuiltin("ToggleDebug")
                debug_on_off_button = self.getControl(self.third_button)
                if not _is_debugging():
                    debug_on_off_button.setLabel('Debug Off')
                else:
                    debug_on_off_button.setLabel('Debug On')

        elif control_id == 20290:
            if mode == 'nocoin':
                self.close()
            else:
                xbmc.executebuiltin("RunAddon(script.tvaddons.debug.log)")

        elif control_id == 20297:
            try:
                self.path, kb_contents = text_view(t_path='kb_input', d_path=self.path)
                main_content_box = self.getControl(self.main_content_box_control)
                main_content_box.setText(kb_contents)
                file_name_box = self.getControl(self.file_name_box_control)
                file_name_box.setLabel(self.path)
            except TypeError:
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
    # if not isinstance(command, basestring):
    if not isinstance(command, str):
        command = json.dumps(command)
    response = xbmc.executeJSONRPC(command)
    return json.loads(response)


def keyboard(default="", heading="", hidden=False):
    kb = xbmc.Keyboard(default, heading, hidden)
    kb.doModal()
    if kb.isConfirmed() and kb.getText():
        return str(kb.getText()).encode("utf-8")
    del kb


def get_logpath():        # global path
        # global content
        # path = ''
        # content = ''
    logfile_name = xbmc.getInfoLabel('System.FriendlyName').split()[0].lower()
    l_path = os.path.join(xbmc.translatePath('special://logpath'), logfile_name + '.log')
    if not os.path.isfile(l_path):
        l_path = os.path.join(xbmc.translatePath('special://logpath'), 'kodi.log')
        if not os.path.isfile(l_path):
            pass
    return l_path


def text_view(t_path='', t_contents='', d_path=''):
    # path can be a url to an internet file
    if (not t_path) and (not t_contents):
        return
    if t_path and not t_contents:
        if t_path == 'kb_input':
            t_path = keyboard(default=d_path, heading='Please enter the Url/path to the file you wish to view')
            if not t_path:
                return
        if 'http' in t_path.lower():  # string.lower(t_path):
            try:
                t_contents = kodi.read_file(t_path)
            except Exception as e:
                print(str(e))
                t_contents = 'The web site seems to be having trouble or the file could not be read' \
                             '\nPlease try again later'
        else:
            if t_path == 'log':
                t_path = get_logpath()
            if not os.path.isfile(t_path):
                t_contents = 'Could not find path to file ' + t_path
                return t_path, t_contents
            # Open and read the file from path location
            try:
                with open(t_path, 'rb') as temp_file:
                    t_contents = temp_file.read()
            except IOError:
                t_contents = 'Could not read the file'
    if not t_contents:
        t_contents = 'The file was empty'
    # Set contents for text display function
    t_contents = t_contents.replace(' ERROR: ', ' [COLOR red]ERROR[/COLOR]: ') \
        .replace(' WARNING: ', ' [COLOR gold]WARNING[/COLOR]: ')
    return t_path, t_contents


def window():
    win = Viewer('textview-skin.xml', Addon.getAddonInfo('path'), 'textviewer')
    win.doModal()
    del win


def display(re_path, re_content, re_mode='log'):
    global path, content, mode
    path = re_path
    content = re_content
    mode = re_mode
    window()
