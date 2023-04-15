import cmd 
from Map import Map

map_path = "./test/test_map.json"

class BusSys(cmd.Cmd):
    intro = 'Welcome to busSys. The power of bus simulation is here\n'
    prompt = '(busSys)$: '

    def do_wtf(self, args):
        print("wtf is a word used be people for expressing internail feelings of wtf")

    def do_map_test(self, args):
        print("Tesing map Functionalities")
        my_map = Map(path=map_path)
        temp = my_map.shortest(1,2)
        if (temp[0] == [1]):
            print("Shortest is fine")
        else:
            print("Shortest has a problem")
            print(temp)




if __name__ == "__main__":
    BusSys().cmdloop()