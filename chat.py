import sys
import requests
from PyQt5 import QtWidgets as Qt
import time
from chat.thread import thread


class Example(Qt.QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        user, ok = Qt.QInputDialog.getText(self, 'Input Dialog',
                                           'Enter your name:')

        if ok and user != '':

            self.btn1 = Qt.QPushButton('Enter', self)
            self.inp = Qt.QLineEdit(self)
            self.out = Qt.QLabel(self)
            self.clear = Qt.QPushButton('Clear', self)

            self.btn1.clicked.connect(lambda: self.addMsg(self.inp, user))
            self.clear.clicked.connect(self.Clear)
            self.vueMsg(self.out)

            layout = Qt.QVBoxLayout()
            layout.addWidget(self.out)
            layout.addWidget(self.inp)
            layout.addWidget(self.btn1)
            layout.addWidget(self.clear)

            self.setLayout(layout)

            self.setGeometry(300, 300, 290, 350)
            self.setWindowTitle('USER: {}'.format(user))
            self.show()
        else:
            sys.exit()

    def addMsg(self, inp, user):
        if inp.text() != '':
            requests.post('http://127.0.0.1:5000', json={'user': user, 'message': inp.text()})
        inp.clear()

    def Clear(self):
        requests.delete('http://127.0.0.1:5000')

    @thread
    def vueMsg(self, out):
        while True:
            store = []

            b = requests.get('http://127.0.0.1:5000').json()
            for f in b['messages']:
                for j in b['user']:
                    if f['user'] == j['id']:
                        store.append('{}: {}'.format(j['user'], f['text']))

            out.setText('\n'.join(store))
            time.sleep(1)


if __name__ == '__main__':

    app = Qt.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
