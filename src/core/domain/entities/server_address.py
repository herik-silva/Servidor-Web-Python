class ServerAddress:
    __host: str
    __port: int

    def __init__(self, host: str, port: int):
        self.__host = host
        self.__port = port

    def get_host(self):
        return self.__host
    
    def get_port(self):
        return self.__port
    
    def get_address(self):
        return (self.__host, self.__port)