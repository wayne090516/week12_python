from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from client.ServiceController import ServiceController


class AddStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ServiceController()
        self.setObjectName("add_stu_widget")

        layout = QtWidgets.QGridLayout()

        # Header, Name and Query-button
        header_label = LabelComponent(20, "Add Student")
        content_label_name = LabelComponent(16, "Name: ")
        self.editor_label_name = LineEditComponent("Name")
        self.editor_label_name.mousePressEvent = self.editor_label_name.clear_editor_content
        self.editor_label_name.textChanged.connect(self.name_entered)

        self.button_query = ButtonComponent("Query")
        self.button_query.clicked.connect(self.query_pressed)
        self.button_query.disable()

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(content_label_name, 1, 0, 1, 1)
        layout.addWidget(self.editor_label_name, 1, 1, 1, 1)
        layout.addWidget(self.button_query, 1, 2, 1, 2)


        # Subject
        content_label_subject = LabelComponent(16, "Subject: ")
        self.editor_label_subject = LineEditComponent("Subject")
        self.editor_label_subject.mousePressEvent = self.editor_label_subject.clear_editor_content
        self.editor_label_subject.disable()

        layout.addWidget(content_label_subject, 2, 0, 1, 1)
        layout.addWidget(self.editor_label_subject, 2, 1, 1, 1)


        # Score and Add-button
        content_label_score = LabelComponent(16, "Score: ")
        self.editor_label_score = LineEditComponent("Score")
        self.editor_label_score.mousePressEvent = self.editor_label_score.clear_editor_content
        self.editor_label_score.disable()
        self.editor_label_score.setValidator(QtGui.QIntValidator())
        self.editor_label_score.textChanged.connect(self.score_entered)

        self.button_add = ButtonComponent("Add")
        self.button_add.clicked.connect(self.add_pressed)
        self.button_add.disable()

        layout.addWidget(content_label_score, 3, 0, 1, 1)
        layout.addWidget(self.editor_label_score, 3, 1, 1, 1)
        layout.addWidget(self.button_add, 3, 2, 1, 2)


        # Respond-window
        self.respond_window = LabelComponent(16, "", "color:red;")
        self.button_send = ButtonComponent("Send")
        self.button_send.clicked.connect(self.send_pressed)
        layout.addWidget(self.respond_window, 0, 4, 5, 1)
        layout.addWidget(self.button_send, 6, 4, 1, 1)
        self.button_send.disable()


        # Set Layout
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 4)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 2)
        layout.setRowStretch(4, 2)
        layout.setRowStretch(5, 2)
        layout.setRowStretch(6, 2)
        self.setLayout(layout)


    def query_pressed(self):
        self.button_query.disable()

        self.controller.query_signal.connect(self.get_server_query)
        self.controller.query_stu(self.editor_label_name.text())

    def get_server_query(self, status):
        if status == "Fail":
            self.editor_label_name.disable()
            self.editor_label_subject.enable()
            self.editor_label_score.enable()
        elif status == "OK":
            self.editor_label_name.setText("Name")

    def add_pressed(self):
        if (self.editor_label_name.text()=="" or self.editor_label_subject.text()=="" or self.editor_label_score.text()==""):
            self.respond_window.setText("Please enter the subject and score for the student")
        else:
            self.button_send.enable()
            self.add_dict={self.editor_label_subject.text():self.editor_label_score.text()}
            self.respond_window.setText(f"Student {str(self.editor_label_name.text())}'s "
                                        + f"subject '{str(self.editor_label_subject.text())}' "
                                        + f"with score '{str(self.editor_label_score.text())}' added")

    def send_pressed(self):
        if (self.editor_label_name.text() ==""or self.editor_label_subject.text() =="" or self.editor_label_score.text() ==""):
            self.respond_window.setText("Please enter the subject and score for the student")
        else:
            self.parameters = {'name': self.editor_label_name.text(), 
                            'scores': {self.editor_label_subject.text():self.editor_label_score.text()}}
            
            self.controller.send_signal.connect(self.get_server_add)
            self.controller.send_stu(self.parameters)

    def get_server_add(self, status):
        if status == "Fail":
            self.respond_window.setText("Add " + str(self.parameters) + " failed!")
        elif status == "OK":
            self.respond_window.setText("Add " + str(self.parameters) + " successfully!")

            self.editor_label_name.setText("Name")
            self.editor_label_subject.setText("Subject")
            self.editor_label_score.setText("Score")
            self.editor_label_subject.disable()
            self.editor_label_score.disable()
            self.editor_label_name.enable()
            self.button_query.disable()
            self.button_add.disable()

    def name_entered(self):
        if self.editor_label_name.text() != "":
            self.button_query.enable()
    
    def score_entered(self):
        if self.editor_label_score.text() != "":
            self.button_add.enable()
