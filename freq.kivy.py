# -*- coding: utf-8 -*-
import threading
import mmap
import struct as st
from math import sin, cos, radians
from random import randint
import pyaudio as pa
import os


from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView

from kivy.clock import Clock, mainthread
from kivy.lang import Builder


#class MainFrame(BoxLayout):
    #frcon = ObjectProperty(None)
    #pass


class MainApp(App):
    #stop = threading.Event()
    sample_freq = 44100
    duration = 1.0
    freqs = []

    #frcon = ObjectProperty(None)

    #def build(self):
        #self.mainframe = MainFrame()
        #return self.mainframe
    #    return MainFrame()


    def add_freq(self,w):
        f = Builder.load_file('freqwidget.kv')
        self.freqs.append(f)
        w.add_widget(f)

    def rm_freq(self,w):
        self.freqs.remove(w)
        w.parent.remove_widget(w)

    def openFileDialog(self, w):
        f = Builder.load_file('filedialog.kv')
        w.add_widget(f)


    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            for f in self.freqs:
                stream.write(str(f.freq) +' '+ str(f.volume) + '\n')

    def load(self, path, filename):
        box = self.root.ids.frcon
        box.clear_widgets()
        #with open(os.path.join(path, filename[0])) as stream:
            #while True:
        file = open(os.path.join(path, filename[0]))
        for data in file.readlines():
                #data = stream.readline().split()
                f = Builder.load_file('freqwidget.kv')
                f.freq = int(data[0])
                f.volume = float(data[1])
                self.freqs.append(f)
                box.add_widget(f)


    def start_play(self, btn):
        self.play()



    def play(self):
        if not self.freqs: return
        fv = [(f.freq, f.volume) for f in self.freqs]
        sf = self.sample_freq
        n = len(self.freqs)
        data = []

        for i in range(int( self.duration * 44100 )):
            x = 0
            for f in fv:
                #x += int(sin(radians(i * (f.freq) / (self.sample_freq / 360))) * 32767)
                x += int(sin(radians(i * f[0] / (sf / 360))) * 32767 * f[1])
            x = int(x / n)
            data.append( st.pack("<h", x) )
            #i = 0 if i == 359 else i + 1
            # x = randint(0,65535) # white noise


        s = pa.PyAudio().open(format=pa.paInt16,
                              channels=1,
                              rate=self.sample_freq,
                              output=True)

        for d in data:
            s.write(d)
        s.close()
        pa.PyAudio().terminate()


if __name__ == '__main__':
    MainApp().run()