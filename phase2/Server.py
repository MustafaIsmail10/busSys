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
        i = 0
        while i < len(r):
            if r[i][0] == '"':
                string = ""
                while r[i][-1] != '"':
                    string += r[i] + " "
                    i += 1
                string += r[i]
                string = string.rstrip()
                result.append(string)
            else:
                result.append(r[i])
            i += 1
        return result

    def handle_auth(self, sock, user):
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

    def handle_req(self, req, user, token):
        result = None
        try:
            func = getattr(self.busSys, req[0])
            result = func(user, token, *req[1:])
        except AttributeError:
            print("not found")
            return "ERROR, Command not found\n"
        except Exception as e:
            print(e)
            return f"ERROR {str(e)}\n"
        print("user", user)
        print(token)
        return str(result)

    def agent(self, ns):
        user = User()
        ns.send("new here? type sign up , otherwise type login \n".encode())
        token = self.handle_auth(ns, user)
        # call auth here
        task1 = Thread(target=self.user_cmd,  args=(ns, user, token))
        task2 = Thread(target=self.notif_handler, args=(ns, user, token))
        task1.start()
        task2.start()

    def user_cmd(self, sock, user, token):
        req = sock.recv(1000)
        while req and req != '':
            parsed = self.parse(req)
            handled_req_response = self.handle_req(parsed, user, token)
            sock.send(handled_req_response.encode())
            req = sock.recv(1000)

    def notif_handler(self, sock, user, token):
        while True:
            notificatoins = user.get_notifications()
            sock.send(str(notificatoins).encode())

    def server(self):
        user = User()
        token = user.login()
        # TESTING START
        self.busSys.add_map(user, token, 0, "./test/test_map.json")
        self.busSys.add_schedule(user, token, 0, "The First one")

        self.busSys.add_stop(user, token, 1, 1, True, 20, "S11")
        self.busSys.add_stop(user, token, 1, 1, False, 80, "S12")

        self.busSys.add_stop(user, token, 1, 2, True, 20, "S21")
        self.busSys.add_stop(user, token, 1, 2, False, 80, "S22")

        self.busSys.add_stop(user, token, 1, 3, True, 20, "S31")
        self.busSys.add_stop(user, token, 1, 3, False, 80, "S32")

        self.busSys.add_stop(user, token, 1, 4, True, 20, "S41")
        self.busSys.add_stop(user, token, 1, 4, False, 80, "S42")

        self.busSys.add_stop(user, token, 1, 5, True, 20, "S51")
        self.busSys.add_stop(user, token, 1, 5, False, 80, "S52")

        self.busSys.add_stop(user, token, 1, 6, True, 20, "S61")
        self.busSys.add_stop(user, token, 1, 6, False, 80, "S62")

        self.busSys.add_stop(user, token, 1, 7, True, 20, "S71")
        self.busSys.add_stop(user, token, 1, 7, False, 80, "S72")

        self.busSys.add_stop(user, token, 1, 8, True, 20, "S81")
        self.busSys.add_stop(user, token, 1, 8, False, 80, "S82")

        self.busSys.add_stop(user, token, 1, 9, True, 20, "S91")
        self.busSys.add_stop(user, token, 1, 9, False, 80, "S92")

        self.busSys.add_stop(user, token, 1, 10, True, 20, "S101")
        self.busSys.add_stop(user, token, 1, 10, False, 80, "S102")

        self.busSys.add_route(user, token, 1)
        self.busSys.add_stop_to_route(user, token, 1, 1, 1, 4)
        self.busSys.add_stop_to_route(user, token, 1, 1, 10, 3)
        self.busSys.add_stop_to_route(user, token, 1, 1, 12, 4)
        self.busSys.add_stop_to_route(user, token, 1, 1, 20, 4)
        self.busSys.add_stop_to_route(user, token, 1, 1, 4, 4)

        self.busSys.add_route(user, token, 1)
        self.busSys.add_stop_to_route(user, token, 1, 2, 6, 4)
        self.busSys.add_stop_to_route(user, token, 1, 2, 16, 5)
        self.busSys.add_stop_to_route(user, token, 1, 2, 8, 4)
        self.busSys.add_stop_to_route(user, token, 1, 2, 18, 4)
        self.busSys.add_stop_to_route(user, token, 1, 2, 19, 4)

        self.busSys.add_route(user, token, 1)
        self.busSys.add_stop_to_route(user, token, 1, 3, 17, 4)
        self.busSys.add_stop_to_route(user, token, 1, 3, 9, 5)
        self.busSys.add_stop_to_route(user, token, 1, 3, 2, 4)
        self.busSys.add_stop_to_route(user, token, 1, 3, 6, 4)
        self.busSys.add_stop_to_route(user, token, 1, 3, 16, 4)
        self.busSys.add_stop_to_route(user, token, 1, 3, 8, 4)

        self.busSys.add_route(user, token, 1)
        self.busSys.add_stop_to_route(user, token, 1, 4, 5, 4)
        self.busSys.add_stop_to_route(user, token, 1, 4, 9, 5)
        self.busSys.add_stop_to_route(user, token, 1, 4, 7, 4)
        self.busSys.add_stop_to_route(user, token, 1, 4, 3, 4)
        self.busSys.add_stop_to_route(user, token, 1, 4, 1, 4)
        self.busSys.add_stop_to_route(user, token, 1, 4, 16, 4)


        self.busSys.add_route(user, token, 1)
        self.busSys.add_stop_to_route(user, token, 1, 5, 7, 4)
        self.busSys.add_stop_to_route(user, token, 1, 5, 17, 5)
        self.busSys.add_stop_to_route(user, token, 1, 5, 20, 4)
        self.busSys.add_stop_to_route(user, token, 1, 5, 12, 4)
        self.busSys.add_stop_to_route(user, token, 1, 5, 11, 4)
        self.busSys.add_stop_to_route(user, token, 1, 5, 13, 4)
        
        self.busSys.add_line(user, token, 1, "Blue Ring", 120, 1400, 15, 1, "This is the blue line")
        self.busSys.add_line(user, token, 1, "Red Ring", 500, 1400, 10, 2, "This is the red line")
        self.busSys.add_line(user, token, 1, "Yellow Ring", 600, 1000, 20, 3, "This is the yellow line")
        self.busSys.add_line(user, token, 1, "Green Ring", 100, 1200, 30, 4, "This is the green line")
        self.busSys.add_line(user, token, 1, "Purple Ring", 160, 1300, 20, 5, "This is the purple line")
        # TESTING END
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

    def close(self):
        self.sock.close()


def main():
    s = Server(int(sys.argv[2]))
    try:
        s.server()
    except KeyboardInterrupt:
        s.close()


if __name__ == "__main__":
    main()


# server = Thread(target=Server.server, args=(20445,))
