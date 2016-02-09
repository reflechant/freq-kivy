from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


class MainFrame(BoxLayout):
    pass


class MainApp(App):
    def build(self):
        return MainFrame()


if __name__ == '__main__':
    MainApp().run()
