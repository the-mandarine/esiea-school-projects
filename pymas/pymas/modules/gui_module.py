"""Description of the module goes here"""
import sys
from PyQt4 import QtGui, QtCore
from threading import Thread

# Is the module blocking or not ?
BLOCKING = True

# Beliefs that are impacted by this module
USEFUL_FOR = ['GUI']

# Commands we can send to this
COMMAND_RGX ='.*'

# Only the concerned beliefs are sent
# All desires are sent
# To create de new belief, you must generate a desire (see belief_creator.py)
def initialize(launcher):
    """Module initialisation"""
    log.debug("Running GUI")
    beliefs['friends'] = {}
    data.app = QtGui.QApplication(sys.argv)
    data.ex = GUI_main()
    data.app.exec()

def execute(cmd_string):
    """Execute the command string"""
    data.ex.addMonitorLine(cmd_string)

def stop():
    QtGui.QApplication.quit()

class GUI_main(QtGui.QMainWindow):
    def __init__(self):
        super(GUI_main,self).__init__()
        self.monitor = QtGui.QTabWidget()
        self.initUI()

    def initUI(self):
        self.setGeometry(300,300,800,800)
        self.setWindowTitle('PyMAS Management GUI')
        
        mainLayout = QtGui.QVBoxLayout()
        topLayout = QtGui.QHBoxLayout()
        buttonsLayout = QtGui.QGridLayout()

        agentListLayout = QtGui.QVBoxLayout()
        agentListLayout.addWidget(QtGui.QLabel("Agent List"))
        self.agentList = QtGui.QListWidget()
        agentListLayout.addWidget(self.agentList)
        self.getAgentList()
        self.refreshList = QtGui.QPushButton('Refresh')
        agentListLayout.addWidget(self.refreshList)
        topLayout.addLayout(agentListLayout)
        
        agentInfoLayout = QtGui.QVBoxLayout()
        agentInfoLayout.addWidget(QtGui.QLabel("Agent Information"))
        self.agentInfo = QtGui.QTextEdit()
        self.agentInfo.setReadOnly(True)
        agentInfoLayout.addWidget(self.agentInfo)
        topLayout.addLayout(agentInfoLayout)

        leftLayout = QtGui.QVBoxLayout()
        insideLayout = QtGui.QHBoxLayout()
        self.newIntentionValue = QtGui.QLineEdit()
        leftLayout.addWidget(QtGui.QLabel("Local Agent Controls"))
        insideLayout.addWidget(QtGui.QLabel('Add Intention'))
        insideLayout.addWidget(self.newIntentionValue)
        self.intentionButton = QtGui.QPushButton('Add Intention')
        leftLayout.addLayout(insideLayout)
        leftLayout.addWidget(self.intentionButton)
        leftLayout.addStretch()
        topLayout.addLayout(leftLayout)

        self.localMonitor = QtGui.QTextEdit()
        self.localMonitor.setReadOnly(True)
        self.monitor.addTab(self.localMonitor,"Local")
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(QtGui.QLabel('Monitor'))
        mainLayout.addWidget(self.monitor)
        

        self.intentionButton.clicked.connect(self.addIntention)
        self.refreshList.clicked.connect(self.getAgentList)
        self.agentList.itemClicked.connect(self.updateInfo)
        widget = QtGui.QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        self.show()

    def addMonitorLine(self,Msg):
        self.localMonitor.setHtml(self.localMonitor.toHtml()+'\n'+Msg)
    
    def getAgentList(self):
        self.agentList.clear()
        friends = beliefs['friends'].keys()
        if friends != None:
            for agt in friends:
                self.agentList.addItem(agt)
    def addIntention(self):
        if len(self.newIntentionValue.text())>0:
            command_queue.put_str(self.newIntentionValue.text())
            self.newIntentionValue.setText("")

    def updateInfo(self,item):
        friend = beliefs['friends'][item.text()]
        self.agentInfo.setText(str(friend))
