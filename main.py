from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock

import select
import socket
import sys

from encrypt import AESCipher

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
        self.tout.text += '\nConnection to {}:{} failed. If you\'ve already connected to a server, try restarting your client.'.format(text.split(' ')[1], text.split(' ')[2])
        self.connected = 0

    elif text == '#exit':
      sys.exit()

    elif self.connected:
      self.client.send(self.enc.encrypt(text))

    self.tin.text = ''

class Manager(ScreenManager):
  pass

class Main(App):
  def build(self):
    Builder.load_string('''
<Chat>:
  tout: tout
  tin: tin
  send_btn: send_btn

  TextInput:
    id: tout
    width: root.width
    height: root.height * 0.94
    y: root.height * 0.06
    text: "Use #connect <ip> <port> to connect to a server. Use the command `/help` to view a server's commands. Use #passwd <password> if the server you're connected to has encryption."

  TextInput:
    id: tin
    focus: True
    multiline: False
    width: root.width * 0.9
    height: root.height * 0.06
    on_text_validate: root.send_msg()

  Button:
    id: send_btn
    width: root.width * 0.1
    height: root.height * 0.06
    x: root.width * 0.9
    text: 'Send'
    on_press: root.send_msg()

<Manager>:

  Screen:
    name: 'chat'
    Chat:
      id: chat''')
    return Manager()

Main().run()
