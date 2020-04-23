import shutil
import time
import urllib
import zipfile
import traceback

import os
import sys
import xbmc
import xbmcaddon
import xbmcgui
# import extract
from libs import kodi
from libs import viewsetter

dp = xbmcgui.DialogProgress()
AddonTitle = kodi.addon.getAddonInfo('name')
addon_id = kodi.addon.getAddonInfo('id')
selfAddon = xbmcaddon.Addon(id=addon_id)

zip_setting = kodi.get_setting("zip")
zip_path = xbmc.translatePath(os.path.join(zip_setting))
home_path = xbmc.translatePath('special://home/')
logfile_name = xbmc.getInfoLabel('System.FriendlyName').split()[0].lower()
dialog = xbmcgui.Dialog()


def backup_menu():
    kodi.add_item('[COLOR white]Select Backup Location[/COLOR]', 'url', 'display_backup_settings', '',
                 description="Choose the location to which you wish to store your backups!")
    kodi.add_item('[COLOR white]Full Backup (All Files and Folders Included)[/COLOR]', 'url', 'full_backup', '',
                 description="Backup everything possible!")
    kodi.add_item('[COLOR white]Backup No Database (No Database Files Included)[/COLOR]', 'url', 'small_backup', '',
                 description="Backup your Kodi configuration without unnecessary database files!")
    kodi.add_dir('[COLOR white]Restore Backup[/COLOR]', '', 'do_backup_restore', '',
                description="Restore your Kodi configuration from a backup!")
    kodi.add_dir('[COLOR white]Delete Backup[/COLOR]', '', 'del_backup', '',
                description="Erase any backups you have saved!")
    viewsetter.set_view("sets")


def check_path():
    if zip_setting == "Click Here":
        kodi.open_settings(addon_id, id1=0, id2=0)
        sys.exit(0)
    if home_path in zip_path:
        dialog.ok(AddonTitle, 'Invalid backup path. The selected path may be removed during backup '
                              'and cause an error. Please pick another path that is not in the Kodi directory')
        kodi.open_settings(addon_id, id1=0, id2=0)
        sys.exit(0)


def get_keyboard(default="", heading="", hidden=False):
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return str(keyboard.getText().encode("utf-8"))
    return default


def set_name():
    vq = get_keyboard(heading="Enter a name for this backup")
    if not vq:
        return False
    try:
        title = urllib.quote_plus(vq)
    except AttributeError:
        title = urllib.parse.quote_plus(vq)
    return title


# #############  Backup  ############################################

def backup(b_type):
    exclude_dirs = ['cache', 'archive_cache', 'temp', kodi.get_setting('zip').strip('/')]
    exclude_files = [logfile_name + '.log', logfile_name + '.old.log']
    message_header = "%s Is Creating A %s Backup..." % (AddonTitle, b_type.replace('_', ' ').title())
    message1 = "Archiving..."
    if b_type == 'no_data':
        exclude_dirs.extend(['Thumbnails', 'Databases'])
        exclude_files.extend(["Textures13.db"])
    check_path()
    if not os.path.exists(zip_path):
        os.makedirs(zip_path)
    title = set_name()
    if not title:
        return
    destfile = xbmc.translatePath(os.path.join(zip_path, str(title) + '.zip'))
    if os.path.exists(destfile):
        if not dialog.yesno('File Name Already Exists', 'Would You like to Create Another File',
                            'Or Overwrite The Existing File?', '', 'Overwrite File', 'Create Another'):
            os.remove(destfile)
        else:
            title = set_name()
            if not title:
                return False, 0
            destfile = xbmc.translatePath(os.path.join(zip_path, str(title) + '.zip'))
    try:
        zipobj = zipfile.ZipFile(destfile, 'w', zipfile.ZIP_DEFLATED)  # , allowZip64=True)
    except IOError as e:
        dialog.ok('ERROR', 'Could Not Use This Location for Backup', 'Please Chose Another Location', str(e))
        return
    rootlen = len(home_path)
    for_progress = []
    item = []
    dp.create(message_header, message1, '', '')
    for base, dirs, files in os.walk(home_path):
        for n_file in files:
            item.append(n_file)
    n_item = len(item)
    for base, dirs, files in os.walk(home_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files]
        for file_n in files:
            try:
                for_progress.append(file_n)
                progress = len(for_progress) / float(n_item) * 100
                dp.update(int(progress), "Archiving..", '[COLOR blue]%s[/COLOR]' % file_n, '')
                fp = os.path.join(base, file_n)
                zipobj.write(fp, fp[rootlen:])
            except Exception as e:
                kodi.log(str(e))
    zipobj.close()
    dp.close()
    time.sleep(1)
    dialog.ok("[COLOR gold][B]SUCCESS![/B][/COLOR]", 'Your backup was completed successfully!.', "Backup Location: ",
              '[COLOR=yellow]' + destfile + '[/COLOR]')
    

# ################  Restore  ####################################
def restore():
    if zip_path != 'Click Here':
        for zip_file in os.listdir(zip_path):
            if zip_file.endswith(".zip"):
                url = xbmc.translatePath(os.path.join(zip_path, zip_file))
                kodi.add_item(zip_file, url, 'read_zip', '', '', '')


def find_all_paths(file_name, path):
    paths = []
    for root, dirs, files in os.walk(path):
        if file_name in files:
            paths.append(os.path.join(root, file_name))
    return paths


def read_zip(zip_name):
    if not dialog.yesno(AddonTitle, "[COLOR smokewhite]" + zip_name + "[/COLOR]", "Do you want to restore this backup?",
                        os.path.basename(zip_name)):
        sys.exit(1)
    dp.create(AddonTitle, "Restoring Kodi.", 'In Progress.............', 'Please Wait')

    zip_name.replace('/storage/emulated/0/', '/sdcard/')
    home_path.replace('/storage/emulated/0/', '/sdcard/')
    zin = None
    kodi.log('\t_in= ' + zip_name + '\t_out= ' + home_path)

    # #####     read zip     #####
    try:
        zin = zipfile.ZipFile(zip_name, 'r')  # , allowZip64=True)
    except Exception as e:
        kodi.log(e)
        traceback.print_exc(file=sys.stdout)
        for path in find_all_paths(os.path.basename(zip_name), os.path.abspath(os.sep)):  # '/storage')
            kodi.log('\t trying source path: ' + path)
            try:
                zin = zipfile.ZipFile(path, 'r')  # , allowZip64=True)
                if zin:
                    break
            except Exception as e:
                kodi.log(e)
                traceback.print_exc(file=sys.stdout)

    if not zin:
        dialog.ok(AddonTitle + 'Restore', "Could Not Read Backup Zip File.", "Click OK to Exit Restore.")
        return
    # wipe_backup_restore()

    dp.create(AddonTitle, "Restoring File:", zip_name, '')
    # kodi.ext_all(zip_name, home_path, dp)
    # kodi.extract_all(zip_name, home_path, dp)
    # extract.extract_all(zip_name, home_path, dp)

    # #####     extract zip     #####
    try:
        if not dp:
            zin.extractall(home_path)
        else:
            n_files = float(len(zin.infolist()))
            count = 0
            for item in zin.infolist():
                if dp:
                    count += 1
                    update = count / n_files * 100
                    dp.update(int(update))  # , '', '', '[COLOR dodgerblue][B]' + str(item.filename) + '[/B][/COLOR]')
                zin.extract(item, home_path)
        return True
    except Exception as e:
        kodi.log(e)
        traceback.print_exc(file=sys.stdout)
        try:
            xbmc.executebuiltin("Extract(%s, %s)" % (zip_name, home_path))
            xbmc.sleep(1800)
            # return True
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            # all(_in, _out, dp=None)
            dialog.ok(str(e), 'Please try again later', 'Attempting to continue...', "There was an error:")
            return False

    dialog.ok(AddonTitle, "Installation Complete.", "", "Click OK to exit Kodi and then restart to complete.")
    xbmc.executebuiltin('ShutDown')


def wipe_backup_restore():
    dir_exclude = ('addons', 'temp')
    sub_dir_exclude = [addon_id]
    file_exclude = [logfile_name + '.log']
    dp.create(AddonTitle, "Cleaning Install", 'Removing old folders.', 'Please Wait')
    for (root, dirs, files) in os.walk(home_path, topdown=True):
        dirs[:] = [d for d in dirs if d not in sub_dir_exclude]
        files[:] = [f for f in files if f not in file_exclude]
        for folder in dirs:
            try:
                if folder not in dir_exclude:
                    shutil.rmtree(os.path.join(root, folder))
            except Exception as e:
                kodi.log(e)
                traceback.print_exc(file=sys.stdout)
        for file_name in files:
            try:
                os.remove(os.path.join(root, file_name))
            except Exception as e:
                kodi.log(e)
                traceback.print_exc(file=sys.stdout)
        

def list_back_del():
    for f in os.listdir(zip_path):
        if f.endswith(".zip"):
            url = xbmc.translatePath(os.path.join(zip_path, f))
            kodi.add_dir(f, url, 'do_del_backup', '')


def delete_backup(url):
    if dialog.yesno(AddonTitle, "[COLOR smokewhite]" + url + "[/COLOR]", "Do you want to delete this backup?",
                    os.path.basename(url)):
        os.remove(url)
        dialog.ok(AddonTitle, "[COLOR smokewhite]" + url + "[/COLOR]", "Successfully deleted.")


def delete_all_backups():
    if dialog.yesno(AddonTitle, "Do you want to delete all backups?"):
        shutil.rmtree(zip_path)
        os.makedirs(zip_path)
        dialog.ok(AddonTitle, "All backups successfully deleted.")
