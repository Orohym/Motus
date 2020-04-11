import kivy
from getpass import getpass
import time
import numpy as np

kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

class CapitalInput(TextInput): # Automatic Input in upper case
        def insert_text(self, substring, from_undo=False):
            s = substring.upper()
            return super(CapitalInput, self).insert_text(s, from_undo=from_undo)

def occurence(mot):
    motDict = {}
    for i in range(len(mot)):
        if mot[i] not in motDict.keys():
            motDict[mot[i]] = 1
        else:
            motDict[mot[i]] = motDict[mot[i]] + 1
    return(motDict)

class boxHorizontal(BoxLayout):
    def __init__(self, motADeviner):
        super().__init__()
        self.orientation = "vertical"
        self.spacing = 1
        self.motADeviner = motADeviner
        self.iterateur = 0
        self.maxIteration = 6
        self.correct = []
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
            for j in range(len(motADeviner)):
                if (i == 0 and j == 0 )or (i == 0 and j == (len(motADeviner)-1)):
                    self.listbox[i].listbtn = self.listbox[i].listbtn + [Button(text = motADeviner[j],
                    font_size = '100sp', background_color = blue)]
                elif i == 0:
                    self.listbox[i].listbtn = self.listbox[i].listbtn + [Button(text = ".",font_size = '100sp', background_color = blue)]
                else:
                    self.listbox[i].listbtn = self.listbox[i].listbtn + [Button(text = "",font_size = '100sp', background_color = blue)]
                self.listbox[i].add_widget(self.listbox[i].listbtn[j])
            self.add_widget(self.listbox[i])

    def action(self, instance):
        red = [3*1,0,2*0.3,1]
        yellow = [4*1,2.5*1,2*0.2,1]
        blue =  [0,0,222,0.81]
        colorId = [red, yellow, blue]
        # verifie si on a pas utilisé toutes les chances
        if self.iterateur < self.maxIteration-1:
            # test si les mots sont les mêmes
            if self.textbox.txt.text == self.motADeviner:
                #on met tout les lettres en bleu
                for k in range(len(self.textbox.txt.text)):
                    self.listbox[self.iterateur].listbtn[k].text = self.textbox.txt.text[k]
                    self.listbox[self.iterateur].listbtn[k].background_color = blue
                # on met les lettre en rouge car juste
                for k in range(len(self.motADeviner)):
                    self.listbox[self.iterateur].listbtn[k].text = self.motADeviner[k]
                    self.listbox[self.iterateur].listbtn[k].background_color = red
                    #Clock.schedule_interval(self.Update, 1/60.)#time.sleep(0.6)
                # affichage popup gagné
                content = BoxLayout(orientation = "vertical",spacing = 10)
                rep = Label(text = "Gagné ! \n Le mot était "+self.motADeviner, font_size = '50sp' )#, size_hint(1, .1))
                bouton = Button(text='Ok', on_press = lambda *args: App.get_running_app().stop())
                content.add_widget(rep)
                content.add_widget(bouton)
                size_x = 0.7
                size_y = 0.7
                pos_x = abs(0.5 - size_x / 2)
                pos_y = abs(0.5 - size_y / 2)
                popup = Popup(auto_dismiss=False, content=content, title = "Winner ! ", size_hint=(size_x, size_y),
                      pos_hint={'y': pos_y, 'x': pos_x} )#size_hint=(None, None), size=(400, 400) )
                popup.open()

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
                for k in range(len(self.textbox.txt.text)):
                    self.listbox[self.iterateur].listbtn[k].text = self.textbox.txt.text[k]
                    self.listbox[self.iterateur].listbtn[k].background_color = colorId[couleur[k]]
                    #Clock.schedule_interval(self.Update, 1/60.)#time.sleep(0.6)
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

            else : # Si pas la même longueur, grille une chance
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
                for k in range(len(self.motADeviner)):
                    self.listbox[self.iterateur].listbtn[k].text = self.motADeviner[k]
                    self.listbox[self.iterateur].listbtn[k].background_color = red
                    #time.sleep(0.6)
                content = BoxLayout(orientation = "vertical",spacing = 10)
                rep = Label(text = "Gagné ! \n Le mot était "+self.motADeviner, font_size = '50sp' )#, size_hint(1, .1))
                bouton = Button(text='Ok', on_press = lambda *args: App.get_running_app().stop())
                content.add_widget(rep)
                content.add_widget(bouton)
                size_x = 0.7
                size_y = 0.7
                pos_x = abs(0.5 - size_x / 2)
                pos_y = abs(0.5 - size_y / 2)
                popup = Popup(auto_dismiss=False, content=content, title = "Winner ! ", size_hint=(size_x, size_y),
                      pos_hint={'y': pos_y, 'x': pos_x} )#size_hint=(None, None), size=(400, 400) )
                popup.open()
        # perdu
        else:
            content = BoxLayout(orientation = "vertical",spacing = 10)
            rep = Label(text = "Perdu ! \n Le mot était "+self.motADeviner, font_size = '50sp' )#, size_hint(1, .1))
            #boutonNew = Button(text='Oui', on_press = self.nouvellePartie)
            boutonExit = Button(text='Ok', on_press = lambda *args: App.get_running_app().stop())
            content.add_widget(rep)
            #content.add_widget(boutonNew)
            content.add_widget(boutonExit)
            size_x = 0.7
            size_y = 0.7
            pos_x = abs(0.5 - size_x / 2)
            pos_y = abs(0.5 - size_y / 2)
            self.popup = Popup(auto_dismiss=False, content=content, title = "Looseeeeeer", size_hint=(size_x, size_y),
                  pos_hint={'y': pos_y, 'x': pos_x} )
            self.popup.open()

        self.textbox.txt.text =  ""
        self.iterateur = self.iterateur + 1
        Clock.schedule_once(self._refocus_ti)

    def _refocus_ti(self,*args):
       self.textbox.txt.focus = True


class Motus(App):
    def build(self):
        mot = getpass().upper()
        self.box = BoxLayout(orientation='vertical',spacing = 10)
        box1 = boxHorizontal(motADeviner=mot)
        self.box.add_widget(box1)
        return self.box

Motus().run()
