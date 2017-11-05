import socket
import select
import sys

from encrypt import AESCipher

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(2)
server_addr = ('localhost', 46643)

passwd = input('Please enter the server password now, or press enter for none: ')

enc = AESCipher(passwd)

try:
  client.connect(server_addr)
except:
  print('Unable to establish connection')

def chat_client():
  global client

  print('Welcome to the server. Type `/nick ` to set your nickname on this server.')

  sys.stdout.write('[Me] ')
  sys.stdout.flush()

  while 1:
    SOCKS = [sys.stdin, client]

    readable, writable, exception = select.select(SOCKS,[],[],0)

    for s in readable:
      if s == client:
        data = s.recv(4096)
        if not data:
          print('Server connection killed.')
          sys.exit()
        else:
          try:
            sys.stdout.write('\r' + enc.decrypt(data))
          except:
            pass
          sys.stdout.write('[Me] ')
          sys.stdout.flush()

      else:
        msg = sys.stdin.readline()
        client.send(enc.encrypt(msg))
        sys.stdout.write('[Me] ')
        sys.stdout.flush()

chat_client()
