import json

class AddStu:
    def __init__(self, socket_client,add_dict):
        self.socket_client = socket_client
        self.add_dict = add_dict

    def execute(self):       
        self.socket_client.send_command("add", self.add_dict)
        response = self.socket_client.wait_response()
        #response_dict = json.loads(response)
        if response["status"] == "OK":
            print(f"Add {self.add_dict} success")
            return json.dumps({'status': "OK", 'parameters': self.add_dict})
            #return response
        else:
            print(f"Add {self.add_dict} failed")
            return json.dumps({'status': "Fail", 'parameters': self.add_dict})
            #return response
    
