from PyQt6.QtCore import QThread, pyqtSignal
from client.SocketClient import SocketClient
from client.StudentClientHandler import StudentClientHandler

class ServiceCtrl(QThread):
    query_signal=pyqtSignal(dict)
    add_signal=pyqtSignal(dict)
    send_signal=pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.client = SocketClient("127.0.0.1", 20001)
        self.score_dict = dict()

    def query(self, name):
        student_handler = StudentClientHandler(self.client, {'name': name})
        response = student_handler.query_student()
        self.query_signal.emit(response)
        return response

    def add(self, name, subject, score):
        if name not in self.score_dict:
            self.score_dict[name] = {subject: score}
        else:
            self.score_dict[name][subject] = score
            
        self.add_signal.emit({'response': 'Score is ready to be sent. Click "send" to proceed.'})

    def send(self, name):
        score = self.score_dict.get(name)
        if score is not None:
            student_handler = StudentClientHandler(self.client, {'name': name, 'scores': self.score_dict[name]})
            student_handler.client.send_command('add', {'name': name, 'scores': self.score_dict[name]})
            response = self.client.wait_response()
            self.score_dict.pop(name, None)
            self.send_signal.emit({'response': response})
        else:
            self.send_signal.emit({'response': 'No score to send.'})