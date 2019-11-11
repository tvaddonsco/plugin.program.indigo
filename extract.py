import zipfile
import xbmc
import sys
import traceback
from libs import kodi


def all(_in, _out, dp=None):
    _in = _in.replace('/storage/emulated/0/', '/sdcard/')
    _out = _out.replace('/storage/emulated/0/', '/sdcard/')
    kodi.log('\t_in= ' + _in + '\t_out= ' + _out)
    try:
        zin = zipfile.ZipFile(_in, 'r')
        if not dp:
            zin.extractall(_out)
        else:
            n_files = float(len(zin.infolist()))
            count = 0
            for item in zin.infolist():
                count += 1
                update = count / n_files * 100
                dp.update(int(update))
                zin.extract(item, _out)
        return True
    except:
        traceback.print_exc(file=sys.stdout)
        try:
            # Built-in cant follow symlinks for the source file
            xbmc.executebuiltin("Extract(%s, %s)" % (_in, _out))
            xbmc.sleep(1800)
            return True
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            kodi.okDialog(str(e), 'Please try again later', 'Attempting to continue...', "There was an error:")
            return False
