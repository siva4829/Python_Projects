import sys
import random
from PyQt5.QtWidgets import QMainWindow,QWidget,QLabel,QGridLayout,QPushButton,QApplication,QHBoxLayout,QVBoxLayout,QStackedWidget
from PyQt5.QtCore import Qt


class mainwindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tic Tac Toe")
        self.resize(300, 400)

        self.stack = QStackedWidget()

        self.game = tic_tac_toe(self.stack)
        self.menu = main(self.stack, self.game)

        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.game)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)


class main(QWidget):
    def __init__(self, stack, game):
        super().__init__()

        self.stack = stack
        self.game = game

        game_label = QLabel("Tic Tac Toe")
        game_label.setAlignment(Qt.AlignCenter)

        btn1 = QPushButton("Player Vs Player")
        btn2 = QPushButton("Player Vs Computer")

        grid_layout = QGridLayout()
        grid_layout.addWidget(btn1, 0, 0)
        grid_layout.addWidget(btn2, 0, 1)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(game_label)
        layout.addSpacing(30)
        layout.addLayout(grid_layout)
        layout.addStretch()

        self.setLayout(layout)
        btn1.clicked.connect(self.start_pvp)
        btn2.clicked.connect(self.start_pvc)

        self.setStyleSheet("""
                QWidget {
                    background-color: #f2f2f2;
                }

                /* Title */
                QLabel {
                    font-size: 28px;
                    font-weight: bold;
                    color: #222;
                }

                /* Buttons */
                QPushButton {
                    background-color: #1e3a8a;
                    color: white;
                    padding: 10px;
                    border-radius: 8px;
                    min-width: 180px;
                    margin: 20px;
                }

                QPushButton:hover {
                    background-color: #274bb5;
                }
                """)

    def start_pvp(self):
        self.game.mode = "pvp"
        self.stack.setCurrentWidget(self.game)

    def start_pvc(self):
        self.game.mode = "pvc"
        self.stack.setCurrentWidget(self.game)


    def set_mode(self, mode):
        self.mode = mode
        print(mode)
        self.stack.setCurrentWidget(self.game)

class tic_tac_toe(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.mode="pvp"
        self.setWindowTitle("Tic Tac Toe")
        self.setGeometry(50,20,300,400)

        self.button1 = QPushButton()
        self.button2 = QPushButton()
        self.button3 = QPushButton()
        self.button4 = QPushButton()
        self.button5 = QPushButton()
        self.button6 = QPushButton()
        self.button7 = QPushButton()
        self.button8 = QPushButton()
        self.button9 = QPushButton()

        self.reset_button = QPushButton("Reset Game")
        self.back = QPushButton("Back")

        self.game_name = QLabel("Tic Tac Toe")
        self.game_status = QLabel()
        self.player1 = QLabel("Player 1 : X")
        self.player2 = QLabel("Player 2 : O")

        self.current_player = 'X'
        self.game_over = False
        self.track = 0

        self.initUI()
        self.button_function()

    def initUI(self):
        self.game_name.setAlignment(Qt.AlignHCenter)
        self.game_status.setAlignment(Qt.AlignHCenter)
        self.game_status.setObjectName("game_status")

        self.player1.setAlignment(Qt.AlignHCenter)
        self.player1.setObjectName("player1")

        self.player2.setAlignment(Qt.AlignHCenter)
        self.player2.setObjectName("player2")

        # Title layout (UNCHANGED)
        title_layout = QVBoxLayout()
        title_layout.addWidget(self.game_name)
        title_layout.addWidget(self.game_status)
        title_layout.addWidget(self.player1)
        title_layout.addWidget(self.player2)

        # Grid layout (UNCHANGED)
        self.grid = QGridLayout()
        self.grid.addWidget(self.button1,0,0)
        self.grid.addWidget(self.button2,0,1)
        self.grid.addWidget(self.button3,0,2)
        self.grid.addWidget(self.button4,1,0)
        self.grid.addWidget(self.button5,1,1)
        self.grid.addWidget(self.button6,1,2)
        self.grid.addWidget(self.button7,2,0)
        self.grid.addWidget(self.button8,2,1)
        self.grid.addWidget(self.button9,2,2)

        self.grid.setSpacing(0)

        # Main layout (same structure)
        main_layout = QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addLayout(self.grid)
        main_layout.addWidget(self.reset_button)
        # Back button (no new stack!)
        main_layout.addWidget(self.back)
        main_layout.setSpacing(0)


        self.setLayout(main_layout)

        # Style (UNCHANGED)
        self.setStyleSheet("""
        *{
        background-color:black;
        }
        QPushButton {
        height: 80px;
        width: 80px;
        border:3px solid brown;
        color:white;
        font-size:30px;
        }
        QLabel {
        color:red;
        font-size:50px;
        font-weight:bold;
        font-style:italic;
        font-family:Arial,serif;
        }
        #game_status {
        color:blue;
        }
        #player1 {
        font-size:30px;
        color:green;
        }
        #player2 {
        font-size:30px;
        color:green;
        }
        """)

    def button_function(self):
        self.reset_button.clicked.connect(self.reset_game)
        self.back.clicked.connect(self.go_back)

        if not self.game_over:
            for btn in [self.button1, self.button2, self.button3,
                        self.button4, self.button5, self.button6,
                        self.button7, self.button8, self.button9]:
                btn.clicked.connect(self.button_clicked)
        else:
            for btn in [self.button1, self.button2, self.button3,
                        self.button4, self.button5, self.button6,
                        self.button7, self.button8, self.button9]:
                btn.setDisabled(True)
    def go_back(self):
            self.stack.setCurrentIndex(0)  # go back to menu
    def button_clicked(self):
        if self.game_over:
            return

        btn = self.sender()

        if btn.text() != "":
            return

        btn.setText(self.current_player)
        self.track += 1
        self.game_logic()

        # stop if game ended
        if self.game_over:
            return

        # switch turn
        self.current_player = "O" if self.current_player == "X" else "X"

        # AI move (ONLY after player X move)
        if self.mode == "pvc" and self.current_player == "O":
            self.computer_move()

    def game_logic(self):
        # (UNCHANGED — your logic kept as-is)
        if self.button1.text() == self.button2.text()== self.button3.text()=='X':
            self.game_status.setText("Player 1 Winner"); self.game_over = True
        if self.button4.text() == self.button5.text()== self.button6.text()=='X':
            self.game_status.setText("Player 1 Winner"); self.game_over = True
        if self.button7.text() == self.button8.text()== self.button9.text()=='X':
            self.game_status.setText("Player 1 Winner"); self.game_over = True

        if self.button1.text() == self.button4.text()== self.button7.text()=='X':
            self.game_status.setText("Player 1 Winner"); self.game_over = True
        if self.button2.text() == self.button5.text()== self.button8.text()=='X':
            self.game_status.setText("Player 1 Winner"); self.game_over = True
        if self.button3.text() == self.button6.text()== self.button9.text()=='X':
            self.game_status.setText("Player 1 Winner"); self.game_over = True

        if self.button1.text() == self.button5.text()== self.button9.text()=='X':
            self.game_status.setText("Player 1 Winner"); self.game_over = True
        if self.button3.text() == self.button5.text()== self.button7.text()=='X':
            self.game_status.setText("Player 1 Winner"); self.game_over = True

        if self.button1.text() == self.button2.text()== self.button3.text()=='O':
            self.game_status.setText("Player 2 Winner"); self.game_over = True
        if self.button4.text() == self.button5.text()== self.button6.text()=='O':
            self.game_status.setText("Player 2 Winner"); self.game_over = True
        if self.button7.text() == self.button8.text()== self.button9.text()=='O':
            self.game_status.setText("Player 2 Winner"); self.game_over = True

        if self.button1.text() == self.button4.text()== self.button7.text()=='O':
            self.game_status.setText("Player 2 Winner"); self.game_over = True
        if self.button2.text() == self.button5.text()== self.button8.text()=='O':
            self.game_status.setText("Player 2 Winner"); self.game_over = True
        if self.button3.text() == self.button6.text()== self.button9.text()=='O':
            self.game_status.setText("Player 2 Winner"); self.game_over = True

        if self.button1.text() == self.button5.text()== self.button9.text()=='O':
            self.game_status.setText("Player 2 Winner"); self.game_over = True
        if self.button3.text() == self.button5.text()== self.button7.text()=='O':
            self.game_status.setText("Player 2 Winner"); self.game_over = True

        if self.track == 9:
            self.game_status.setText("Draw")
            self.game_over = True

    def reset_game(self):
        self.game_over = False
        self.current_player = 'X'
        self.track = 0
        self.game_status.setText("")

        for btn in [self.button1, self.button2, self.button3,
                    self.button4, self.button5, self.button6,
                    self.button7, self.button8, self.button9]:
            btn.setText("")
            btn.setDisabled(False)

    def computer_move(self):
        if self.game_over:
            return

        empty = [b for b in [
            self.button1, self.button2, self.button3,
            self.button4, self.button5, self.button6,
            self.button7, self.button8, self.button9
        ] if b.text() == ""]

        if not empty:
            return

        btn = random.choice(empty)
        btn.setText("O")
        self.track += 1

        self.game_logic()

        if self.game_over:
            return

        self.current_player = "X"



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())
