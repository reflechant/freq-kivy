# -*- coding: utf-8 -*-
import threading
import mmap
import struct as st
from math import sin, cos, radians
from random import randint
import pyaudio as pa


from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.button import Button

from kivy.clock import Clock, mainthread
from kivy.lang import Builder


class MainFrame(BoxLayout):
    pass


class MainApp(App):
    #stop = threading.Event()
    sample_freq = 44100
    duration = 1.0
    freqs = []

    def build(self):
        return MainFrame()


    def add_freq(self,w):
        f = Builder.load_file('freqwidget.kv')
        self.freqs.append(f)
        w.add_widget(f)

    def rm_freq(self,w):
        self.freqs.remove(w)
        w.parent.remove_widget(w)

    def save(self):
        pass

    def load(self):
        pass


    def start_play(self, btn):
        '''if btn.text == "остановить":
            print "начинаем играть"
            btn.text = "играть"
            #self.thread = threading.Thread(target=self.play)
            #self.thread.start()
        else:
            print "останавливаем"
            btn.text = "остановить"
            #self.stop.set()
        '''
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