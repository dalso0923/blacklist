"""
회사로 악성메일 유입시, 차단해야할 IP와 네트워크 대역대, 도메인을 입력함
입력된 대상의 형식에 맞추어 차단 리스트 파일을 만들어 저장함
저장 위치는 사용자가 정할 수 있고, 파일이름은 '대상_저장날짜_저장시간'으로 고정
사용자는 파일을 각 방화벽으로 업로드하면 차단 객체 생성을 할 수 있음

명명규칙 ::
함수 - '동작_대상', 모두 소문자, 두개의 단어는 '_'로 구분


author  soae0923@gmail.com
version 1.0, 20/08/18
since   python3.8.5
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from common_module.in_out import InputModule
from black.black_domain import BlackDomain
from black.black_ip import BlackIP
from black.black_network import BlackNetwork

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Blacklist')
        self.setWindowIcon(QIcon('E:/leesa/blacklist/cat.png'))
        font = QFont()
        font.setFamily("나눔스퀘어")
        #stylesheet 적용하는법 찾아보기

        #===========1행 [차단 대상 선택하기] ===========#
        """
        IP, Network, Domain 중 차단 대상을 선택한다
        """

        label_obj = QLabel("차단대상")
        label_obj.setFont(font)
        self.cmb_obj = QComboBox(self)
        self.cmb_obj.addItem('IP')
        self.cmb_obj.addItem('Network')
        self.cmb_obj.addItem('Domain')
        self.cmb_obj.setFont(font)
        self.cmb_obj.setStyleSheet("background-color: #FFFFFF;")

        box_obj = QHBoxLayout()
        box_obj.addWidget(label_obj)
        box_obj.addWidget(self.cmb_obj)
        box_obj.setContentsMargins(10, 10, 10, 10)

        # ===========2행 [차단 대상 입력하기] ===========#
        """
        입련란에 차단 IP, Domain을 입력하고
        '입력'버튼을 눌러서
        확인란에서 제대로 입력되었는지 확인한다
        제대로 입력이 되지 않았을 경우
        '재입력'버튼을 눌러서 다시 입력한다
        """
        ## [2행 1열 : 입력란]

        label_input = QLabel("입력")
        label_input.setFont(font)
        self.text_input = QTextEdit(self)
        # text_input.setAcceptRichText(False)
        self.text_input.setPlaceholderText("2개 이상일 경우 (,)로 구분하여 입력하세요")
        self.text_input.setStyleSheet("background-color: #FFFFFF;")
        self.text_input.setFont(font)

        box_input = QVBoxLayout()
        box_input.addWidget(label_input)
        box_input.addWidget(self.text_input)

        ## [2행 2열 : 버튼]
        btn_input = QPushButton('입력', self)
        btn_del = QPushButton('재입력', self)
        btn_input.setFont(font)
        btn_input.setStyleSheet("background-color: #c9d6de")
        btn_del.setFont(font)
        btn_del.setStyleSheet("background-color: #c9d6de")
        # btn_del.setStyleSheet("background-color: #FADAD8")

        box_btn = QVBoxLayout()
        box_btn.addWidget(btn_input)
        box_btn.addWidget(btn_del)

        btn_input.clicked.connect(self.input_data)
        btn_del.clicked.connect(self.del_data)

        ##[2행 3열 : 확인란]
        label_chk = QLabel("확인")
        label_chk.setFont(font)
        self.text_chk = QTextEdit(self) #scroll
        self.text_chk.setReadOnly(True) #selectable 복사 가능
        self.text_chk.setStyleSheet("background-color: #FFFFFF;")
        self.text_chk.setFont(font)

        box_chk = QVBoxLayout()
        box_chk.addWidget(label_chk)
        box_chk.addWidget(self.text_chk)

        ## [2행 레이아웃 ]

        box_data = QHBoxLayout()
        box_data.addLayout(box_input)
        box_data.addLayout(box_btn)
        box_btn.setContentsMargins(10, 0, 10, 0)
        box_data.addLayout(box_chk)
        box_data.setContentsMargins(10, 10, 10, 10)

        # ===========3행 [저장경로] ===========#
        """
        '찾아보기'버튼을 눌러
        저장경로를 설정한다
        설정이 완료된 경우, '저장'버튼을 눌러서 보고서를 저장
        """

        label_path = QLabel("저장경로")
        label_path.setFont(font)
        self.text_path = QLineEdit(self)
        self.text_path.setFont(font)
        self.text_path.setStyleSheet("background-color: #FFFFFF;")

        btn_path = QPushButton('찾아보기', self)
        btn_path.setFont(font)
        btn_path.setStyleSheet("background-color: #c9d6de")
        btn_save = QPushButton('저장', self)
        btn_save.setFont(font)
        btn_save.setStyleSheet("background-color: #c9d6de")

        box_path = QHBoxLayout()
        box_path.addWidget(label_path)
        box_path.addWidget(self.text_path)
        box_path.addWidget(btn_path)
        box_path.addWidget(btn_save)
        box_path.setContentsMargins(10, 10, 10, 10)

        btn_path.clicked.connect(self.make_path)
        btn_save.clicked.connect(self.save_report)

        ### =========== [레이아웃 추가] =========== ###

        layout = QVBoxLayout()
        layout.addLayout(box_obj)
        layout.addLayout(box_data)
        layout.addLayout(box_path)

        ### =========== [레이아웃 스타일] =========== ###
        self.setStyleSheet("background-color: #f4f5f9")
        layout.setContentsMargins(15, 15, 15, 15)

        label_obj.adjustSize()
        self.setLayout(layout)
        self.show()

    def input_data(self):
        """
        '입력'버튼을 누르면 입력란의 데이터를 리스트화하여 확인란에 출력한다
        """
        print(self.text_input.toPlainText())
        self.list = InputModule(self.text_input.toPlainText())
        self.text_chk.setPlainText(str(self.list.data_set))

    def del_data(self):
        """
        '재입력'버튼을 누르면 확인란과 입련란의 데이터를 모두 정리한다
        """
        self.text_chk.clear()
        self.text_input.clear()

    def make_path(self):
        """
        '찾아보기'버튼을 누르면 저장경로를 설정할 수 있게 한다
        """
        self.dir = QFileDialog.getExistingDirectory(self, str("Open Directory"))
        self.text_path.setText(self.dir)

    def save_report(self):
        """
        '저장'버튼을 누르면 보고서를 출력하도록 한다
        """
        #콤보박스의 결과에 따라서 객체 생성이 달라짐
        #[0]일 경우, black_ip 객체 생성
        #[1]일 경우, black_network 객체 생성
        #[2]일 경우, black_domain 객체 생성
        self.idx_obj = self.cmb_obj.currentIndex() #(0~2)
        self.name_obj = self.cmb_obj.currentText() #IP, Network, Domain

        if self.idx_obj == 0:
            output_ip = BlackIP(self.list.data_set)
            output_ip.make_report_ip(self.dir, self.name_obj)
        elif self.idx_obj == 1:
            output_net = BlackNetwork(self.list.data_set)
            output_net.slicing_net()
            output_net.make_report_network(self.dir, self.name_obj)
        elif self.idx_obj == 2:
            output_dom = BlackDomain(self.list.data_set)
            output_dom.ns_lookup()
            output_dom.slicing_domain()
            output_dom.make_report_domain(self.dir, self.name_obj)

        msg_box = QMessageBox.question(self, 'Message', '저장이 완료되었습니다. \n프로그램을 종료하시겠습니까?',
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if msg_box == QMessageBox.Yes:
            sys.exit()
        else:
            self.text_chk.clear()
            self.text_input.clear()
            self.text_path.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())