from client.client_command.AddStu import AddStu
from client.client_command.Query import Query
from PyQt6.QtCore import QThread, pyqtSignal
from client.client import SocketClient
import json

class ServiceControl(QThread):
    query_signal=pyqtSignal(dict)
    add_signal=pyqtSignal(dict)
    send_signal=pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.socket_client = SocketClient()
        self.score_dict = dict()

    def query(self,name):
        response=Query(self.socket_client,{'name':name, 'scores': self.score_dict}).execute()
        self.query_signal.emit(response)

    def add(self,subject,score):
        self.score_dict[subject]=score
        response={'status': "OK", 'parameters': (f"add {subject} : {score}")}
        self.add_signal.emit(response)

    def send(self,name):
        response=AddStu(self.socket_client,{'name': name, 'scores': self.score_dict}).execute()
        print("response received: ", response)
        self.score_dict={}
        if response:
            response_dict = json.loads(response)
            self.send_signal.emit(response_dict)