from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import *
from client.ServiceCtrl import ServiceCtrl

class AddStuWidget(QtWidgets.QWidget):
    dataOut = QtCore.pyqtSignal(object)


    def __init__(self):
        super().__init__()
        self.setObjectName("add_stu_widget")
        self.scores = {}
        layout = QtWidgets.QGridLayout()

        self.service_ctrl = ServiceCtrl()
        
        header_label = LabelComponent(20, "Add Student")
        
        name_label = LabelComponent(16, "Name: ")
        self.name_label = LineEditComponent("Name")
        self.name_label.mousePressEvent = lambda event, le=self.name_label: le.clear()

        query_button = ButtonComponent("Query")
        query_button.clicked.connect(self.query_name) 
        self.result_label = LabelComponent(16, "")

        subject_label = LabelComponent(16, "Subject: ")
        self.subject_label = LineEditComponent("Subject")
        self.subject_label.mousePressEvent = lambda event, le=self.subject_label: le.clear()
        self.subject_label.setReadOnly(True)
        self.subject_label.mousePressEvent = self.subject_label_click_handler
        
        score_label = LabelComponent(16, "Score: ")
        self.score_label = NumberLineEditComponent("", 3, 100, 16)
        
        add_button = ButtonComponent("Add")
        add_button.clicked.connect(self.confirm_action)

        send_button = ButtonComponent("Send")
        send_button.clicked.connect(self.send_action)

        layout.addWidget(header_label, 0, 0, 1, 3) 
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(self.name_label, 1, 1, 1, 2)
        layout.addWidget(query_button, 1, 3, 1, 1)
        
        layout.addWidget(subject_label, 2, 0, 1, 1)
        layout.addWidget(self.subject_label, 2, 1, 1, 2)
        
        layout.addWidget(score_label, 3, 0, 1, 1)
        layout.addWidget(self.score_label, 3, 1, 1, 2)
        layout.addWidget(add_button, 3, 3, 1, 1)
        layout.addWidget(send_button, 4, 4, 1, 2)

        layout.addWidget(self.result_label, 1, 4, 3, 7) 
        
        layout.setContentsMargins(10,10,10,10)
        for i in range(0,8,2):
            layout.setColumnStretch(i, 1)
        for i in range(6):
            layout.setRowStretch(i, 1)


        self.setLayout(layout)

    def subject_label_click_handler(self, event):
        event.ignore()

    def confirm_action(self):
        if not self.name_label.text().strip() or not self.subject_label.text().strip() or not self.score_label.text().strip():
            self.result_label.setText(f"Name, Subject and Score cannot be empty.")
        else:
            name = self.name_label.text()
            subject = self.subject_label.text()
            score = float(self.score_label.text())

            if name not in self.scores:
                self.scores[name] = {}
            self.scores[name][subject] = score

            self.result_label.setText(f"Name: {name},\nSubject: {subject},\nScore: {score}")
            self.service_ctrl.add(name, subject, score)

    def send_action(self):
        if not self.name_label.text().strip() or not self.scores:
            self.result_label.setText(f"Name, Subject and Score cannot be empty.")
        else:
            name = self.name_label.text()
            self.dataOut.emit({'name': name, 'scores': self.scores[name]})
            self.service_ctrl.send(name)
            
    def query_name(self):   
        if not self.name_label.text().strip():
            self.result_label.setText("Name cannot be empty.")
        else:
            name = self.name_label.text()
            response = self.service_ctrl.query(name)
            if response.get('status') == 'failed':
                self.result_label.setText(f"{name} does not exist")
                self.subject_label.setReadOnly(False)
                self.subject_label.mousePressEvent = lambda event: self.subject_label.clear()
                self.service_ctrl.query(name)
            else:
                self.result_label.setText(f"{name} does exist")
            
    def clear_editor_content(self, event):
        sender = self.sender()
        if isinstance(sender, LineEditComponent):
            sender.clear()
