import select
import socket
import sys
import time

from encrypt import AESCipher

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

server_addr = ('localhost',46643)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(server_addr)

passwd = input('You can now enter a password for your server, or press enter for none: ')

enc = AESCipher(passwd)

server.listen(12)

SOCKS = [server]

nicknames = {}

def chat_server():

  global SOCKS, nicknames, passwd
  while SOCKS:

    readable, writable, exception = select.select(SOCKS,[],[],0)

    for s in readable:

      elif s == server:
        sock, addr = server.accept()
        SOCKS.append(sock)
        print('{} connected to server\n'.format(addr))

        nicknames[sock] = addr
        broadcast(s,'{} connected to server\n'.format(addr))

      else:

        data = s.recv(4096)

        try:
          plaintext = enc.decrypt(data)
          assert plaintext
        except:
          plaintext = 'User has sent message using an incorrect password\n'

        if data:
          if plaintext.startswith('/nick '):
            broadcast(s,'{} changed their nickname to {}'.format(nicknames[s],plaintext[6:]))
            nicknames[s] = plaintext[6:].strip()

          else:
            broadcast(s,'{}: {}'.format(nicknames[s],plaintext))
        else:
          broadcast(s,'{} killed the connection\n'.format(s.getpeername()))
          print('{} killed the connection\n'.format(s.getpeername()))
          if s in SOCKS:
            SOCKS.remove(s)
          s.close()

    for s in exception:
      broadcast(s,'{} killed the connection\n'.format(s.getpeername()))
      print('{} killed the connection\n'.format(s.getpeername()))
      if s in SOCKS:
        SOCKS.remove(s)
      s.close()


def broadcast(sock,message):
  global server, SOCKS
  for s in SOCKS:
    if s not in [sock,server]:
      try:
        s.send(enc.encrypt(message))
      except:
        s.close()
        if s in SOCKS:
          SOCKS.remove(s)


chat_server()
