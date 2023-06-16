class Route:
    route_name: str
    file_path: str

    def __init__(self, route_name: str, file_path: str):
        self.route_name = route_name
        self.file_path = file_path