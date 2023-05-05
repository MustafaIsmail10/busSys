from BusSys import BusSys 
from User import User








busSys = BusSys()
user = User()
token = user.login()

# busSys.print_hello(user, token, "WTF")

map_id = busSys.add_map(user, token , 0, "./test/test_map.json")
user.add_map(map_id)

schedule_id = busSys.add_schedule(user, token, map_id, "OMIGOS")
user.add_schedule(schedule_id)




