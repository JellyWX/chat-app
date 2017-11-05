from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.button import Button


class Chat(Widget):
  pass

class Manager(ScreenManager):
  pass

class Main(App):
  def build(self):
    return Manager()

Main().run()
