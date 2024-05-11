from socket_cli.AddStu import AddStu
from socket_cli.Query import Query
from PyQt6.QtCore import QThread, pyqtSignal
from socket_cli.Socket_cli import SocketClient



class Control(QThread):
    query_signal=pyqtSignal(dict)
    add_signal=pyqtSignal(dict)
    send_signal=pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.client = SocketClient()
        self.score_dict = dict()

    def query(self,name):
        pesponse=Query(self.client,{"name":name}).execute()
        self.query_signal.emit(pesponse)

    def add(self,subject,score):
        self.score_dict[subject]=score
        pesponse={'status': "OK", 'reason': (f"add {subject} : {score}")}
        self.add_signal.emit(pesponse)

    def send(self,name):
        pesponse=AddStu(self.client,{'name': name, 'scores': self.score_dict}).execute()
        self.score_dict={}
        self.send_signal.emit(pesponse)


