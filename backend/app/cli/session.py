class CLISession:
    def __init__(self, device_id):
        self.device_id = device_id
        self.history = []

    def execute(self, command):
        self.history.append(command)
        return f"{self.device_id}> {command}"
