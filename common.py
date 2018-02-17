import os
import urllib2
import xbmc
import xbmcaddon
import xbmcgui

from libs import kodi

addon_id = kodi.addon_id

settings = xbmcaddon.Addon(id=addon_id)


## ################################################## ##
## ################################################## ##
def gAI(t):
    try:
        return settings.getAddonInfo(t)
    except:
        return ""


## ################################################## ##
## ################################################## ##
icon = gAI('icon')
fanart = gAI('fanart')
addon_name = gAI('name')
addon_path = gAI('path')
addon_type = gAI('type')
addon_author = gAI('author')
addon_version = gAI('version')
addon_stars = gAI('stars')
addon_changelog = gAI('changelog')
disclaimer = gAI('disclaimer')
description = gAI('description')
summary = gAI('summary')
artPath = xbmc.translatePath(os.path.join(addon_path, 'noteart'))


## ################################################## ##
## ################################################## ##
def note(title='', msg='', delay=5000, image=''):
    if len(image) == 0: image += icon
    xbmc.executebuiltin('XBMC.Notification("%s","%s",%d,"%s")' % (title, msg, delay, image))


def SettingG(setting):
    try:
        return settings.getSetting(setting)
    except:
        return ""


def SettingS(setting, value):
    settings.setSetting(id=setting, value=value)


def deb(s, t):  ### for Writing Debug Data to log file ###
    # if (_debugging==True): 
    print s + ':  ' + t


def debob(t):  ### for Writing Debug Object to log file ###
    # if (_debugging==True): 
    print t


def nolines(t):
    it = t.splitlines()
    t = ''
    for L in it: t = t + L
    t = ((t.replace("\r", "")).replace("\n", ""))
    return t


def art(f, fe=''):
    fe1 = '.png'
    fe2 = '.jpg'
    fe3 = '.gif'
    fe4 = '.wav'
    fe5 = '.txt'
    if fe1 in f:
        f = f.replace(fe1, ''); fe = fe1
    elif fe2 in f:
        f = f.replace(fe2, ''); fe = fe2
    elif fe3 in f:
        f = f.replace(fe3, ''); fe = fe3
    elif fe4 in f:
        f = f.replace(fe4, ''); fe = fe4
    elif fe5 in f:
        f = f.replace(fe5, ''); fe = fe5
    return xbmc.translatePath(os.path.join(artPath, f + fe))


def artp(f, fe='.png'): return art(f, fe)


def artj(f, fe='.jpg'): return art(f, fe)


def addonPath(f, fe=''): return xbmc.translatePath(os.path.join(addon_path, f + fe))


def cFL(t, c='tan'): return '[COLOR ' + c + ']' + t + '[/COLOR]'  ### For Coloring Text ###


def popYN(title='', line1='', line2='', line3='', n='', y=''):
    diag = xbmcgui.Dialog()
    r = diag.yesno(title, line1, line2, line3, n, y)
    if r:
        return r
    else:
        return False


# del diag
def popOK(msg="", title="", line2="", line3=""):
    dialog = xbmcgui.Dialog()
    # ok=dialog.ok(title, msg, line2, line3)
    dialog.ok(title, msg, line2, line3)


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows U Windows NT 5.1 en-GB rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link


def File_Save(path, data):
    file = open(path, 'w')
    file.write(data)
    file.close()


def File_Open(path):
    if os.path.isfile(path):  ## File found.
        file = open(path, 'r')
        contents = file.read()
        file.close()
        return contents
    else:
        return ''  ## File not found.


def tfalse(r, d=False):  ## Get True / False
    if (r.lower() == 'true') or (r.lower() == 't') or (r.lower() == 'y') or (r.lower() == '1') or (r.lower() == 'yes'):
        return True
    elif (r.lower() == 'false') or (r.lower() == 'f') or (r.lower() == 'n') or (r.lower() == '0') or (
        r.lower() == 'no'):
        return False
    else:
        return d


## ################################################## ##
ACTION_PREVIOUS_MENU = 10  ## ESC action
ACTION_NAV_BACK = 92  ## Backspace action
ACTION_MOVE_LEFT = 1  ## Left arrow key
ACTION_MOVE_RIGHT = 2  ## Right arrow key
ACTION_MOVE_UP = 3  ## Up arrow key
ACTION_MOVE_DOWN = 4  ## Down arrow key
ACTION_MOUSE_WHEEL_UP = 104  ## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN = 105  ## Mouse wheel down
ACTION_MOUSE_DRAG = 106  ## Mouse drag
ACTION_MOUSE_MOVE = 107  ## Mouse move
#
ACTION_SELECT_ITEM = 7  ## ?
ACTION_PARENT_DIR = 9  ## ?
ACTION_CONTEXT_MENU = 117  ## ?
ACTION_NEXT_ITEM = 14  ## ?
ACTION_BACKSPACE = 110  ## ?
## ################################################## ##
## ################################################## ##
OverlayBorder = artp('blank1')
OverlayBackground = artp('ContentPanel')
hubLogo = artp('tvaddons_logo')
# hubLogo=artp('logo_notice.png')
DefaultNoteImage = artp('blank1')
DefaultSplitter = "|||"
DefaultUrl = "http://indigo.tvaddons.co/notifications/news.txt"


class MyWindow(xbmcgui.WindowDialog):  # xbmcgui.Window): ##xbmcgui.Window

    scr = {}
    scr['L'] = 0
    scr['T'] = 0
    scr['W'] = 1280
    scr['H'] = 720

    def __init__(self, noteType='t', noteMessage='', noteImage='', L=140, T=110, W=1000, H=500, Font='font14', TxtColor='0xFF64d1ff'):
        super(MyWindow, self).__init__()
        if len(noteImage) == 0: noteImage = DefaultNoteImage
        if (noteType.lower() == 'text') or (noteType.lower() == 't'):
            noteType = 't'
        elif (noteType.lower() == 'image') or (noteType.lower() == 'i'):
            noteType = 'i'
        self.noteType = noteType
        self.noteMessage = noteMessage
        self.noteImage = noteImage
        self.Font = Font
        self.TxtColor = TxtColor
        ## ### ##
        self.background = OverlayBackground  # artp('black1')
        self.BG = xbmcgui.ControlImage(L, T, W, H, self.background, aspectRatio=0, colorDiffuse='0xFF3030FF')
        # self.OlayBrdr=xbmcgui.ControlImage(L,T,W,H,OverlayBorder,aspectRatio=0)
        # self.OlaySplash=xbmcgui.ControlImage(L,T,W,H,icon,aspectRatio=0)
        iLogoW = 300
        iLogoH = 68
        self.iLogo = xbmcgui.ControlImage((L + (W / 2)) - (iLogoW / 2), T + 10, iLogoW, iLogoH, hubLogo, aspectRatio=2)
        ## ### ##
        ###L2=L+110 T2=T+130 W2=W-(T2-T)-90 H2=H-(L2-L)-110 #L3=L2+5 T3=T2+5 W3=W2-18 H3=H2-10
        ##L2=L+87 T2=T+80 W2=W-(T2-T)-96 H2=H-(L2-L)-74 L3=L2+5 T3=T2+60 W3=W2-18 H3=H2-5-60
        # L2=L+67 T2=T+60 W2=W-(T2-T)-96 H2=H-(L2-L)-74
        L2 = 200
        T2 = 200
        W2 = 880
        H2 = 340
        L3 = L2 + 5
        T3 = T2 + 60
        W3 = W2 - 18
        H3 = H2 - 5 - 60
        self.ImgMessage = xbmcgui.ControlImage(L2, T2, W2, H2, self.noteImage, aspectRatio=0)
        self.TxtMessage = xbmcgui.ControlTextBox(L2 + 5, T2, W2 - 10, H2, font=self.Font, textColor=self.TxtColor)
        # self.TxtMessage=xbmcgui.ControlTextBox(L3,T3,W3,H3,font=self.Font,textColor=self.TxtColor)
        # print [self.background,OverlayBorder,self.noteImage]
        ## ### ##
        focus = artp('button-focus_lightblue')
        nofocus = artp('button-focus_grey')
        w1 = 120
        h1 = 35
        w2 = 160
        h2 = 35
        spacing1 = 20
        l2 = L + W - spacing1 - w2
        t2 = T + H - h2 - spacing1
        l1 = L + W - spacing1 - w2 - spacing1 - w1
        t1 = T + H - h1 - spacing1
        self.buttonDismiss = xbmcgui.ControlButton(l1, t1, w1, h1, "Dismiss", textColor="0xFF000000",
                                                   focusedColor="0xFF000000", alignment=2, focusTexture=focus,
                                                   noFocusTexture=nofocus)
        self.buttonRemindMe = xbmcgui.ControlButton(l2, t2, w2, h2, "Remind Later", textColor="0xFF000000",
                                                    focusedColor="0xFF000000", alignment=2, focusTexture=focus,
                                                    noFocusTexture=nofocus)
        # self.OlaySplash
        for z in [self.BG, self.ImgMessage, self.TxtMessage, self.iLogo, self.buttonRemindMe,
                  self.buttonDismiss]: self.addControl(z)
        # for z in [self.BG,self.ImgMessage,self.TxtMessage,self.OlayBrdr,self.buttonRemindMe,self.buttonDismiss]: self.addControl(z)
        # for z in [self.BG,self.OlayBrdr,self.ImgMessage,self.TxtMessage,self.buttonRemindMe,self.buttonDismiss]: self.addControl(z)
        # self.OlayBrdr.setAnimations([('WindowOpen','effect=fade delay=0 time=0 start=0 end=70')])
        # self.ImgMessage.setAnimations([('WindowOpen','effect=fade delay=0 time=0 start=0 end=70')])
        # self.OlaySplash.setAnimations([('WindowOpen','effect=fade delay=0 time=8000 start=100 end=0')])
        # self.OlaySplash.setAnimations([('WindowOpen','effect=slide delay=0 time=5000 start=-1800 end=1800')])
        # self.ImgMessage.setAnimations([('WindowOpen','effect=fade delay=2000 time=2000 start=0 end=100')])
        # for z in [self.BG,self.ImgMessage,self.TxtMessage,self.OlayBrdr,self.buttonRemindMe,self.buttonDismiss]:
        for z in [self.BG, self.ImgMessage, self.TxtMessage, self.iLogo, self.buttonRemindMe, self.buttonDismiss]:
            # z.setAnimations([('WindowOpen','effect=slide delay=0 time=5000 start=0,-1800 end=0'),('WindowClose','effect=slide delay=0 time=5000 start=0 end=0,-1800')])
            z.setAnimations([('WindowOpen', 'effect=fade delay=0 time=2000 start=0 end=100'),
                             ('WindowClose', 'effect=slide delay=0 time=2000 start=0 end=0,' + str(0 - (H + T + 10)))])
        ## ### ##
        self.buttonRemindMe.controlLeft(self.buttonDismiss)
        self.buttonRemindMe.controlRight(self.buttonDismiss)
        self.buttonDismiss.controlLeft(self.buttonRemindMe)
        self.buttonDismiss.controlRight(self.buttonRemindMe)
        ## ### ##
        self.TxtMessage.setText(self.noteMessage)
        self.setFocus(self.buttonRemindMe)

    def doRemindMeLater(self):
        try:
            SettingS("noteType", self.noteType)
            SettingS("noteImage", "")
            SettingS("noteMessage", "")
        except:
            pass
        ##CODE HERE##
        self.CloseWindow1st()

    def doDismiss(self):
        try:
            SettingS("noteType", self.noteType)
            SettingS("noteImage", self.noteImage)
            SettingS("noteMessage", self.noteMessage)
        except:
            pass
        ##CODE HERE##
        self.CloseWindow1st()

    def onAction(self, action):
        try:
            F = self.getFocus()
        except:
            F = False
        if action == ACTION_PREVIOUS_MENU:
            self.doRemindMeLater()
        elif action == ACTION_NAV_BACK:
            self.doRemindMeLater()
        elif action == ACTION_SELECT_ITEM:
            self.doDismiss()
        else:
            try:
                if not F == self.buttonRemindMe:
                    self.setFocus(self.buttonDismiss)
            except:
                pass

    def onControl(self, control):
        if control == self.buttonRemindMe:
            self.doRemindMeLater()
        elif control == self.buttonDismiss:
            self.doDismiss()
        else:
            try:
                self.setFocus(self.buttonRemindMe)
            except:
                pass

    # def onInit(self): pass
    # def onClick(self,control): pass
    # def onControl(self,control): pass
    # def onFocus(self,control): pass
    # def onAction(self,action): pass
    def CloseWindow1st(self):
        ##CODE HERE##
        self.close()


## ################################################## ##
## ################################################## ##
DefaultReturn = ["", ""]


def FetchNews():
    NewImage = ""
    NewMessage = ""
    info_location = addonPath("test.txt")
    info_location3 = addonPath("url.txt")
    info_location2 = DefaultUrl
    if os.path.isfile(info_location) == True:
        try:
            html = File_Open(info_location)
        # kodi.log(info_location)
        except:
            return DefaultReturn
    elif os.path.isfile(info_location3) == True:
        try:
            info_location3B = File_Open(info_location3).strip()
            if info_location3B > 0:
                html = OPEN_URL(info_location3B)
            # kodi.log(info_location3B)
            else:
                return DefaultReturn
        except:
            return DefaultReturn
    else:
        try:
            html = OPEN_URL(info_location2)
        # kodi.log(info_location2)
        except:
            return DefaultReturn
    if DefaultSplitter in html:
        NewImage = html.split(DefaultSplitter)[0].strip()
        NewMessage = html.split(DefaultSplitter)[1].strip()
    return NewImage, NewMessage


def CheckNews(TypeOfMessage, NewImage, NewMessage, DoFromService=True):
    if (len(NewImage) > 0) or (len(NewMessage) > 0):
        debob(
            ["notifications-on-startup", SettingG("notifications-on-startup"), "DoFromService", DoFromService])
        if (SettingG("notifications-on-startup") == 'false') or (DoFromService == False):
            if NewImage.lower() == "none":
                NewImage = ""
            if NewMessage.lower() == "none":
                NewMessage = ""
            OldnoteType = SettingG("noteType")
            OldnoteImage = SettingG("noteImage")
            OldnoteMessage = SettingG("noteMessage")
            OldnoteImage = OldnoteImage.replace(DefaultNoteImage, '')
            if OldnoteImage.lower() == "none":
                OldnoteImage = ""
            if OldnoteMessage.lower() == "none":
                OldnoteMessage = ""
            # print ['OLD',OldnoteType,OldnoteImage,OldnoteMessage]
            # print ['NEW',TypeOfMessage,NewImage,NewMessage]
            if (not OldnoteImage == NewImage) or (not OldnoteMessage == NewMessage):
                TempWindow = MyWindow(noteType=TypeOfMessage, noteMessage=NewMessage, noteImage=NewImage)
                TempWindow.doModal()
                del TempWindow
            elif DoFromService == True:
                return
            else:
                TempWindow = MyWindow(noteType=TypeOfMessage, noteMessage=NewMessage, noteImage=NewImage)
                TempWindow.doModal()
                del TempWindow

## ################################################## ##
## ################################################## ##
