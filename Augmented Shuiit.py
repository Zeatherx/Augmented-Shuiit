import os
os.environ['KIVY_IMAGE'] = 'pil'
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.config import Config
from kivy.core.image import Image
from kivy.uix.slider import Slider
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.animation import Animation
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
from kivy.graphics.texture import Texture
from multiprocessing import freeze_support
import random
import cv2
import numpy as np
import math

def resource_path(relative_path):
    """Get absolute path to resource, from this .py file's directory"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

freeze_support()
hs = 0
tombolsb = "start"
bgmset = "belum"
battlestatus = "off"
camerainit = "belum"
Config.set('graphics','resizable','0')
bgm = SoundLoader.load("Data/BGM.wav")
Window.size = (350, 690)

screen_helper = """
ScreenManager:
    MenuScreen:
    PlayScreen:
    SettingsScreen:

<MenuScreen>:
    name: 'menu'
    Widget:
        canvas:
            Color:
                rgba: 247/255, 196/255, 170/255, 1
            Rectangle:
                size: self.size
                pos: self.pos
    Image:
        source : 'Data/rpslogo.png'
        size: self.texture_size
        pos_hint: {'center_x':0.5,'center_y':0.75}
    MDIconButton:
        pos_hint: {'center_x':0.5,'center_y':0.48}
        on_press: root.manager.current = 'play'
        user_font_size: 100
        icon: 'Data/playlogo.png'
        icon_size: "100sp"
    MDIconButton:
        pos_hint: {'center_x':0.5,'center_y':0.33}
        on_press: root.manager.current = 'settings'
        icon: 'Data/settingslogo.png'
        user_font_size: 100
        icon_size: "100sp"
    MDIconButton:
        pos_hint: {'center_x':0.5,'center_y':0.18}
        on_press: quit()
        user_font_size: 100
        icon : 'Data/exitlogo.png'
        icon_size: "100sp"
    
<PlayScreen>:
    name: 'play'
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Data/shuiitplaymenubg.jpg'
    MDIconButton:
        id: startbutton
        pos_hint: {'center_x':0.275,'center_y':0.16}
        on_press: root.start(self)
        user_font_size: 62
        disabled : False
        icon : "Data/playlogo.png"
        icon_size : "80sp"
    MDIconButton:
        pos_hint: {'center_x':0.275,'center_y':0.06}
        on_press: root.manager.current = 'menu'
        user_font_size: 62
        icon:'Data/backlogo.png'
        icon_size : "80sp"
    Label:
        id: countdown_label
        text: "-"
        pos_hint: {'center_x':0.82,'center_y':0.590}
        font_size: sp(25)
        bold: True
    Label:
        id: choice_label
        text: "-"
        pos_hint: {'center_x':0.65,'center_y':0.15}
        font_size: sp(23)
        bold: True
    Label:
        id: result_label
        text: "-"
        pos_hint: {'center_x':0.65,'center_y':0.06}
        font_size: sp(23)
        bold: True
    Image:
        id: imagenpc
        source: 'Data/shuiittranspa1.png'
        size: self.texture_size
        pos_hint: {'center_x':0.5,'center_y':0.378}    
    Image:
        id: imagecamera
        source: 'Data/cameralogo.png'
        size_hint: None,None
        height:200
        width:320
        pos_hint: {'center_x':0.5,'center_y':0.789}    

<SettingsScreen>:
    name: 'settings'
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Data/shuiitcreditandsettingsbg.jpg'
    MDIconButton:
        pos_hint: {'center_x':0.5,'center_y':0.09}
        on_press: root.manager.current = 'menu'
        user_font_size: 80
        icon: 'Data/backlogo.png'
        icon_size: "110sp"
    MDSlider:
        id: vslider
        min: 0
        max: 100
        step: 1
        value: 25
        on_value: root.volumes(self)
        orientation: 'horizontal'
        pos_hint: {'center_x':0.5,'center_y':0.76}
    Label:
        text: 'Volume : '
        font_size: sp(23)
        pos_hint: {'center_x':0.5,'center_y':0.81}
    Label:
        id: highscore_label
        text: 'High Score : -'
        font_size: sp(23)
        pos_hint: {'center_x':0.5,'center_y':0.70}
"""

class MenuScreen(Screen):
    def on_enter(*args):
        global bgmset
        if bgmset == "belum":
            global bgm
            bgm.play() 
            bgm.loop = True
            bgm.volume = 0.25
            bgmset = "udh"
        else:
            pass     
    
class PlayScreen(Screen):
    def on_pre_enter(self, *args):
        self.reset()
        self.camera()
    
    def reset(self):
        global tombolsb
        tombolsb = "start"
        self.ids.imagenpc.source = "Data/shuiittranspa1.png"
        self.ids.countdown_label.text = "-"
        self.ids.countdown_label.font_size = "25"
        self.ids.result_label.text = "-"
        self.ids.choice_label.text = "-"
        self.ids.startbutton.icon = "Data/startlogo.png"
    def camera(self):
        global camerainit
        # try:
        if camerainit == "belum":
            print("Camera not found or not accessible.")
            camerainit = "udh"
            self.detector = HandDetector(maxHands=1)
            kmodel = resource_path("Data\keras_model.h5")
            klabel = resource_path("Data\labels.txt")
            self.classifier = Classifier(kmodel, klabel)
            self.offset = 20
            self.imgSize = 300
            self.labels = ["Scissor","Rock","Paper"]
            self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            Clock.schedule_interval(self.load_video, 1.0/30.0)
        else:
            pass
        # except:
        #     print("Camera not found or not accessible.")
        #     pass


    def load_video(self,*args):
        global battlestatus
        try:
            ret, frame = self.capture.read() 
            imgOutput = frame.copy()
            hands, img = self.detector.findHands(frame)
            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']
        
                imgWhite = np.ones((self.imgSize, self.imgSize, 3), np.uint8) * 255
                imgCrop = img[y - self.offset:y + h + self.offset, x - self.offset:x + w + self.offset]
        
                imgCropShape = imgCrop.shape
        
                aspectRatio = h / w
        
                if aspectRatio > 1:
                    k = self.imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, self.imgSize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((self.imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                    prediction, index = self.classifier.getPrediction(imgWhite, draw=False)
                else:
                    k = self.imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (self.imgSize, hCal))
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((self.imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize
                    prediction, index = self.classifier.getPrediction(imgWhite, draw=False)

                cv2.putText(imgOutput, self.labels[index], (x -19, y -35), cv2.FONT_HERSHEY_PLAIN, 1.8, (255, 255, 255), 2)
                cv2.rectangle(imgOutput, (x-self.offset, y-self.offset),
                (x + w+self.offset, y + h+self.offset), (0, 0, 0), 4)
        except:
            pass
        try:
            imgOutput = frame
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer,colorfmt='bgr',bufferfmt='ubyte')
            self.ids.imagecamera.texture = texture
            if battlestatus == "off":
                self.ids.choice_label.text = f"{self.labels[index]}"
            else:
                pass
        except:
            pass

    def start(self,widget, *args):
        global tombolsb
        self.ids.imagenpc.source = "Data/shuiittranspa1.png"
        self.ids.startbutton.icon = "Data/battlelogo.png"
        if tombolsb == "battle":
            if self.ids.choice_label.text == "-":
                self.ids.countdown_label.text = "          Plz Show\n          Your Hand"
            else:
                self.ids.startbutton.disabled = True
                
                def animateloadnpc(dt):
                    self.ids.imagenpc.source = "Data/rpshandlogo.zip"
                    
                def countdown(dt):
                    def countdownone(dt):
                        self.ids.countdown_label.font_size = "25"
                        self.ids.countdown_label.text = "3"

                    def countdowntwo(dt):
                        self.ids.countdown_label.text = "2"

                    def countdownthree(dt):
                        global battlestatus
                        battlestatus = "on"
                        self.ids.countdown_label.text = "1"

                    def countdownfour(dt):
                        global hs 
                        npcchoice = random.randint(1, 3)
                        if npcchoice == 1:
                            npcimage = "Data/rocklogo.png"
                        elif npcchoice == 2:
                            npcimage = "Data/paperlogo.png"
                        else:
                           npcimage = "Data/scissorslogo.png"
                        result = "-"
                        self.ids.countdown_label.text = "    GO!!!"
                        self.ids.imagenpc.source = str(npcimage)
                        playerchoice = self.ids.choice_label.text
                        compchoice = npcchoice
                        if playerchoice == "Rock":
                            playerchoice = 1
                        elif playerchoice == "Paper":
                            playerchoice = 2
                        elif playerchoice == "Scissor":
                            playerchoice = 3
                        if playerchoice == compchoice:
                            result = "Tiee"
                            hs = 0
                        elif(playerchoice == 1 and compchoice == 2) :
                            result = "NPC WIN"
                            hs = 0
                        elif(playerchoice == 2 and compchoice ==1 ):
                            result = "Player WIN"
                            hs += 1
                        elif(playerchoice == 1 and compchoice == 3):
                            result = "Player WIN"
                            hs += 1
                        elif(playerchoice == 3 and compchoice == 1):
                            result = "NPC WIN"
                            hs = 0
                        elif(playerchoice == 3 and compchoice == 2):
                            result = "Player WIN"
                            hs += 1
                        elif(playerchoice == 2 and compchoice == 3):
                            result = "NPC WIN"
                            hs = 0
                        else:
                            result = "Error"
                        self.ids.result_label.text = result
                        dataread = open("Data/datahs.txt", "r")
                        highscore =  dataread.readline(1)
                        dataread.close()
                        highscores = int(highscore)
                        if hs > highscores:
                            datawrite = open("Data/datahs.txt", "w")
                            datawrite.write(f"{hs}")
                            datawrite.close()       
                    def countdownfive(dt):
                        global battlestatus
                        self.ids.startbutton.disabled = False
                        battlestatus = "off"
                        
                    Clock.schedule_once(countdownone, 0)
                    Clock.schedule_once(countdowntwo, 1)
                    Clock.schedule_once(countdownthree, 2)
                    Clock.schedule_once(countdownfour, 3)
                    Clock.schedule_once(countdownfive, 4)

                
                Clock.schedule_once(countdown, 0)
                Clock.schedule_once(animateloadnpc, 0)
                self.ids.startbutton.icon = "Data/startlogo.png"
                tombolsb = "start"
        else:
            self.ids.countdown_label.font_size = "15"
            self.ids.countdown_label.text = "          Plz Show\n          Your Hand"
            tombolsb = "battle"       

class SettingsScreen(Screen):
    def on_pre_enter(self, *args):
        filepath = "Data/datahs.txt"
        if not os.path.exists("Data"):
            os.makedirs("Data")
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                f.write("0")

        with open(filepath, "r") as data:
            highscore = data.readline().strip()
        self.ids.highscore_label.text = f"High Score : {highscore}"

    
    def volumes(self, *args):
        global bgm
        vsliderv = self.ids.vslider.value
        vslidervol = vsliderv/100
        bgm.volume = vslidervol

sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(PlayScreen(name='play'))
sm.add_widget(SettingsScreen(name='settings'))

class ShuittApp(MDApp):

    def build(self):
        self.icon = "Data/shuiitapplogo.jpg"
        screen = Builder.load_string(screen_helper)
        return screen

ShuittApp().run()
