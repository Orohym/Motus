'''
Created by Antoine Perney on 12/04/2020.
Copyright © 2020 Antoine Perney. All rights reserved.
'''

import kivy
from getpass import getpass
import time
import numpy as np
import random
import sys
import os
from functools import partial

kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock, ClockBase
from kivy.core.audio import SoundLoader



path = sys.argv[0]

absolute_path = os.path.abspath(path)
repository = os.path.dirname(absolute_path)

sounds = [SoundLoader.load(repository +'/audio/lettre.mp3'), SoundLoader.load(repository +'/audio/lettrejaune.mp3'), SoundLoader.load(repository +'/audio/lettrebleu.mp3')]
winning_sound = SoundLoader.load(repository + '/audio/win.mp3')
lose_sound = SoundLoader.load(repository + '/audio/motusperdu.mp3')
file = open(repository + '/data/liste.txt', 'r', encoding = "utf-8")
lines = file.readlines()
list_mot = []
for line in lines:
    list_mot.append(line[:-1])

class CapitalInput(TextInput): # Automatic Input in upper case
        def insert_text(self, substring, from_undo=False):
            s = substring.upper()
            return super(CapitalInput, self).insert_text(s, from_undo=from_undo)

class boxHorizontal(BoxLayout):
    def __init__(self):
        super().__init__()
        rand = random.randrange(len(list_mot))
        self.orientation = "vertical"
        self.spacing = 1
        self.motADeviner = list_mot[rand]
        self.iterateur = 0
        self.maxIteration = 6
        self.correct = []
        self.idcolor = 0
        self.textbox =  BoxLayout(padding = 1, orientation = "horizontal")
        self.textbox.txt = CapitalInput(hint_text = 'Saisie du mot', font_size = '50sp', multiline = False, size_hint = (1,1))
        Clock.schedule_once(self._refocus_ti)
        self.textbox.txt.bind(on_text_validate = self.action)
        self.textbox.add_widget(self.textbox.txt)
        self.add_widget(self.textbox)
        blue =  [0,0,222,0.81]
        self.listbox = [] # creation of list to list 6 boxlayout each boxlayout will contain the word
        for i in range(self.maxIteration):
            self.listbox = self.listbox + [BoxLayout(padding = 1, orientation = "horizontal")]
            self.listbox[i].listbtn = []
            for j in range(len(self.motADeviner)):
                if (i == 0 and j == 0 )or (i == 0 and j == (len(self.motADeviner)-1)):
                    self.listbox[i].listbtn = self.listbox[i].listbtn + [Button(text = self.motADeviner[j],
                    font_size = '100sp', background_color = blue)]
                elif i == 0:
                    self.listbox[i].listbtn = self.listbox[i].listbtn + [Button(text = ".",font_size = '100sp', background_color = blue)]
                else:
                    self.listbox[i].listbtn = self.listbox[i].listbtn + [Button(text = "",font_size = '100sp', background_color = blue)]
                self.listbox[i].add_widget(self.listbox[i].listbtn[j])
            self.add_widget(self.listbox[i])


    def action(self, instance):
        #sounds = SoundLoader.load('/audio/lettre_ok.wav')
        red = [3*1,0,2*0.3,1]
        yellow = [4*1,2.5*1,2*0.2,1]
        blue =  [0,0,222,0.81]
        colorId = [red, yellow, blue]
        self.colorid = colorId
        # verifie si on a pas utilisé toutes les chances
        if self.iterateur < self.maxIteration-1:
            # test si les mots sont les mêmes
            if self.textbox.txt.text == self.motADeviner:
                #on met tout les lettres en bleu
                for k in range(len(self.textbox.txt.text)):
                    self.listbox[self.iterateur].listbtn[k].text = self.textbox.txt.text[k]
                    self.listbox[self.iterateur].listbtn[k].background_color = blue
                delay_time = 0.21
                add_delay = 0
                remove_delay = 0
                for k in range(len(self.textbox.txt.text)):
                    self.listbox[self.iterateur].listbtn[k].idcolor = 0
                for w in self.listbox[self.iterateur].listbtn:
                    remove_delay += delay_time
                    Clock.schedule_once(partial(self.colorLetter,w), add_delay )
                    add_delay += delay_time
                # affichage popup gagné
                Clock.schedule_once(self.popupwin, add_delay+0.2)

            # test si les mots on la même longueur
            elif len(self.textbox.txt.text) == len(self.motADeviner):
                # on met toutes les lettres en bleu
                for k in range(len(self.textbox.txt.text)):
                    self.listbox[self.iterateur].listbtn[k].text = self.textbox.txt.text[k]
                    self.listbox[self.iterateur].listbtn[k].background_color = blue
                egalite = np.array(list(self.textbox.txt.text)) ==  np.array(list(self.motADeviner))
                couleur = [i for i in range(len(self.motADeviner))]
                posFaux = []
                devin = []
                for i in range(len(egalite)):
                    if egalite[i] == True:
                        couleur[i] = 0 #red = 0
                        if i not in self.correct:
                            self.correct.append(i)
                    else:
                        posFaux = posFaux + [i]
                        devin = devin + [self.motADeviner[i]]
                for j in posFaux:
                    if self.textbox.txt.text[j] in devin:
                        couleur[j] = 1 # yellow = 1
                        iter = 0
                        while self.textbox.txt.text[j] != devin[iter]:
                            iter=iter+1
                        del devin[iter]
                    else:
                        couleur[j] = 2 # blue =2
                delay_time = 0.21
                add_delay = 0
                remove_delay = 0
                for k in range(len(self.textbox.txt.text)):
                    self.listbox[self.iterateur].listbtn[k].idcolor = couleur[k]
                for w in self.listbox[self.iterateur].listbtn:
                    remove_delay += delay_time
                    Clock.schedule_once( partial(self.colorLetter,w), add_delay )
                    add_delay += delay_time
                Clock.schedule_once(self.newline, add_delay+0.2)

            else : # Si pas la même longueur, grille une chance
                lose_sound.play()
                for k in range(len(self.motADeviner)):
                    if k in self.correct:
                        self.listbox[self.iterateur+1].listbtn[k].text = self.motADeviner[k]
                        self.listbox[self.iterateur+1].listbtn[k].background_color = blue
                    else:
                        self.listbox[self.iterateur+1].listbtn[k].text = "."
                        self.listbox[self.iterateur+1].listbtn[k].background_color = blue
                self.listbox[self.iterateur+1].listbtn[0].text = self.motADeviner[0]
                self.listbox[self.iterateur+1].listbtn[0].background_color = blue
                self.listbox[self.iterateur+1].listbtn[-1].text = self.motADeviner[-1]
                self.listbox[self.iterateur+1].listbtn[-1].background_color = blue

        # encore une chance de gagné
        elif self.iterateur == (self.maxIteration-1) and self.textbox.txt.text == self.motADeviner:
                # Si on a le bon mot popup Gagné !
                for k in range(len(self.textbox.txt.text)):
                    self.listbox[self.iterateur].listbtn[k].text = self.textbox.txt.text[k]
                    self.listbox[self.iterateur].listbtn[k].background_color = blue
                for k in range(len(self.textbox.txt.text)):
                    self.listbox[self.iterateur].listbtn[k].idcolor = 0
                delay_time = 0.21
                add_delay = 0
                remove_delay = 0
                for w in self.listbox[self.iterateur].listbtn:
                    remove_delay += delay_time
                    Clock.schedule_once( partial(self.colorLetter,w), add_delay )
                    add_delay += delay_time
                winning_sound.play()
                # affichage popup gagné
                Clock.schedule_once(self.popupwin, add_delay+0.2)
        # perdu
        else:
            lose_sound.play()
            size_x = 0.7
            size_y = 0.7
            pos_x = abs(0.5 - size_x / 2)
            pos_y = abs(0.5 - size_y / 2)
            self.popup = Popup(auto_dismiss=False, title = "Fin de partie", size_hint=(size_x, size_y),
                  pos_hint={'y': pos_y, 'x': pos_x} )
            content = BoxLayout(orientation = "vertical",spacing = 10)
            rep = Label(text = "Perdu ! \nLe mot était "+self.motADeviner, font_size = '40sp' )
            bouton_new = Button(text='Nouvelle partie', on_press = self.reset)
            bouton_exit = Button(text='Quitter', on_press = lambda *args: App.get_running_app().stop())
            content.add_widget(rep)
            content.add_widget(bouton_new)
            content.add_widget(bouton_exit)
            self.popup.content = content
            self.popup.open()

        self.textbox.txt.text =  ""
        self.iterateur = self.iterateur + 1
        Clock.schedule_once(self._refocus_ti)

    def reset(self,intance):
        self.popup.dismiss()
        self.remove_widget(self.textbox)
        rand = random.randrange(len(list_mot))
        self.orientation = "vertical"
        self.spacing = 1
        self.motADeviner = list_mot[rand]
        self.iterateur = 0
        self.maxIteration = 6
        self.correct = []
        self.textbox =  BoxLayout(padding = 1, orientation = "horizontal")
        self.textbox.txt = CapitalInput(hint_text = 'Saisie du mot', font_size = '50sp', multiline = False, size_hint = (1,1))
        Clock.schedule_once(self._refocus_ti)
        self.textbox.txt.bind(on_text_validate = self.action)
        self.textbox.add_widget(self.textbox.txt)
        self.add_widget(self.textbox)
        for i in range(self.maxIteration):
            self.remove_widget(self.listbox[i])
        blue =  [0,0,222,0.81]
        self.listbox = [] # creation of list to list 6 boxlayout each boxlayout will contain the word
        for i in range(self.maxIteration):
            self.listbox = self.listbox + [BoxLayout(padding = 1, orientation = "horizontal")]
            self.listbox[i].listbtn = []
            for j in range(len(self.motADeviner)):
                if (i == 0 and j == 0 )or (i == 0 and j == (len(self.motADeviner)-1)):
                    self.listbox[i].listbtn = self.listbox[i].listbtn + [Button(text = self.motADeviner[j],
                    font_size = '100sp', background_color = blue)]
                elif i == 0:
                    self.listbox[i].listbtn = self.listbox[i].listbtn + [Button(text = ".",font_size = '100sp', background_color = blue)]
                else:
                    self.listbox[i].listbtn = self.listbox[i].listbtn + [Button(text = "",font_size = '100sp', background_color = blue)]
                self.listbox[i].add_widget(self.listbox[i].listbtn[j])
            self.add_widget(self.listbox[i])

    def _refocus_ti(self,*args):
          self.textbox.txt.focus = True

    def colorLetter(self, widget,dt):
        widget.background_color = self.colorid[widget.idcolor]
        sounds[widget.idcolor].play()

    def newline(self, instance):
        blue = [0,0,222,0.81]
        for k in range(len(self.motADeviner)):
            if k in self.correct:
                self.listbox[self.iterateur].listbtn[k].text = self.motADeviner[k]
                self.listbox[self.iterateur].listbtn[k].background_color = blue
            else:
                self.listbox[self.iterateur].listbtn[k].text = "."
                self.listbox[self.iterateur].listbtn[k].background_color = blue
        self.listbox[self.iterateur].listbtn[0].text = self.motADeviner[0]
        self.listbox[self.iterateur].listbtn[0].background_color = blue
        self.listbox[self.iterateur].listbtn[-1].text = self.motADeviner[-1]
        self.listbox[self.iterateur].listbtn[-1].background_color = blue

    def popupwin(self, instance):
        winning_sound.play()
        size_x = 0.7
        size_y = 0.7
        pos_x = abs(0.5 - size_x / 2)
        pos_y = abs(0.5 - size_y / 2)
        self.popup = Popup(auto_dismiss=False, title = "Fin de partie", size_hint=(size_x, size_y),
              pos_hint={'y': pos_y, 'x': pos_x} )
        content = BoxLayout(orientation = "vertical",spacing = 10)
        rep = Label(text = "Gagné ! \nLe mot était "+self.motADeviner, font_size = '40sp' )
        bouton_new = Button(text='Nouvelle partie', on_press = self.reset)
        bouton_exit = Button(text='Quitter', on_press = lambda *args: App.get_running_app().stop())
        content.add_widget(rep)
        content.add_widget(bouton_new)
        content.add_widget(bouton_exit)
        self.popup.content = content
        self.popup.open()


class Motus(App):
    def build(self):
        self.box = BoxLayout(orientation='vertical',spacing = 10)
        box1 = boxHorizontal()
        self.box.add_widget(box1)
        return self.box

Motus().run()
