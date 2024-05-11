class Query:
    def __init__(self, socket_client, query_dict):
        self.socket_client = socket_client
        self.query_dict = query_dict

    def execute(self):
        self.socket_client.send_command("query", self.query_dict)
        response = self.socket_client.wait_response()
        response_dict = response  
        if response_dict["status"] == 'Fail':
            reason = "The name is not found."
            return {'status': "Fail", 'reason': reason}
        else:
            print(f"The name {self.query_dict['name']} is already exist.")
            return {'status': "OK", 'scores': self.query_dict['scores'] }
