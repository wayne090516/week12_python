class AddStu:
    def __init__(self, client, parameters):
        self.client = client
        self.parameters = parameters

    def execute(self):
        self.client.send_command("add", self.parameters)
        response = eval(self.client.wait_response())

        return response