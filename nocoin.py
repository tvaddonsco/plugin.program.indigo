import os
import re
import base64
import datetime
import shutil
import traceback
import xbmc
import xbmcgui
import xbmcaddon
import tarfile
import zipfile
from zipfile import ZipFile
from libs import kodi

# try:
#     from urllib.request import urlopen, Request  # python 3.x
# except ImportError:
#     from urllib2 import urlopen, Request  # python 2.x

addon_id = xbmcaddon.Addon().getAddonInfo('id')
profile_path = os.path.join(xbmc.translatePath('special://profile/'), 'addon_data/', addon_id)
addons_path = os.path.join(xbmc.translatePath('special://home/'), 'addons/')
log_file = os.path.join(profile_path, 'nocoin.log')
error_log_file = os.path.join(profile_path, 'nocoin_error.log')
setting = xbmcaddon.Addon().getSetting


class Ziplevels:
    def __init__(self):
        self.path = ''
        self.name = ''
        self.tmp_dir = ''


def zip_file(zip_main_file_path, zip_main_file_name, main_directory, definitions, _totals_):
    tmp_dir = main_directory + '/temp_unzips'
    zip_list = Ziplevels()
    zip_list.path = zip_main_file_path
    zip_list.name = zip_main_file_name
    zip_list.tmp_dir = os.path.join(tmp_dir, os.path.splitext(zip_list.name)[0])
    classes = [zip_list]
    try:
        for mylists in classes:
            if not os.path.exists(mylists.tmp_dir):
                os.makedirs(mylists.tmp_dir)
            z_file = tarfile.open(mylists.path) if tarfile.is_tarfile(mylists.path) else ZipFile(mylists.path)
            with z_file as zip_dir_path:
                zip_dir_path.extractall(path=mylists.tmp_dir)
                for (tmp_dir_name, tmp_sub_dir, tmp_file_name) in os.walk(mylists.tmp_dir, topdown=True):
                    for zip_file_name in tmp_file_name:
                        tmp_dir_path = os.path.join(tmp_dir_name, zip_file_name)
                        if zipfile.is_zipfile(zip_file_name) or tarfile.is_tarfile(tmp_dir_path):
                            temp_list = Ziplevels()
                            temp_list.path = tmp_dir_path
                            temp_list.name = zip_file_name
                            temp_list.tmp_dir = os.path.splitext(tmp_dir_path)[0]
                            classes.append(temp_list)
                        else:
                            file_check(tmp_dir_path, zip_file_name, main_directory, definitions, _totals_,
                                       zip_main_file_name)
        shutil.rmtree(tmp_dir)
    except Exception as e:
        log(zip_main_file_path + '  Is not a valid zipfile', str(e))


def file_check(file_path, file_name, main_directory, definitions, _totals_, zip_name=''):
    a_name = 'Unknown'
    mining_count = 0
    source_file_decoded = []
    try:
        with open(file_path, 'r+') as source_file:
            match2 = re.findall('''[\"|\']([^\'|"]*)[\'|\"]''', source_file.read())
            for text in match2:
                try:
                    if base64.b64encode(base64.b64decode(text)) == text:
                        decoded_text = base64.b64decode(text)
                        if decoded_text:
                            source_file_decoded.append(decoded_text)
                except TypeError:
                    pass
        for line_d in definitions.splitlines():
            with open(file_path, 'r+') as source_file:
                if line_d in file_path or line_d in str(source_file_decoded) or line_d in source_file.read():
                    for folders in 'addons/', '_data/':
                        match = re.search(folders + '([^/]*)', file_path)
                        if match:
                            if match.group(1) != 'temp_unzips':
                                a_name = match.group(1)
                            break
                    if a_name == 'Unknown':
                        for (m_directory, m_sub_dir, m_files) in os.walk(addons_path, topdown=True):
                            for f_name in m_files:
                                if not f_name.endswith('.zip'):
                                    main_file_path = os.path.join(m_directory, f_name)
                                    try:
                                        with open(main_file_path, 'r+') as source:
                                            if file_name in source.read():
                                                match = re.search('addons/([^/]*)', main_file_path)
                                                if match:
                                                    a_name = match.group(1)
                                                    break
                                    except Exception as e:
                                        log(error=str(e))
                    if 'temp_unzips' in file_path:
                        t_file_path = os.path.join(main_directory, zip_name)
                        file_name = zip_name
                    else:
                        t_file_path = file_path
                    occur = 'Occurrence of %s\nAddon: %s\nFile: %s\nPath: %s\n' \
                            % (line_d, a_name, file_name, t_file_path)
                    _totals_['total_occurrences'].append(occur)
                    mining_count += 1
        _totals_['total_mining_instances'] += mining_count
        _totals_['total_file_count'] += 1
    except Exception as e:
        log(error=str(e))


def log(text='', error=''):
    _file = error_log_file if error else log_file
    with open(_file, 'a+') as logfile:
        logfile.write(text + '\n')
        if error:
            traceback.print_exc(file=logfile)
            logfile.write(' ' + '\n')


# def open_url(path):
#     req = Request(path)
#     req.add_header('User-Agent',
#                    'Mozilla/5.0 (Windows U Windows NT 5.1 en-GB rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#     return urlopen(req).read().decode('utf-8')


def get_definitions():
    defs = ''
    log('Definition Locations:')
    default_defs = [setting('default_url')] if setting('default_url_t') == "true" else []
    # user_defs = 'https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/hosts.txt'
    for numb in range(0, 6):
        user_def = xbmcaddon.Addon().getSetting('user_url' + str(numb))
        if user_def:
            default_defs.append(user_def)
    for def_list in default_defs:
        log('    ' + def_list)
        try:
            # definitons = open_url(def_list) if 'http' in def_list else str(open(def_list, 'rb'))
            definitons = kodi.read_file(def_list) if 'http' in def_list else str(open(def_list, 'rb'))
            for line in definitons.splitlines():
                if line and not line.startswith('#'):
                    for pattern in ('[^\/]*\/\/([^$]*)', '\s([^$]*)', '([\d+\.]+)\s'):
                        match = re.search(pattern, line)
                        if match:
                            match = match.group(1).replace('*', '')
                            if match not in defs and match != '0.0.0.0':
                                defs += str(match + '\n')  # default_defs.append(match)
            if 'http' not in def_list:
                definitons.close()
        except Exception as e:
            log(error=str(e))
    log(' ')
    return defs


def nocoin():
    _totals_ = {'total_occurrences': [],
                'total_mining_instances': 0,
                'total_file_count': 0,
                }
    f_count = 1
    fz_count = 0
    start_time = datetime.datetime.now()
    # if called from service or auto run, skip dp reporting
    dp = xbmcgui.DialogProgress()
    dp.create('Scanning')
    dp.update(0)
    if os.path.exists(log_file):
        os.remove(log_file)
    if os.path.exists(error_log_file):
            os.remove(error_log_file)
    definitions = get_definitions()
    directories = [xbmc.translatePath('special://home/')] if setting('scan_default_dir') == 'true' else []
    if setting('scan_warning') == 'true':
        for numb in range(0, 7):
            scan_dir = xbmcaddon.Addon().getSetting('scan_dir' + str(numb))
            if scan_dir:
                directories.append(scan_dir)
    for directory_to_test in directories:
        f_count = sum(len(main_files) for _, _, main_files in os.walk(directory_to_test))
    for directory_to_test in directories:
        for (main_directory, main_sub_dir, main_files) in os.walk(directory_to_test, topdown=True):
            for main_file_name in main_files:
                main_file_path = os.path.join(main_directory, main_file_name)
                # if called from service or auto run, skip dp reporting
                percent = 100 * fz_count / f_count if 100 * fz_count / f_count >= 0 else 0
                dp.update(int(percent), os.path.dirname(main_file_path), main_file_name,
                          '%s of %s    %s%%' % (fz_count, f_count, percent))
                if dp.iscanceled():
                    dp.close()
                    return
                try:
                    if zipfile.is_zipfile(main_file_name) or tarfile.is_tarfile(main_file_path):
                        zip_file(main_file_path, main_file_name, main_directory, definitions, _totals_)
                    else:
                        file_check(main_file_path, main_file_name, main_directory, definitions, _totals_)
                    fz_count += 1
                except Exception as e:
                    log('could not open ' + main_file_path, str(e))
    # if called from service or auto run, skip dp reporting
    dp.close()
    if not _totals_['total_occurrences'] and not _totals_['total_mining_instances']:
        log('The Files are Clean')
    if _totals_['total_occurrences']:
        for occur in _totals_['total_occurrences']:
            log(occur)
        log('\ntotal mining instances = %s' % _totals_['total_mining_instances'])
    log('total files checked = %s \nScan Complete: Elapsed Time = %s'
        % (_totals_['total_file_count'], (datetime.datetime.now() - start_time)))
    log('Last run: %s' % datetime.datetime.now())
    # if ran from service or auto run, regex log for time stamp from service
    # if ran from service or auto run, call nc_options(log_file) directly if _totals_['total_mining_instances'] > 0
    import textviewer
    textviewer.display(log_file, '', 'nocoin')


def nc_options(nc_path):
    addon_list = []
    dialog = xbmcgui.Dialog()
    with open(nc_path, 'rb') as temp_file:
        nc_contents = temp_file.read()
        match = re.findall('Addon: ([^\n]*)\nFile: ([^\n]*)\nPath: ([^\n]*)', nc_contents)
        if not match:
            dialog.ok('No Instances Found', 'Nothing to do at this time.')
            return
        for addon_name, file_name, path_name in match:
            if not addon_list:
                addon_list = [[addon_name, file_name, path_name]]
            else:
                if path_name not in str(addon_list):
                    addon_list.append([addon_name, file_name, path_name])
        index = dialog.select('Choose an Instance', [inst[0] for inst in addon_list])
        if index > -1:
            i_addon = str(addon_list[index][0])
            i_file = str(addon_list[index][1])
            i_path = str(addon_list[index][2])
            if i_addon == 'Unknown':
                action = dialog.select(i_file, ['Take No Action', ' Delete file'])
                if action == 1 and os.path.isfile(i_path):
                    if dialog.yesno('Delete File', 'Please Confirm that you want to Delete', i_path):
                        os.remove(i_path)
                        status = 'Could not remove file' if os.path.isfile(i_path) else 'File has been removed'
                        dialog.ok('Delete File', i_path, status)
            else:
                action = dialog.select(i_addon, ['Take No Action', 'Disable', 'Uninstall'])
                if action == 1:
                    if dialog.yesno('Disable', 'Please Confirm that you want to Disable', i_addon):
                        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":'
                                            '{"addonid": "%s","enabled":false}}' % i_addon)
                        status = 'Could not Disable addon' if xbmc.getCondVisibility("System.HasAddon(%s)" % i_addon) \
                            else 'Addon is Disabled'
                        dialog.ok('Disable', i_addon, status)
                elif action == 2:
                    if dialog.yesno('Uninstall Addon', 'Please Confirm that you want to Uninstall', i_addon):
                        shutil.rmtree(addons_path + i_addon)
                        status = 'Could not Uninstall addon' if os.path.isdir(addons_path + i_addon) \
                            else 'addon has been Uninstalled'
                        dialog.ok('Uninstall Addon', addons_path + i_addon, status)
                        if os.path.isdir(profile_path + i_addon):
                            if dialog.yesno('Uninstall Userdata', 'Please Confirm that you also want to Remove the ',
                                            i_addon + ' Userdata/addon_data folder'):
                                shutil.rmtree(profile_path + i_addon)
                                status = 'Could not Remove Addons Userdata' if os.path.isdir(profile_path + i_addon) \
                                    else 'Addons Userdata has been Removed'
                                dialog.ok('Uninstall Userdata', profile_path + i_addon, status)
                        if os.path.isfile(i_path):
                            if dialog.yesno('Uninstall File', 'Please Confirm that you also want to Remove ', i_file):
                                os.remove(i_path)
                                status = 'Could not Remove ' + i_file if os.path.isfile(i_path) \
                                    else i_file + ' has been Removed'
                                dialog.ok('Uninstall File', status)
