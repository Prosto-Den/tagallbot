class Memory:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self):
        from psutil import virtual_memory
        self.__ram = virtual_memory().total * 0.5

    @property
    def max_ram(self):
        return self.__ram

memory = Memory()
