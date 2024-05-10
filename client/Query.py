class Query:
    def __init__(self, client, name):
        self.client = client
        self.name = name

    def execute(self):
        self.client.send_command("query", self.name)
        response = eval(self.client.wait_response())

        return response