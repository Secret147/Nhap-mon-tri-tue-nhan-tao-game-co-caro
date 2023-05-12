class GameBoard(object):
    """Game board."""

    def __init__(self):
        # board là một mảng 15 * 15: mỗi vị trí ban đầu được đặt là 0
        self.__board = [[0 for _ in range(15)] for _ in range(15)]

        # Lưu trữ vị trí của 5 nước đi trên một dòng
        self.won = {}

    def reset(self):
        """Xóa bảng (đặt tất cả vị trí thành 0)."""
        self.__board = [[0 for _ in range(15)] for _ in range(15)]

    def get(self, row, col):
        """Nhận giá trị tại một ô."""

        if row < 0 or row >= 15 or col < 0 or col >= 15:
            return 0
        return self.__board[row][col]

    def check(self):
        """ 
            Kiểm tra xem có người chiến thắng không.
            Trả về: 0 - không có người thắng, 1 - người chơi O thắng, 2 - người chơi X thắng
        """
        board = self.__board
        # Kiểm tra trong 4 hướng
        # Một tọa độ là viết tắt của một hướng cụ thể, hãy tưởng tượng hướng của một tọa độ liên quan đến điểm gốc trên trục xy
        dirs = ((1, -1), (1, 0), (1, 1), (0, 1))
        for i in range(15):
            for j in range(15):
                # Nếu không có nước đi nào trên vị trí, không cần xem xét vị trí này
                if board[i][j] == 0:
                    continue
                # value - giá trị tại một ô, i-row, j-col
                value = board[i][j]
                # Kiểm tra xem có tồn tại 5 nước đi liên tục trong một dòng không
                for d in dirs:
                    x, y = i, j
                    count = 0
                    for _ in range(5):
                        if self.get(x, y) != value:
                            break
                        x += d[0]
                        y += d[1]
                        count += 1
                    # Nếu có 5 nước đi trong một dòng, lưu trữ vị trí của tất cả các nước đi, trả về giá trị
                    if count == 5:
                        self.won = {}
                        r, c = i, j
                        for _ in range(5):
                            self.won[(r, c)] = 1
                            r += d[0]
                            c += d[1]
                        return value
        return 0

    def board(self):
        return self.__board

    def show(self):
        """Hiển thị ra bảng hiện tại."""
        print('  A B C D E F G H I J K L M N O')
        self.check()
        for col in range(15):
            print(chr(ord('A') + col), end=" ")
            for row in range(15):
                ch = self.__board[row][col]
                if ch == 0:
                    print('.', end=" ")
                elif ch == 1:
                    print('O', end=" ")
                elif ch == 2:
                    print('X', end=" ")
            print()
