from PyQt5.QtWidgets import (QDialog, QAction, QApplication, QLabel, QGridLayout,
                             QLineEdit, QMenuBar, QPushButton)


class FrontPanel(QDialog):
    """This is FiledSensor test program front panel class"""

    def __init__(self):
        super().__init__()
        # GroupBox Initialization
        self.mainlayout = QGridLayout()   # basicinfo layout

        self.names = []
        self.menuBar = QMenuBar()
        # PushButton Initialization
        self.BeginTestButton = QPushButton('开始测试')
        self.CancelTestButton = QPushButton('取消测试')
        self.PauseTestButton = QPushButton('暂停测试')
        self.SaveBasicinfoButton = QPushButton('保存基本信息')

        self.initUI()

    def initUI(self):
        """initialise the UI"""
        self.BasicinfoList()
        self.ButtonList()
        self.CreateMenu()
        self.StretchSet()

        self.mainlayout.addWidget(self.SaveBasicinfoButton, 12, 0, 1, 2)
        self.mainlayout.setMenuBar(self.menuBar)

        self.setLayout(self.mainlayout)

        self.setGeometry(300, 100, 900, 700)  # 设置窗口位置大小
        self.setWindowTitle('FieldSensor')

        self.show()

    def CreateMenu(self):
        """create the menu"""
        file_menu = self.menuBar.addMenu('&File')

        open_action = QAction('&打开', self)
        exit_action = QAction('&退出', self)

        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)

        exit_action.triggered.connect(self.accept)

    def ButtonList(self):

        names = [self.BeginTestButton, self.CancelTestButton,
                 self.PauseTestButton]

        for i in range(3):
            self.mainlayout.addWidget(names[i], i + 4, 4)

    def BasicinfoList(self):
        """basicinfo layout set"""

        certificate_num_label = QLabel('证书编号')
        certificate_serial_label = QLabel('证书序列号')
        manufacturer_label = QLabel('生产厂家')
        device_name_label = QLabel('设备名称')
        custom_address_label = QLabel('客户地址')
        custom_name_label = QLabel('客户名称')
        calibration_address_label = QLabel('校准地点')
        temperature_label = QLabel('温    度')
        humidity_label = QLabel('湿    度')
        tester_label = QLabel('测试人员')
        date_label = QLabel('测试日期')
        # LineEdit Initialization
        certificatenumber = QLineEdit()
        certificateserial = QLineEdit()
        manufacturer = QLineEdit()
        devicename = QLineEdit()
        customaddress = QLineEdit()
        customname = QLineEdit()
        calibrationaddress = QLineEdit()
        temperature = QLineEdit()
        humidity = QLineEdit()
        tester = QLineEdit()
        date = QLineEdit()

        self.names = [certificate_num_label, certificatenumber,
                 certificate_serial_label, certificateserial,
                 manufacturer_label, manufacturer,
                 device_name_label, devicename,
                 custom_address_label, customaddress,
                 custom_name_label, customname,
                 calibration_address_label, calibrationaddress,
                 temperature_label, temperature,
                 humidity_label, humidity,
                 tester_label, tester,
                 date_label, date]

        for i in range(22):
            if i % 2 == 0:
                self.mainlayout.addWidget(self.names[i], i / 2, 0)
            else:
                self.mainlayout.addWidget(self.names[i], (i - 1) / 2, 1)

    def StretchSet(self):
        # set column stretch
        self.mainlayout.setColumnStretch(0, 0.5)
        self.mainlayout.setColumnStretch(1, 2)
        self.mainlayout.setColumnStretch(2, 1)
        self.mainlayout.setColumnStretch(3, 1)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    front_panel = FrontPanel()
    sys.exit(app.exec_())
