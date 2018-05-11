import xbmc, time
import xbmcaddon
import kodi

addon = xbmcaddon.Addon()
name = addon.getAddonInfo('name')

LOGDEBUG = xbmc.LOGDEBUG
LOGERROR = xbmc.LOGERROR
LOGFATAL = xbmc.LOGFATAL
LOGINFO = xbmc.LOGINFO
LOGNONE = xbmc.LOGNONE
LOGNOTICE = xbmc.LOGNOTICE
LOGSEVERE = xbmc.LOGSEVERE
LOGWARNING = xbmc.LOGWARNING

def log(msg, level=xbmc.LOGNOTICE):
    # override message level to force logging when addon logging turned on
    if addon.getSetting('debug') == 'true' and level == xbmc.LOGDEBUG:
        level = xbmc.LOGNOTICE
    
    try: xbmc.log('%s: %s' % (name, msg), level)
    except:
        try: xbmc.log('Logging Failure', level)
        except: pass  # just give up



def trace(method):
    #  @debug decorator
    def method_trace_on(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()
        log('{name!r} time: {time:2.4f}s args: |{args!r}| kwargs: |{kwargs!r}|'.format(name=method.__name__, time=end - start, args=args, kwargs=kwargs), LOGDEBUG)
        return result

    def method_trace_off(*args, **kwargs):
        return method(*args, **kwargs)

    if __is_debugging():
        return method_trace_on
    else:
        return method_trace_off

def __is_debugging():
    command = {'jsonrpc': '2.0', 'id': 1, 'method': 'Settings.getSettings', 'params': {'filter': {'section': 'system', 'category': 'logging'}}}
    js_data = kodi.execute_jsonrpc(command)
    if 'result' in js_data and 'settings' in js_data['result']:
        for item in js_data['result']['settings']:
            if item['id'] == 'debug.showloginfo':
                return item['value']

    return False
