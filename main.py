from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock

import select
import socket
from encrypt import AESCipher

class Chat(Widget):
  tout = ObjectProperty(None)
  tin = ObjectProperty(None)
  send_btn = ObjectProperty(None)



  def __init__(self, *args, **kwargs):
    super(Chat, self).__init__(*args, **kwargs)

    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client.settimeout(2)
    server_addr = ('localhost', 46643)

    #passwd = input('Please enter the server password now, or press enter for none: ')
    passwd = ''

    self.enc = AESCipher(passwd)

    try:
      self.client.connect(server_addr)
    except:
      print('Unable to establish connection')

    print('Welcome to the server. Type `/nick ` to set your nickname on this server.')

    Clock.schedule_interval(self.chat_client, 0)

  def chat_client(self,e):

    readable, writable, exception = select.select([self.client],[],[],0)

    if self.client in readable:
      data = self.client.recv(4096)
      if not data:
        print('Server connection killed.')
      else:
        self.tout.text += '\n' + self.enc.decrypt(data)


  def send_msg(self):
    self.client.send(self.enc.encrypt(self.tin.text))

class Manager(ScreenManager):
  pass

class Main(App):
  def build(self):
    return Manager()

Main().run()
