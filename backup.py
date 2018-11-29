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
from libs import kodi
from libs import viewsetter

dp = xbmcgui.DialogProgress()
AddonTitle = kodi.addon.getAddonInfo('name')
addon_id = kodi.addon_id
selfAddon = xbmcaddon.Addon(id=addon_id)

backupfull = selfAddon.getSetting('backup_database')
backupaddons = selfAddon.getSetting('backup_addon_data')
zip_setting = kodi.get_setting("zip")
zip_path = xbmc.translatePath(os.path.join(zip_setting))

# ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
home_path = xbmc.translatePath('special://home/')
addons_path = xbmc.translatePath(os.path.join('special://home', 'addons', ''))
packages_path = xbmc.translatePath(os.path.join('special://home/addons/' + 'packages'))
userdata_path = xbmc.translatePath(os.path.join('special://home/userdata', ''))
addon_data_path = xbmc.translatePath(os.path.join(userdata_path, 'addon_data'))
databases_path = xbmc.translatePath(os.path.join(userdata_path, 'Database'))
navi_path = xbmc.translatePath(os.path.join(addons_path, 'script.navi-x'))
excludes_folder = xbmc.translatePath(os.path.join(userdata_path, 'BACKUP'))
dialog = xbmcgui.Dialog()


def backup_menu():
    kodi.addItem('[COLOR white]Select Backup Location[/COLOR]', 'url', 'display_backup_settings', '',
                 description="Choose the location to which you wish to store your backups!")
    kodi.addItem('[COLOR white]Full Backup (All Files and Folders Included)[/COLOR]', 'url', 'full_backup', '',
                 description="Backup everything possible!")
    kodi.addItem('[COLOR white]Backup No Database (No Database Files Included)[/COLOR]', 'url', 'small_backup', '',
                 description="Backup your Kodi configuration without unnecessary database files!")
    kodi.addDir('[COLOR white]Restore Backup[/COLOR]', '', 'do_backup_restore', '',
                description="Restore your Kodi configuration from a backup!")
    kodi.addDir('[COLOR white]Delete Backup[/COLOR]', '', 'del_backup', '',
                description="Erase any backups you have saved!")
    viewsetter.set_view("sets")


def check_path():
    if zip_setting == "Click Here":
        kodi.openSettings(addon_id, id1=0, id2=0)
        sys.exit(0)
    if home_path in zip_path:
        dialog.ok(AddonTitle, 'Invalid backup path. The selected path may be removed during backup '
                              'and cause an error. Please pick another path that is not in the Kodi directory')
        kodi.openSettings(addon_id, id1=0, id2=0)
        sys.exit(0)


def get_keyboard(default="", heading="", hidden=False):
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return str(keyboard.getText().encode("utf-8"))
    return default


# #############  Backup  ############################################

def full_backup():
    exclude_dirs = ['backupdir', 'cache', 'temp']
    exclude_files = ["spmc.log", "spmc.old.log", "xbmc.log", "xbmc.old.log", "kodi.log", "kodi.old.log", "fretelly.log",
                     "freetelly.old.log", "ftmc.log", "ftmc.old.log", "firemc.log", "firemc.old.log", "nodi.log", "nodi.old.log"]
    message_header = "%s Is Creating A  Full  Backup..." % AddonTitle
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    archive_cb(home_path, message_header, message1, message2, message3, exclude_dirs, exclude_files)


def no_data_backup():
    exclude_dirs = ['backupdir', 'cache', 'temp', 'Thumbnails', 'Databases']
    exclude_files = ["spmc.log", "spmc.old.log", "xbmc.log", "xbmc.old.log", "kodi.log", "kodi.old.log",
                     "Textures13.db", "fretelly.log", "freetelly.old.log", "ftmc.log", "ftmc.old.log", "firemc.log", "firemc.old.log", "nodi.log", "nodi.old.log"]
    message_header = "%s is creating the backup..." % AddonTitle
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    archive_cb(home_path, message_header, message1, message2, message3, exclude_dirs, exclude_files)


def backup(type):
    exclude_dirs = ['backupdir', 'cache', 'temp', 'Thumbnails', 'Databases']
    exclude_files = ["spmc.log", "spmc.old.log", "xbmc.log", "xbmc.old.log", "kodi.log", "kodi.old.log", "freetelly.log",
                     "freetelly.old.log", "ftmc.log", "ftmc.old.log", "firemc.log", "firemc.old.log", "nodi.log", "nodi.old.log"]
    message_header = "%s Is Creating A Backup..." % AddonTitle
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    if type == 'full':
        message_header = "%s Is Creating A  Full  Backup..." % AddonTitle
        message1 = "Archiving..."
    elif type == 'no_data':
        exclude_dirs.extend(["Textures13.db"])
        exclude_files.extend(["Textures13.db"])
    else:
        return

    archive_cb(home_path, message_header, message1, message2, message3, exclude_dirs, exclude_files)


def archive_cb(sourcefile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    check_path()
    # ##TODO check for file. Prompt to pick another name or replace the existing file
    if not os.path.exists(zip_path):
        os.makedirs(zip_path)
    vq = get_keyboard(heading="Enter a name for this backup")
    if not vq:
        return False, 0
    # ##
    title = urllib.quote_plus(vq)
    destfile = xbmc.translatePath(os.path.join(zip_path, title + '.zip'))
    zipobj = zipfile.ZipFile(destfile, 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    item = []
    dp.create(message_header, message1, message2, message3)
    for base, dirs, files in os.walk(sourcefile):
        for n_file in files:
            item.append(n_file)
    n_item = len(item)
    for base, dirs, files in os.walk(sourcefile):
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
    for zip_file in os.listdir(zip_path):
        if zip_file.endswith(".zip"):
            url = xbmc.translatePath(os.path.join(zip_path, zip_file))
            kodi.addItem(zip_file, url, 'read_zip', '', '', '')


def read_zip(url):
    if not dialog.yesno(AddonTitle, "[COLOR smokewhite]" + url + "[/COLOR]", "Do you want to restore this backup?"):
        sys.exit(1)
    # wipe_backup_restore()
    dp.create(AddonTitle, "Restoring File:", url, '')
    unzip(url, home_path, dp)
    dialog.ok(AddonTitle, "Installation Complete.", "", "Click OK to exit Kodi and then restart to complete .")
    xbmc.executebuiltin('ShutDown')


def remove_paths(path):
        try:
            for root, dirs, files in os.walk(path, topdown=True):
                dirs[:] = [d for d in dirs if d not in excludes_folder]
                for name in files:
                    try:
                        os.unlink(os.path.join(root, name))
                    except Exception as e:
                        kodi.log(str(e))
                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name))
                        os.rmdir(root)
                    except Exception as e:
                        kodi.log(str(e))
        except:
            traceback.print_exc(file=sys.stdout)


def wipe_backup_restore():
    dp.create(AddonTitle, "Restoring Kodi.", 'In Progress.............', 'Please Wait')
    try:
        for root, dirs, files in os.walk(home_path, topdown=True):
            dirs[:] = [d for d in dirs if d not in excludes_folder]
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                    os.rmdir(os.path.join(root, name))
                except:
                    pass

            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name)); os.rmdir(root)
                except:
                    pass
    except:
        pass

    dp.create(AddonTitle, "Cleaning Install", 'Removing old folders.', 'Please Wait')
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    if os.path.exists(databases_path):
        try:
            for root, dirs, files in os.walk(databases_path, topdown=True):
                dirs[:] = [d for d in dirs]
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                        os.rmdir(os.path.join(root, name))
                    except:
                        pass

                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name)); os.rmdir(root)
                    except:
                        pass
        except:
            pass

    if os.path.exists(addon_data_path):
        try:
            for root, dirs, files in os.walk(addon_data_path, topdown=True):
                dirs[:] = [d for d in dirs]
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                        os.rmdir(os.path.join(root, name))
                    except:
                        pass

                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name)); os.rmdir(root)
                    except:
                        pass
        except:
            pass


def REMOVE_EMPTY_FOLDERS():
    # initialize the counters
    empty_count = 0
    used_count = 0
    try:
        for curdir, subdirs, files in os.walk(home_path):
            if len(subdirs) == 0 and len(files) == 0:  # check for empty directories. len(files) == 0 may be overkill
                empty_count += 1  # increment empty_count
                os.rmdir(curdir)  # delete the directory
                # kodi.log("Successfully Removed: "+curdir)
            elif len(subdirs) > 0 and len(files) > 0:  # check for used directories
                used_count += 1  # increment
    except:
        pass


def unzip(_in, _out, dp):
    zin = zipfile.ZipFile(_in, 'r')
    nFiles = float(len(zin.infolist()))
    count = 0
    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            dp.update(int(update), '', '', '[COLOR dodgerblue][B]' + str(item.filename) + '[/B][/COLOR]')
            try:
                zin.extract(item, _out)
            except Exception as e:
                print(str(e))
    except Exception as e:
        print(str(e))
        return False
    return True


def ListBackDel():
    addonfolder = xbmc.translatePath(os.path.join('special://', 'home'))
    for file in os.listdir(zip_path):
        if file.endswith(".zip"):
            url = xbmc.translatePath(os.path.join(zip_path, file))
            kodi.addDir(file, url, 'do_del_backup', '')


def DeleteBackup(url):
    if dialog.yesno(AddonTitle, "[COLOR smokewhite]" + url + "[/COLOR]", "Do you want to delete this backup?"):
        os.remove(url)
        dialog.ok(AddonTitle, "[COLOR smokewhite]" + url + "[/COLOR]", "Successfully deleted.")


def DeleteAllBackups():
    if dialog.yesno(AddonTitle, "Do you want to delete all backups?"):
        shutil.rmtree(zip_path)
        os.makedirs(zip_path)
        dialog.ok(AddonTitle, "All backups successfully deleted.")
