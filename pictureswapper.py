# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'base.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import functools
import random
import time
import sqlite3
import datetime

class Ui_pictureSwapper(object):
    def setupUi(self, pictureSwapper):

        self.stylesheet = """

            QMainWindow{
                background-color: black;
                color: red;
            }
            QDialog {
                background-color: black;
                color: red;
            }
            QPushButton{
                height: 100%;
                width: 100%;
                background-color: red;
                color: #fff;
            }
            QLabel {
                color: red;
            }
            QAction {
                background-color: black;
            }
            QMenu {
                background-color: black;
                color: red;
            }

        """
        self.difficulty = []
        self.clicks = 0
        self.matchup  = 0
        rows = 4
        columns = 4
        matches = int(( rows * columns )/2)
        self.difficulty.append({"difficulty": "Easy","rows": rows, "columns": columns,"matches": matches})
        rows = 4
        columns = 8
        matches = int(( rows * columns )/2)
        self.difficulty.append({"difficulty": "Normal","rows": rows, "columns": columns,"matches": matches})
        rows = 6
        columns = 8
        matches = int(( rows * columns )/2)
        self.difficulty.append({"difficulty": "Hard","rows": rows, "columns": columns,"matches": matches})

        self.diff = self.difficulty[0]["difficulty"]
        self.rows = self.difficulty[0]['rows']
        self.columns = self.difficulty[0]['columns']
        self.matches = self.difficulty[0]['matches']

        self.open = []
        self.holders = []
        self.defaultIcon = QtGui.QIcon("images/default.png")
        self.rmcologo = QtGui.QIcon("images/rmcologo.png")
        self.connect_db()
        self.create_table()

        self.defaultIcon.actualSize(QtCore.QSize(100, 100))


        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/rmcologo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        pictureSwapper.setWindowIcon(icon)


        pictureSwapper.setStyleSheet(self.stylesheet)
        pictureSwapper.setObjectName("pictureSwapper")
        pictureSwapper.resize(625, 600)
        self.centralwidget = QtWidgets.QWidget(pictureSwapper)

        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.centralwidget.setStyleSheet(self.stylesheet)
        pictureSwapper.setCentralWidget(self.centralwidget)
        self.menu(pictureSwapper)
        self.scoreboard()
        self.swapper(pictureSwapper, self.gridLayout)


    def scoreboard(self):
        font = QtGui.QFont()
        font.setFamily("DS-Digital")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        goal = QtWidgets.QLabel("GOAL: ")
        goal.setFont(font)
        self.goal_lbl = QtWidgets.QLabel(str(self.matches))
        self.goal_lbl.setFont(font)
        matched = QtWidgets.QLabel(" MATCHED: ")
        matched.setFont(font)
        self.matched_lbl = QtWidgets.QLabel(str(self.matchup))
        self.matched_lbl.setFont(font)
        clicks = QtWidgets.QLabel(" CLICKS: ")
        clicks.setFont(font)
        self.clicks_lbl = QtWidgets.QLabel(str(self.clicks))
        self.clicks_lbl.setFont(font)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(goal)
        layout.addWidget(self.goal_lbl)
        layout.addWidget(matched)
        layout.addWidget(self.matched_lbl)
        layout.addWidget(clicks)
        layout.addWidget(self.clicks_lbl)
        self.gridLayout_2.addLayout(layout, 0,0,1,1)

    def connect_db(self):
        try:
            self.conn = sqlite3.connect("PictureSwapper.db")
            self.cursor = self.conn.cursor()
        except ValueError as e:
            print(e)

    def menu(self, pictureSwapper):
        self.menubar = QtWidgets.QMenuBar(pictureSwapper)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 625, 26))
        self.menubar.setObjectName("menubar")
        self.menuMENU = QtWidgets.QMenu(self.menubar)
        self.menuMENU.setObjectName("menuMENU")
        pictureSwapper.setMenuBar(self.menubar)
        self.actionNEW_GAME = QtWidgets.QAction(pictureSwapper)
        self.actionNEW_GAME.setObjectName("actionNEW_GAME")
        self.actionNEW_GAME.triggered.connect(functools.partial(self.new_game_dialog))
        self.actionHighscore = QtWidgets.QAction(pictureSwapper)
        self.actionHighscore.setObjectName("actionHighscore")
        self.actionHighscore.triggered.connect(self.view_highscore)
        self.actionAbout = QtWidgets.QAction(pictureSwapper)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.triggered.connect(self.aboutMessage)
        self.actionExit = QtWidgets.QAction(pictureSwapper)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.triggered.connect(self.closeFun)
        self.menuMENU.addAction(self.actionNEW_GAME)
        self.menuMENU.addAction(self.actionHighscore)
        self.menuMENU.addSeparator()
        self.menuMENU.addAction(self.actionAbout)
        self.menuMENU.addSeparator()
        self.menuMENU.addAction(self.actionExit)
        self.menubar.addAction(self.menuMENU.menuAction())

        self.retranslateUi(pictureSwapper)
        QtCore.QMetaObject.connectSlotsByName(pictureSwapper)

    def create_table(self):
        try:
            self.cursor.execute("CREATE TABLE highscores (name TEXT, difficulty TEXT,score INT, time DATETIME)")
        except:
            pass

    def swapper(self, pictureSwapper, grid):
        x = self.rows
        y = self.columns
        self.clicks = 0
        self.matchup  = 0
        self.clicks_lbl.setText(str(self.clicks))
        self.matched_lbl.setText(str(self.matchup))
        self.goal_lbl.setText(str(self.matches))
        self.swapperBtn = []
        for x1 in range(x):
            self.swapperBtn.append([])
            for y1 in range(y):
                self.swapperBtn[x1].append(QtWidgets.QPushButton(pictureSwapper))
                self.swapperBtn[x1][y1].clicked.connect(functools.partial(self.me, x1, y1))
                self.swapperBtn[x1][y1].setFixedSize(QtCore.QSize(100,100))
                self.swapperBtn[x1][y1].setIcon(self.defaultIcon)
                self.swapperBtn[x1][y1].setIconSize(QtCore.QSize(100,100))
                grid.addWidget(self.swapperBtn[x1][y1], x1, y1, 1, 1)

        self.images = []
        for i in range(self.matches):
            self.images.append([i+1, 0])

        self.open = []
        self.holders = []
        for x1 in range(x):
            for y1 in range(y):
                self.set_images(x1,y1)

    def set_images(self,x,y):
        image = random.randint(1, self.matches)
        if self.images[image-1][1] < 2:
        	icon = str(image)
        	self.holders.append([icon,x,y])
        	self.images[image-1][1] += 1
        else:
            self.set_images(x,y)

    def me(self, x, y):
        z = x + y*self.rows
        if len(self.open) < 2:
            if (len(self.open) == 1 and self.open[0][0] != z) or len(self.open) == 0:
                self.clicks += 1
                self.clicks_lbl.setText(str(self.clicks))
                if(self.clicks == 1):
                    self.time = int(time.time())
                im = self.holders[z]
                self.swapperBtn[x][y].setIcon(QtGui.QIcon("images/"+str(im[0])+".jpg"))
                self.open.append([z,x,y])
                self.check()


    def matchup_func(self):
        if self.matches == self.matchup:
            self.restart()

    def check(self):
        if len(self.open) > 1:
            if self.holders[self.open[0][0]][0] == self.holders[self.open[1][0]][0]:
                self.matchup += 1
                self.matched_lbl.setText(str(self.matchup))
                self.match()
                self.open = []
            else:
                QtCore.QTimer.singleShot(1000,self.setdefault)

    def match(self):
        z1, x1,y1 = self.open[0]
        z2, x2,y2 = self.open[1]
        self.swapperBtn[x1][y1].setDisabled(True)
        self.swapperBtn[x2][y2].setDisabled(True)
        self.matchup_func()

    def setdefault(self):
        z1, x1,y1 = self.open[0]
        z2, x2,y2 = self.open[1]
        self.swapperBtn[x1][y1].setIcon(self.defaultIcon)
        self.swapperBtn[x2][y2].setIcon(self.defaultIcon)
        self.open = []

    def restart(self):
        self.score = self.gen_scores()
        self.final_clicks = self.clicks
        self.restart_dialog = QtWidgets.QDialog()
        self.restart_dialog.setStyleSheet(self.stylesheet)
        self.restart_dialog.resize(400, 300)
        grid = QtWidgets.QGridLayout(self.restart_dialog)
        label = QtWidgets.QLabel()
        label.setText("Victory!!!")
        label.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(label,0,0,1,2)
        label2 = QtWidgets.QLabel()
        label2.setText("Add highscore")
        label2.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(label2,1,0,1,2)
        label3 = QtWidgets.QLabel()
        label3.setText("Name")
        label3.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(label3,2,0,1,1)
        self.name = QtWidgets.QLineEdit()
        grid.addWidget(self.name,2,1,1,1)
        restart = QtWidgets.QPushButton()
        restart.setText("ENTER")
        restart.clicked.connect(self.restart_func)
        grid.addWidget(restart,3,0,1,2)
        grid.setAlignment(QtCore.Qt.AlignCenter)
        self.restart_dialog.exec_()

    def add_highscore(self):
        date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
        name = self.name.text()
        self.cursor.execute("INSERT INTO highscores (name, difficulty, score, time, clicks) VALUES (?,?,?,?,?)",
                (self.name.text(), self.diff, int(self.score), date, self.final_clicks))
        self.conn.commit()

    def gen_scores(self):
        myscore = (self.rows * self.columns) * self.matches
        timer = int(time.time()) - self.time
        ratio = self.matches/self.clicks
        final = myscore + (myscore/timer) + (myscore * ratio)
        return final


    def view_highscore(self):
        self.scores = QtWidgets.QDialog()
        self.scores.setStyleSheet(self.stylesheet)
        grid = QtWidgets.QGridLayout(self.scores)
        highscore_lbl = QtWidgets.QLabel()
        highscore_lbl.setText("Highscores")
        highscore_lbl.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(highscore_lbl,0,0,1,5)
        name_lbl = QtWidgets.QLabel()
        name_lbl.setText("Name")
        name_lbl.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(name_lbl,1,0,1,1)
        difficulty_lbl = QtWidgets.QLabel()
        difficulty_lbl.setText("Difficulty")
        difficulty_lbl.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(difficulty_lbl,1,1,1,1)
        score_lbl = QtWidgets.QLabel()
        score_lbl.setText("Score")
        score_lbl.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(score_lbl,1,2,1,1)
        time_lbl = QtWidgets.QLabel()
        time_lbl.setText("Time")
        time_lbl.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(time_lbl,1,3,1,1)
        click_lbl = QtWidgets.QLabel()
        click_lbl.setText("Clicks")
        click_lbl.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(click_lbl,1,4,1,1)
        try:
            sql = "SELECT * FROM highscores ORDER BY score DESC LIMIT 10"
            x = 2
            for row in self.cursor.execute(sql):
                grid.addWidget(QtWidgets.QLabel(str(row[0])),x,0,1,1)
                grid.addWidget(QtWidgets.QLabel(str(row[1])),x,1,1,1)
                grid.addWidget(QtWidgets.QLabel(str(int(row[2]))),x,2,1,1)
                grid.addWidget(QtWidgets.QLabel(str(row[3])),x,3,1,1)
                grid.addWidget(QtWidgets.QLabel(str(row[4])),x,4,1,1)
                x+=1
        except ValueError as e:
            pass
        closeBtn = QtWidgets.QPushButton()
        closeBtn.setText("Close")
        closeBtn.clicked.connect(self.close_highscore)
        grid.addWidget(closeBtn,x,1,1,3)
        self.scores.exec_()

    def close_highscore(self):
        self.scores.close()
    def restart_func(self):
        self.add_highscore()
        self.swapper(pictureSwapper, self.gridLayout)
        self.restart_dialog.close()

    def new_game_dialog(self):
        self.new_dialog = QtWidgets.QDialog()
        self.new_dialog.setStyleSheet(self.stylesheet)
        self.new_dialog.resize(400, 300)
        grid = QtWidgets.QGridLayout(self.new_dialog)
        label = QtWidgets.QLabel()
        label.setText("Start a New Game")
        label.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(label,0,0,3,1)
        x = 0
        gameButtons = []
        for i in self.difficulty:
            gameButtons.append(QtWidgets.QPushButton())
            gameButtons[x].setText(i['difficulty'])
            gameButtons[x].clicked.connect(functools.partial(self.new_game, i))
            grid.addWidget(gameButtons[x], 1, x, 1, 1)
            x += 1
        self.new_dialog.exec_()

    def new_game(self, difficulty):
        self.new_dialog.close()
        self.diff = difficulty["difficulty"]
        self.rows = difficulty['rows']
        self.columns = difficulty['columns']
        self.matches = difficulty['matches']
        self.swapper(pictureSwapper, self.gridLayout)

    def aboutMessage(self):
        body = QtWidgets.QDialog()
        body.setStyleSheet(self.stylesheet)
        body.resize(400, 300)
        body.setWindowTitle("About Us")
        grid = QtWidgets.QVBoxLayout(body)

        image = QtGui.QPixmap("images/rmcologo.png")
        newimage = image.scaled(QtCore.QSize(300,200), QtCore.Qt.KeepAspectRatio)
        photoholder = QtWidgets.QLabel(body)
        photoholder.setText("")
        photoholder.setAlignment(QtCore.Qt.AlignCenter)
        photoholder.setPixmap(image)
        grid.addWidget(photoholder, 1)
        label = QtWidgets.QLabel(body)
        label.setText("PictureSwapper Powered by RMCO")
        label.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(label)
        body.exec_()

    def retranslateUi(self, pictureSwapper):
        _translate = QtCore.QCoreApplication.translate
        pictureSwapper.setWindowTitle(_translate("pictureSwapper", "Picture Swapper"))
        self.menuMENU.setTitle(_translate("pictureSwapper", "FILE"))
        self.actionNEW_GAME.setText(_translate("pictureSwapper", "New Game"))
        self.actionHighscore.setText(_translate("pictureSwapper", "Highscore"))
        self.actionAbout.setText(_translate("pictureSwapper", "About"))
        self.actionExit.setText(_translate("pictureSwapper", "Exit"))


    def closeFun(self):
        sys.exit(app.exec_())

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    pictureSwapper = QtWidgets.QMainWindow()
    ui = Ui_pictureSwapper()
    ui.setupUi(pictureSwapper)
    pictureSwapper.show()
    sys.exit(app.exec_())
