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
        r = req.decode().split()
        result = []
        i = 0;
        while i < len(r):
            if r[i][0] == '"':
                string = ""
                while r[i][-1] != '"':
                    string += r[i] + " "                   
                    i +=1;
                string += r[i]
                string = string.rstrip()
                result.append(string)
            else:
                result.append(r[i])
            i += 1
        return result   

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
        ##################### TESTING START
        self.busSys.add_map(user, token, 0, "./test/test_map.json")
        self.busSys.add_schedule(user, token, 0, "The First one")
        self.busSys.add_stop(user, token, 1, 1, True, 30, "S1")
        self.busSys.add_stop(user, token, 1, 5, True, 40, "S2")
        self.busSys.add_stop(user, token, 1, 6, True, 6, "S3")
        self.busSys.add_stop(user, token, 1, 7, True, 56, "S4")
        self.busSys.add_stop(user, token, 1, 2, True, 50, "S5")
        self.busSys.add_stop(user, token, 1, 3, True, 10, "S6")
        self.busSys.add_stop(user, token, 1, 4, True, 50, "S7")
        self.busSys.add_stop(user, token, 1, 7, True, 30, "S8")
        self.busSys.add_stop(user, token, 1, 6, True, 52, "S9")
        self.busSys.add_stop(user, token, 1, 8, True, 50, "S10")
        self.busSys.add_stop(user, token, 1, 2, True, 10, "S11")
        self.busSys.add_stop(user, token, 1, 3, True, 50, "S12")
        ##################### TESTING END


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
    s = Server(1427)
    s.server()
    pass


if __name__ == "__main__":
    main()


# server = Thread(target=Server.server, args=(20445,))
