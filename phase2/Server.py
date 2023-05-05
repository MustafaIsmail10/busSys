from socket import *
import os
import sys
from threading import Thread
import Scheduale
from BusSys import BusSys
from User import User


class Server():
    # TCP port taken as a command line option as:  python3 yourapp.py --port 1423
    # need to parse cmd and call Server(port) then Server.server()
    def __init__(self, port):
        self.port = port
        self.sock = None
        self.busSys = BusSys()

    def parse(self, req):
        # remove trailing newline and blanks
        req = req.rstrip()
        return req.decode().split()

    def handle_auth(self, sock,user):
        req = sock.recv(1000)
        while req and req != '':
            parsed = self.parse(req)
            if parsed[0] == "login":
                token = user.login()
                return token
            elif parsed[0] == "sign":
                token = user.login()
                return token
            else:
                sock.send("try again \n".encode())
                req = sock.recv(1000)

    def handle_req(self, req, user , token):
        try:
            func = getattr(self.busSys, req[0])
        except AttributeError:
            print("not found")
            exit()
        print("user",user)
        print(token)
        return str(func(user, token, *req[1:]))

    def agent(self, ns):
        user = User()
        ns.send("new here? type sign up , otherwise type login \n".encode())
        token = self.handle_auth(ns,user)
        # call auth here
        task1 = Thread(target=self.user_cmd,  args=(ns, user, token))
        task2 = Thread(target=self.notif_handler, args=(ns, user, token))
        task1.start()
        task2.start()

    def user_cmd(self, sock, user, token):
        req = sock.recv(1000)
        while req and req != '':
            parsed = self.parse(req)
            handled_req_response = self.handle_req(parsed,user,token)
            sock.send(handled_req_response.encode())
            req = sock.recv(1000)

    def notif_handler(self,sock,user,token):
        pass

    def server(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen()  # check limitations
        try:
            while True:
                ns, peer = self.sock.accept()
                print(peer, "connected\n")
                # create a thread with new socket
                t = Thread(target=self.agent,  args=(ns,))
                t.start()

        finally:
            self.sock.close()


def main():
    s = Server(1423)
    s.server()
    pass


if __name__ == "__main__":
    main()


# server = Thread(target=Server.server, args=(20445,))
