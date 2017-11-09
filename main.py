from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock

import select
import socket
import sys
try:
  from encrypt import AESCipher
except ImportError:
  print('Windows Compatibility mode enabled. You will be UNABLE to connect to secured servers!')
  class AESCipher():
    def __init__(self,passw):
      pass
    def encrypt(msg):
      return msg.encode()
    def decrypt(msg):
      return msg.decode()

class Chat(Widget):
  tout = ObjectProperty(None)
  tin = ObjectProperty(None)
  send_btn = ObjectProperty(None)

  def __init__(self, *args, **kwargs):
    super(Chat, self).__init__(*args, **kwargs)

    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client.settimeout(2)

    self.enc = AESCipher('')

    self.connected = 0

    Clock.schedule_interval(self.chat_client, 0)

  def chat_client(self,e):
    self.tin.focus = True

    if self.connected:
      readable, writable, exception = select.select([self.client],[],[],0)

      if self.client in readable:
        data = self.client.recv(4096)
        if not data:
          self.tout.text = 'Server connection killed.'
        else:
          try:
            self.tout.text += '\n' + self.enc.decrypt(data)
          except:
            pass

  def send_msg(self):
    text = self.tin.text
    if text.startswith('#passwd '):
      self.enc = AESCipher(text[8:])

    elif text.startswith('#connect '):
      try:
        self.client.connect((text.split(' ')[1], int(text.split(' ')[2])))
        self.connected = 1
      except:
        self.tout.text += '\nConnection to {}:{} failed.'.format(text.split(' ')[1], text.split(' ')[2])
        self.connected = 0

    elif text == '/exit':
      sys.exit()

    else:
      self.client.send(self.enc.encrypt(text))

    self.tin.text = ''

class Manager(ScreenManager):
  pass

class Main(App):
  def build(self):
    return Manager()

Main().run()
