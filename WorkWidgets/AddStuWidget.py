from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from client.client_command.ServiceControl import ServiceControl

class AddStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("add_stu_widget")
        self.int_ui()

    def int_ui(self):
        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(19, "Add Student")
        content_label_name = LabelComponent(16, "Name: ")
        content_label_subject = LabelComponent(16, "Subject: ")
        content_label_score = LabelComponent(16, "Score: ")
        self.content_label_response = LabelComponent(16, "", "color:red;")

        self.editor_label_name = LineEditComponent("Name")
        self.editor_label_subject = LineEditComponent("Subject")
        self.editor_label_score = LineEditComponent()
        self.editor_label_score.setValidator(QtGui.QIntValidator())
        self.editor_label_name.mousePressEvent = self.editor_label_name.clear_editor_content
        self.editor_label_subject.mousePressEvent = self.editor_label_subject.clear_editor_content
        self.editor_label_name.textChanged.connect(self.name_inputed)
        self.editor_label_score.textChanged.connect(self.score_inputed)
        self.editor_label_subject.setEnabled(False)
        self.editor_label_score.setEnabled(False)

        self.button_query = ButtonComponent("Query")
        self.button_add = ButtonComponent("Add")
        self.button_send = ButtonComponent("Send")
        self.button_query.clicked.connect(self.query)
        self.button_add.clicked.connect(self.add)
        self.button_send.clicked.connect(self.send)
        self.button_query.setEnabled(False)
        self.button_add.setEnabled(False)        

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(self.content_label_response, 0, 4, 5, 1)
        layout.addWidget(content_label_name, 1, 0, 1, 1)
        layout.addWidget(content_label_subject, 2, 0, 1, 1)
        layout.addWidget(content_label_score, 3, 0, 1, 1)
        layout.addWidget(self.editor_label_name, 1, 1, 1, 1)
        layout.addWidget(self.editor_label_subject, 2, 1, 1, 1)
        layout.addWidget(self.editor_label_score, 3, 1, 1, 1)
        layout.addWidget(self.button_query, 1, 2, 1, 1)
        layout.addWidget(self.button_add, 3, 2, 1, 1)
        layout.addWidget(self.button_send, 6, 3, 1, 2)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 3)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 3)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 2)
        layout.setRowStretch(4, 2)
        layout.setRowStretch(5, 2)
        layout.setRowStretch(6, 2)

        self.setLayout(layout)
        self.ServiceControl = ServiceControl()

    def name_inputed(self):
        self.button_query.setEnabled(bool(self.editor_label_name.text()))

    def score_inputed(self):
        self.button_add.setEnabled(bool(self.editor_label_score.text()))

    def query(self):
        name = self.editor_label_name.text()
        self.ServiceControl.query_signal.connect(self.query_result)
        self.ServiceControl.query(name)
    
    def query_result(self,response):
        if response["status"]=="Fail":
            self.editor_label_subject.setEnabled(True)
            self.editor_label_score.setEnabled(True)
        else:
            self.content_label_response.setText(f"The name is already exist.")

    def add(self):
        subject = self.editor_label_subject.text()
        score = self.editor_label_score.text()
        if not subject or subject == "Subject" or not score:
            self.content_label_response.setText("Please input valid data.")
            return
        self.ServiceControl.add_signal.connect(self.add_result)
        self.ServiceControl.add(subject, score)
            
    def add_result(self, response):
        if response["status"] == "OK":
            message = response.get("parameters", "error")
            self.content_label_response.setText(f"Add student info: {message}")
        else:
            reason = response.get("reason", "Unknown error")
            self.content_label_response.setText(f"Add operation failed: {reason}")

    def send(self):
        if not self.validate_inputs():
            return
        self.ServiceControl.send_signal.connect(self.send_result)
        self.ServiceControl.send(self.editor_label_name.text())
        
    def send_result(self,response):
        if response['status'] == "OK":
            self.editor_label_name.setText("Name")
            self.editor_label_subject.setText("Subject")
            self.editor_label_score.setText("")
            self.editor_label_subject.setEnabled(False)
            self.editor_label_score.setEnabled(False)
            self.button_query.setEnabled(False)
            self.button_add.setEnabled(False)
            message = response.get("parameters", {})
            name = message.get("name", "Unknown")
            scores = message.get("scores", {})
            subject = ", ".join([f"{key}: {value}" for key, value in scores.items()])
            self.content_label_response.setText(f"The student {name}'s subject {subject} added.")
        else:
             self.content_label_response.setText("Fail to add student.")
    
    def validate_inputs(self):
        name = self.editor_label_name.text()
        subject = self.editor_label_subject.text()
        score = self.editor_label_score.text()
        if not name or not subject or not score:
            self.content_label_response.setText("Please fill in all fields.")
            return False
        return True