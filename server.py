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

socks = [server]

nicknames = {}

def chat_server():

  global socks, nicknames, passwd
  while socks:

    readable, writable, exception = select.select(socks,[],[],0)

    for s in readable:

      if s == server:
        sock, addr = server.accept()
        socks.append(sock)
        print('{} connected to server'.format(addr))

        nicknames[sock] = addr
        broadcast(s,'{} connected to server'.format(addr))

      else:

        try:
          data = s.recv(4096)
        except ConnectionResetError:
          broadcast(s,'{} killed the connection'.format(nicknames[s]))
          print('{} killed the connection'.format(nicknames[s]))
          if s in socks:
            socks.remove(s)
          s.close()
          continue

        try:
          plaintext = enc.decrypt(data)
          assert plaintext
        except:
          continue

        if data:
          if plaintext.startswith('/help'):
            s.send(enc.encrypt('/nick <nickname> - change nickname'))

          elif plaintext.startswith('/nick '):
            broadcast(s,'{} changed their nickname to {}'.format(nicknames[s],plaintext[6:]))
            nicknames[s] = plaintext[6:].strip()

          else:
            broadcast(s,'{}: {}'.format(nicknames[s],plaintext))
        else:
          broadcast(s,'{} killed the connection'.format(nicknames[s]))
          print('{} killed the connection\n'.format(nicknames[s]))
          if s in socks:
            socks.remove(s)
          s.close()

    for s in exception:
      broadcast(s,'{} killed the connection'.format(nicknames[s]))
      print('{} killed the connection'.format(nicknames[s]))
      if s in socks:
        socks.remove(s)
      s.close()


def broadcast(sock,message):
  global server, socks

  for s in socks:
    if s != server:
      try:
        s.send(enc.encrypt(message))
      except:
        s.close()
        if s in socks:
          socks.remove(s)


chat_server()
