import logging
from threading import Thread, Lock, Condition
from websockets.sync.server import serve
import sys
import websockets
from threading import Thread, RLock, Condition
import Scheduale
from BusSys import BusSys
from User import User
import json


class Server:
    def __init__(self, port):
        self.port = port
        self.busSys = BusSys()

    def parse(self, req):
        """
        This method parses the new request
        """
        req = req.strip()
        return req.split(" ")

    def initialize_server(self):
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

        self.busSys.add_line(
            user, token, 2, "Blue Ring", 120, 1400, 15, 1, "This is the blue line"
        )
        self.busSys.add_line(
            user, token, 2, "Red Ring", 500, 1400, 10, 2, "This is the red line"
        )
        self.busSys.add_line(
            user, token, 2, "Yellow Ring", 600, 1000, 20, 3, "This is the yellow line"
        )
        self.busSys.add_line(
            user, token, 2, "Green Ring", 100, 1200, 30, 4, "This is the green line"
        )
        self.busSys.add_line(
            user, token, 2, "Purple Ring", 160, 1300, 20, 5, "This is the purple line"
        )
        # TESTING END

    def handle_auth(self, connection):
        """
        This part checks if the user wants sign up or login
        to continue and be able to access the functions and send commands.
        If anything other than sign up or login is sent, the user is prompted
        to try again and they wont have access until they enter the correct form.
        """
        req = connection.recv(1024)
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
            return (user, token)

        elif parsed[0] == "auToken":
            if len(parsed) < 2:
                return (None, None)
            user = self.busSys.login_with_token(parsed[1])
            return (user, parsed[1])

        else:
            return (None, None)

    def handle_commands(self, user, token, command):
        """
        Handles user requests and gets response or result
        from the handle_req function and sends it back to user
        """
        parsed = self.parse(command)
        response = {
            "status": False,
            "status_str": None,
            "type": "command",
            "result": None,
        }
        try:
            func = getattr(self.busSys, parsed[0])
            response["result"] = func(user, token, *parsed[1:])
            response["status"] = True

        except AttributeError:
            print("Command Error", command)
            response["status"] = False
            response["status_str"] = "ERROR, Command not found"

        except Exception as e:
            print(e)
            response["status"] = False
            response["status_str"] = f"ERROR {str(e)}"

        return json.dumps(response)

    def notif_handler(self, connection, user, lst):
        """
        Sends notifictions whenever there are new updates for this user
        """
        while True:
            notificatoins = user.get_notifications()
            
            with lst[1]:
                if not lst[0] :
                    print("Notification Thread is dead")
                    return
            if (notificatoins):
                connection.send(json.dumps(notificatoins))

    def connection_handler(self, connection):
        user, token = self.handle_auth(connection)
        print(user, token)
        if user:
            print("Authentication Valid")
            response = {
                "type": "token",
                "token": token,
                "username": user.get_username(),
            }
            connection.send(json.dumps(response))
            mutex = RLock()
            lst = [True, mutex]
            notification_tread = Thread(
                target=self.notif_handler, args=(connection, user, lst)
            )
            notification_tread.start()

            try:
                command = connection.recv(1024)
                while command:
                    # Handling new commands
                    response = self.handle_commands(user, token, command)
                    connection.send(response)
                    # Receiving the next command
                    command = connection.recv(1024)

                print("Connection is closed")

            except websockets.exceptions.ConnectionClosed:
                print("Connection is terminated")

            # Killing notification thread
            with mutex:
                lst[0] = False
                user.notify("close")
            
            connection.close()


        else:
            print("Authentication Error")
            response = {
                "type": "error",
                "msg": "Authentication Error"
            }
            connection.send(json.dumps(response))
            connection.close()



def serveconnection(s: Server, connection):
    print("New Connection", connection.remote_address)
    s.connection_handler(connection)


def main():
    """
    Create the server and run it
    """
    HOST = ""
    PORT = int(sys.argv[2])
    s = Server(int(sys.argv[2]))
    s.initialize_server()
    with serve(
        lambda connection: serveconnection(s, connection), host=HOST, port=PORT
    ) as server:
        print("web socket server started")
        server.serve_forever()


if __name__ == "__main__":
    main()
