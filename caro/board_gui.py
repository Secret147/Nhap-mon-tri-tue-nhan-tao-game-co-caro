
import tkinter as tk
import numpy as np
from game_board import GameBoard
from board_searcher import BoardSearcher

size_board = 600


class BoardCanvas(tk.Canvas):
    """Sử dụng Tkinter để thực hiện một GUI cơ bản. Tkinter Canvas Widget là để vẽ bảng trò chơi và các quân cờ X và O."""

    def __init__(self, master=None, height=0, width=0):

        tk.Canvas.__init__(self, master, height=height, width=width)
        self.draw_gameBoard()
        self.gameBoard = GameBoard()
        self.boardSearcher = BoardSearcher()
        self.boardSearcher.board = self.gameBoard.board()
        self.turn = 1   # Lượt đi đầu tiên là O
        self.depth = 2
        self.prev_exist = False
        self.prev_row = 0
        self.prev_col = 0
        self.reset_board = False

        self.size = tk.IntVar()
        self.size.set(15)
        self.symbol_size = 300 / 25
        self.symbol_thickness = 5
        self.symbol_X_color = 'red'
        self.symbol_O_color = 'green'
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0

    def draw_gameBoard(self):
        """Lập bảng trò chơi."""

        # 15 đường ngang
        for i in range(14):
            self.create_line((i + 1) * size_board / 15,
                             0, (i + 1) * size_board / 15, size_board)

        # 15 dòng dọc
        for i in range(14):
            self.create_line(0, (i + 1) * size_board / 15,
                             size_board, (i + 1) * size_board / 15)

    def convert_logical_to_grid_position(self, logical_position):
        """Chuyển từ vị trí trên bảng thành tọa độ trên UI"""

        logical_position = np.array(logical_position)
        return (size_board / 15) * logical_position + size_board / (15 * 2)

    def convert_grid_to_logical_position(self, grid_position):
        """Chuyển từ tọa đồ trên UI thành vị trí trên bảng"""

        grid_position = np.array(grid_position)
        return tuple(np.array(grid_position // (size_board / 15), dtype=int))

    def draw_move(self, row, col):
        # logical_position: vị trí logic trên bàn cờ
        # grid_position: vị trí tọa đồ trên GUI
        logical_position = np.array([row, col])
        grid_position = self.convert_logical_to_grid_position(logical_position)
        if self.turn == 1:
            self.create_oval(grid_position[0] - self.symbol_size, grid_position[1] - self.symbol_size,
                             grid_position[0] + self.symbol_size, grid_position[1] + self.symbol_size, width=self.symbol_thickness,
                             outline=self.symbol_O_color)

        else:
            self.create_line(grid_position[0] - self.symbol_size, grid_position[1] - self.symbol_size,
                             grid_position[0] + self.symbol_size, grid_position[1] + self.symbol_size, width=self.symbol_thickness,
                             fill=self.symbol_X_color)
            self.create_line(grid_position[0] - self.symbol_size, grid_position[1] + self.symbol_size,
                             grid_position[0] + self.symbol_size, grid_position[1] - self.symbol_size, width=self.symbol_thickness,
                             fill=self.symbol_X_color)

    def draw_prev_stone(self, row, col):
        """
            Làm nổi bật nước đi trước đó.
            Tham số: row, col (vị trí của một ô)
        """

        logical_position = np.array([row, col])
        grid_position = self.convert_logical_to_grid_position(logical_position)

        self.create_line(grid_position[0] - self.symbol_size, grid_position[1] - self.symbol_size,
                            grid_position[0] + self.symbol_size, grid_position[1] + self.symbol_size, width=self.symbol_thickness,
                            fill=self.symbol_X_color)
        self.create_line(grid_position[0] - self.symbol_size, grid_position[1] + self.symbol_size,
                            grid_position[0] + self.symbol_size, grid_position[1] - self.symbol_size, width=self.symbol_thickness,
                            fill=self.symbol_X_color)
        
    def is_grid_occupied(self, row, col):
        if self.gameBoard.board()[row][col] != 0:
            return True
        else:
            return False
        
    def new_game(self):
        self.delete("all")
        self.draw_gameBoard()
        self.gameBoard = GameBoard()
        self.boardSearcher = BoardSearcher()
        self.boardSearcher.board = self.gameBoard.board()

    def gameLoop(self, event):
        """
                Vòng lặp chính của trò chơi.
                Lưu ý: Trò chơi được chơi trên cửa sổ tkinter. Tuy nhiên, có một số thông tin khá hữu ích được in trên thiết bị đầu cuối như hình ảnh trực quan đơn giản của bàn cờ sau mỗi lượt, thông báo cho biết người dùng đạt đến bước nào và trò chơi qua thông báo. Người dùng không cần phải nhìn vào những gì hiển thị trên thiết bị đầu cuối.

                self.gameBoard.board()[row][col] == 1(quân cờ O) / 2(quân cờ X)
                self.gameBoard.check() == 1(O thắng) / 2(X thắng)

                Tham số: event (vị trí người dùng nhấp vào bằng chuột)
        """
        if not self.reset_board:
            while True:
                # Lượt đi của người chơi, quân cờ của người chơi là O
                print('Your turn now...\n')
                self.turn = 1
                row, col = self.convert_grid_to_logical_position(
                    [event.x, event.y])
                if self.is_grid_occupied(row, col):
                    print('Invalid position.\n')
                    return 0
                else:
                    self.draw_move(row, col)
                    break
            # Đặt quân cờ O sau khi xác định vị trí
            self.gameBoard.board()[row][col] = 1

            # Nếu người dùng thắng trò chơi, kết thúc trò chơi và hủy liên kết.
            if self.gameBoard.check() == 1:
                self.O_score += 1
                text = 'Winner: You (O)'
                color = self.symbol_X_color

                self.delete("all")
                self.create_text(
                    size_board / 2, size_board / 3, font="cmr 50 bold", fill=color, text=text)

                score_text = 'Scores \n'
                self.create_text(size_board / 2, 5 * size_board / 8, font="cmr 40 bold", fill="blue",
                                 text=score_text)

                score_text = 'You (O): ' + str(self.O_score) + '\n'
                score_text += 'AI (X): ' + str(self.X_score) + '\n'
                self.create_text(size_board / 2, 3 * size_board / 4, font="cmr 30 bold", fill="blue",
                                 text=score_text)

                score_text = 'Play again \n'
                self.create_text(size_board / 2, 15 * size_board / 16, font="cmr 20 bold", fill="gray",
                                 text=score_text)
                self.reset_board = True
                return 0

            # Thay đổi lượt sang AI
            self.turn = 2
            print('AI is thinking now...')

            # Xác định vị trí AI sẽ đặt một quân cờ X.
            score, row, col = self.boardSearcher.search(self.turn, self.depth)
            coord = '%s%s' % (chr(ord('A') + row), chr(ord('A') + col))
            print('AI has moved to {}\n'.format(coord))
            # Đặt một quân cờ X sau khi xác định vị trí.
            self.gameBoard.board()[row][col] = 2
            self.draw_prev_stone(row, col)
            if self.prev_exist == False:
                self.prev_exist = True
            else:
                self.draw_move(self.prev_row, self.prev_col)
            self.prev_row, self.prev_col = row, col
            self.gameBoard.show()
            print('\n')

            # Liên kết sau khi AI di chuyển để người dùng có thể tiếp tục chơi
            self.bind('<Button-1>', self.gameLoop)

            # Nếu AI thắng trò chơi, kết thúc trò chơi.
            if self.gameBoard.check() == 2:
                self.X_score += 1
                text = 'Winner: AI (X)'
                color = self.symbol_X_color

                self.delete("all")
                self.create_text(
                    size_board / 2, size_board / 3, font="cmr 50 bold", fill=color, text=text)

                score_text = 'Scores \n'
                self.create_text(size_board / 2, 5 * size_board / 8, font="cmr 40 bold", fill="blue",
                                 text=score_text)

                score_text = 'You (O): ' + str(self.O_score) + '\n'
                score_text += 'AI (X): ' + str(self.X_score) + '\n'
                self.create_text(size_board / 2, 3 * size_board / 4, font="cmr 30 bold", fill="blue",
                                 text=score_text)

                score_text = 'Play again \n'
                self.create_text(size_board / 2, 15 * size_board / 16, font="cmr 20 bold", fill="gray",
                                 text=score_text)
                self.reset_board = True
                return 0

        else:
            self.new_game()
            self.reset_board = False


class BoardFrame(tk.Frame):
    """Frame Widget được sử dụng để bao bọc bên ngoài Canvas Widget"""

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.create_widgets()

    def create_widgets(self):
        self.boardCanvas = BoardCanvas(height=size_board, width=size_board)
        self.boardCanvas.bind('<Button-1>', self.boardCanvas.gameLoop)
        self.boardCanvas.pack()
