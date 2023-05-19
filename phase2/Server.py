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
        '''
        Parses command given by user in the sense that
        it transforms the command into data that can be passed
        to our functions in our system
        '''
        # remove trailing newline and blanks
        req = req.rstrip()
        r = req.decode().split()
        result = []
        i = 0
        while i < len(r): 
        # handling the part where strings with spaces are passed and
        # we need them to remain as they are, not seperated 
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
        # result is a list of the command and the arguments 
        return result

    def handle_auth(self, sock):
        '''
        This part checks if the user wants sign up or login
        to continue and be able to access the functions and send commands.
        If anything other than sign up or login is sent, the user is prompted
        to try again and they wont have access until they enter the correct form.
        '''
        req = sock.recv(1000)

        parsed = self.parse(req)
        if parsed[0] == "login":
            if len(parsed) < 3:
                return (None, None)
            user, token = self.busSys.login(parsed[1], parsed[2])
            return (user, token)
        elif parsed[0] == "register":
            if len(parsed) < 3:
                return (None, None)
            user, token = self.busSys.register(parsed[1], parsed[2])
            return (user,token)
        elif parsed[0] == "auToken":
            if len(parsed) < 2:
                return (None, None)
            user = self.busSys.login_with_token(parsed[1])
            return (user, parsed[1])
        else:
            return (None, None)

    def handle_req(self, req, user, token):
        '''
        Takes the parsed user request
        and calls the underlying function
        in our system if the command is valid
        then sends back the result to
        the user_cmd function
        '''
        result = None
        try:
            if (req[0] == "close"):
                return None
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
        '''
        Creates a new user
        This thread divides into two threads:
        one handles the user commands and replies to them,
        the other sends notifications if there are any new updates
        '''
        ns.send("new here? type register , otherwise type login or auToken \n".encode())
        user, token = self.handle_auth(ns)
        if (not user or not token):
            ns.send("Authentication Error\n".encode())
            ns.close()
            return 
        ns.send((str(token)+ "\n").encode())
        # call auth here
        task1 = Thread(target=self.user_cmd,  args=(ns, user, token))
        task2 = Thread(target=self.notif_handler, args=(ns, user, token))
        task1.start()
        task2.start()

    def user_cmd(self, sock, user, token):
        '''
        Handles user requests and gets response or result
        from the handle_req function and sends it back to user
        '''
        req = sock.recv(1000)
        while req and req != '':
            parsed = self.parse(req)
            handled_req_response = self.handle_req(parsed, user, token)
            if handled_req_response == None:
                sock.send("Goodbye".encode())
                sock.close()
                return 
            sock.send(handled_req_response.encode())
            req = sock.recv(1000)

    def notif_handler(self, sock, user, token):
        '''
        Sends notifictions whenever there are new updates for this user
        '''
        while True:
            notificatoins = user.get_notifications()
            sock.send(str(notificatoins).encode())

    def server(self):
        '''
        Heart of the program
        creates a TCP socket and binds to it
        then starts listening.
        As soon as a user connects, it starts
        a new agent thread to handle this new user'''
        # this user is for testing

        user, token = self.busSys.register("admin", "admin")
        # TESTING START
        self.busSys.add_map(user, token, 0, "./test/test_map.json")
        self.busSys.add_schedule(user, token, 1, "The First one")

        self.busSys.add_stop(user, token, 2, 1, True, 20, "S11")
        self.busSys.add_stop(user, token, 2, 1, False, 80, "S12")

        self.busSys.add_stop(user, token, 2, 2, True, 20, "S21")
        self.busSys.add_stop(user, token, 2, 2, False, 80, "S22")

        self.busSys.add_stop(user, token, 2, 3, True, 20, "S31")
        self.busSys.add_stop(user, token, 2, 3, False, 80, "S32")

        self.busSys.add_stop(user, token, 2, 4, True, 20, "S41")
        self.busSys.add_stop(user, token, 2, 4, False, 80, "S42")

        self.busSys.add_stop(user, token, 2, 5, True, 20, "S51")
        self.busSys.add_stop(user, token, 2, 5, False, 80, "S52")

        self.busSys.add_stop(user, token, 2, 6, True, 20, "S61")
        self.busSys.add_stop(user, token, 2, 6, False, 80, "S62")

        self.busSys.add_stop(user, token, 2, 7, True, 20, "S71")
        self.busSys.add_stop(user, token, 2, 7, False, 80, "S72")

        self.busSys.add_stop(user, token, 2, 8, True, 20, "S81")
        self.busSys.add_stop(user, token, 2, 8, False, 80, "S82")

        self.busSys.add_stop(user, token, 2, 9, True, 20, "S91")
        self.busSys.add_stop(user, token, 2, 9, False, 80, "S92")

        self.busSys.add_stop(user, token, 2, 10, True, 20, "S101")
        self.busSys.add_stop(user, token, 2, 10, False, 80, "S102")

        self.busSys.add_route(user, token, 2)
        self.busSys.add_stop_to_route(user, token, 2, 1, 1, 4)
        self.busSys.add_stop_to_route(user, token, 2, 1, 10, 3)
        self.busSys.add_stop_to_route(user, token, 2, 1, 12, 4)
        self.busSys.add_stop_to_route(user, token, 2, 1, 20, 4)
        self.busSys.add_stop_to_route(user, token, 2, 1, 4, 4)

        self.busSys.add_route(user, token, 2)
        self.busSys.add_stop_to_route(user, token, 2, 2, 6, 4)
        self.busSys.add_stop_to_route(user, token, 2, 2, 16, 5)
        self.busSys.add_stop_to_route(user, token, 2, 2, 8, 4)
        self.busSys.add_stop_to_route(user, token, 2, 2, 18, 4)
        self.busSys.add_stop_to_route(user, token, 2, 2, 19, 4)

        self.busSys.add_route(user, token, 2)
        self.busSys.add_stop_to_route(user, token, 2, 3, 17, 4)
        self.busSys.add_stop_to_route(user, token, 2, 3, 9, 5)
        self.busSys.add_stop_to_route(user, token, 2, 3, 2, 4)
        self.busSys.add_stop_to_route(user, token, 2, 3, 6, 4)
        self.busSys.add_stop_to_route(user, token, 2, 3, 16, 4)
        self.busSys.add_stop_to_route(user, token, 2, 3, 8, 4)

        self.busSys.add_route(user, token, 2)
        self.busSys.add_stop_to_route(user, token, 2, 4, 5, 4)
        self.busSys.add_stop_to_route(user, token, 2, 4, 9, 5)
        self.busSys.add_stop_to_route(user, token, 2, 4, 7, 4)
        self.busSys.add_stop_to_route(user, token, 2, 4, 3, 4)
        self.busSys.add_stop_to_route(user, token, 2, 4, 1, 4)
        self.busSys.add_stop_to_route(user, token, 2, 4, 16, 4)


        self.busSys.add_route(user, token, 2)
        self.busSys.add_stop_to_route(user, token, 2, 5, 7, 4)
        self.busSys.add_stop_to_route(user, token, 2, 5, 17, 5)
        self.busSys.add_stop_to_route(user, token, 2, 5, 20, 4)
        self.busSys.add_stop_to_route(user, token, 2, 5, 12, 4)
        self.busSys.add_stop_to_route(user, token, 2, 5, 11, 4)
        self.busSys.add_stop_to_route(user, token, 2, 5, 13, 4)
        
        self.busSys.add_line(user, token, 2, "Blue Ring", 120, 1400, 15, 1, "This is the blue line")
        self.busSys.add_line(user, token, 2, "Red Ring", 500, 1400, 10, 2, "This is the red line")
        self.busSys.add_line(user, token, 2, "Yellow Ring", 600, 1000, 20, 3, "This is the yellow line")
        self.busSys.add_line(user, token, 2, "Green Ring", 100, 1200, 30, 4, "This is the green line")
        self.busSys.add_line(user, token, 2, "Purple Ring", 160, 1300, 20, 5, "This is the purple line")
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
    '''
    Create the server and run it
    '''
    s = Server(int(sys.argv[2]))
    try:
        s.server()
    except KeyboardInterrupt:
        s.close()


if __name__ == "__main__":
    main()


# server = Thread(target=Server.server, args=(20445,))
