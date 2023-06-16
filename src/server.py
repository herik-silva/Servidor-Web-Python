import socket
from core.domain.entities.server_address import ServerAddress
from core.helpers.filter_element import filter_element
from routes.public import *

import os

class Server:
    __server_address: ServerAddress
    __data_payload: int
    __route_list: list[Route]

    def __init__(self, host: str = 'localhost', port: int = 8000):
        self.__server_address = ServerAddress(host, port)
        print(self.__server_address.get_host())
        self.__data_payload = 2048
        self.__route_list = [
            HOME,
            ABOUT
        ]

    def handle_request(self, content: bytes):
        # Conteúdo da resposta
        response_content = content

        # Cabeçalhos da resposta
        response_headers = [
            b"HTTP/1.1 200 OK",
            b"Content-Type: text/html",
            b"Content-Length: " + str(len(response_content)).encode(),
            b"Connection: close",
        ]

        # Junta os cabeçalhos com duas quebras de linha para formar o cabeçalho completo
        response = b"\r\n".join(response_headers) + b"\r\n\r\n" + response_content
        return response

    def get_route(self, request: bytes):
        decoded_request = request.decode()
        route = decoded_request.split(" HTTP/1.1")[0]
        return route[4:]
    
    def send_response(self, data: bytes, client: socket.socket):
        route = self.get_route(data)
        print("Rota Solicitada: " + route)
        founded_route = filter_element(self.__route_list, "route_name", route)
        if(founded_route):
            try:
                with open(os.getcwd() + founded_route.file_path, "rb") as file:
                    content = file.read()
                    response = self.handle_request(content)
                    client.send(response)

            except:
                print("ARQUIVO NÃO ENCONTRADO")
                with open(os.getcwd() + "/public/404.html", "rb") as file:
                    content = file.read()
                    response = self.handle_request(content)
                    client.send(response)
        else:
            print("ROTA NAO EXISTE")
            with open(os.getcwd() + "/public/404.html", "rb") as file:
                content = file.read()
                response = self.handle_request(content)
                client.send(response)

        client.close()

    def run_server(self):
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Servidor ouvindo na porta: {}\nAcesse a url http://{}:{}".format(self.__server_address.get_port(), self.__server_address.get_host(), self.__server_address.get_port()))
        conn_socket.bind(self.__server_address.get_address())
        conn_socket.listen(5)

        nRequests = 0

        while True:
            print("Esperando receber uma mensagem do cliente")
            client, address = conn_socket.accept()
            data = client.recv(self.__data_payload)
            if data:
                self.send_response(data, client)
                nRequests +=1

                if nRequests > 20: break

        conn_socket.close()