from phase1.Map import *
from threading  import RLock

class MapProxy(Map):
    def __init__(self, **kwargs) -> None:
        self.guardian = RLock()
        super.__init__(kwargs)

    