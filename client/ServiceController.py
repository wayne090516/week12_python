from client.AddStu import AddStu
from client.Query import Query
from PyQt6.QtCore import QThread, pyqtSignal
from client.SocketClient import SocketClient

class ServiceController(QThread):
    query_signal = pyqtSignal(str)
    send_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.client = SocketClient()
        self.parameters = dict()

    def query_stu(self, name):
        response = Query(self.client,{"name":name}).execute()
        self.query_signal.emit(response["status"])
    
    def send_stu(self, parameters):
        response = AddStu(self.client, parameters).execute()
        self.send_signal.emit(response["status"])
