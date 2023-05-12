'''
	Định nghĩa một class BoardEvaluator.
'''


class BoardEvaluator(object):

    def __init__(self):
        # self.POS là để tăng thêm trọng lượng cho mỗi lần xen kẽ
        # Thêm trọng số của 7 vào tâm, 6 vào hình vuông bên ngoài, sau đó
        # 5, 4, 3, 2, 1, từ 0 đến ô vuông ngoài cùng.
        self.POS = []
        for i in range(15):
            row = []
            for j in range(15):
                row.append(7 - max(abs(i - 7), abs(j - 7)))
            # row = [ (7 - max(abs(i - 7), abs(j - 7))) for j in range(15) ]
            self.POS.append(tuple(row))

        # Các loại tình huống khác nhau bên dưới
        self.cTwo = 1		# chong'er 		2 viên đá liên tiếp, 1 lần di chuyển để tạo chongsan
        self.cThree = 2		# chongsan 		3 viên đá liên tiếp, 1 lần di chuyển để tạo chongsi
        # chongsi 		4 viên đá liên tiếp, 1 lần di chuyển (1 vị trí có thể) để tạo thành 5 viên
        self.cFour = 3
        self.two = 4		# huo'er 		2 viên đá liên tiếp, 1 di chuyển để tạo ra một huosan
        self.three = 5		# huosan 		3 viên đá liên tiếp, 1 lần di chuyển để tạo ra một viên đá huosi
        # huosi 		4 viên đá liên tiếp, 1 lần di chuyển (2 vị trí có thể) để tạo thành 5
        self.four = 6
        self.five = 7		# huowu 		5 viên đá liên tiếp
        self.analyzed = 8		# Đã được phân tích
        self.unanalyzed = 0			# Chưa được phân tích

        # Lưu kết quả phân tích hiện tại trong một dòng
        self.result = [0 for i in range(30)]
        self.line = [0 for i in range(30)]		# Dữ liệu hiện tại trong một dòng
        self.record = []			# Kết quả phân tích toàn bộ bảng

        # Định dạng của mỗi mục trong danh sách là record[row][col][dir]
        for i in range(15):
            self.record.append([])
            self.record[i] = []
            for j in range(15):
                self.record[i].append([0, 0, 0, 0])
        self.count = []				# Số lượng của mỗi tình huống: count[X/O][situation]
        for i in range(3):
            data = [0 for i in range(10)]
            self.count.append(data)
        self.reset()

    # Đặt lại dữ liệu

    def reset(self):
        unanalyzed = self.unanalyzed
        count = self.count
        for i in range(15):
            line = self.record[i]
            for j in range(15):
                line[j][0] = unanalyzed
                line[j][1] = unanalyzed
                line[j][2] = unanalyzed
                line[j][3] = unanalyzed
        for i in range(10):
            count[0][i] = 0
            count[1][i] = 0
            count[2][i] = 0
        return 0

        # Bảng phân tích & đánh giá
        # Trả về điểm dựa trên kết quả phân tích

    def evaluate(self, board, turn):
        score = self.__evaluate(board, turn)
        count = self.count
        if score < -9000:
            if turn == 1:
                stone = 2
            elif turn == 2:
                stone = 1
            # print('evaluate: stone = ', stone)
            for i in range(10):
                if count[stone][i] > 0:
                    score -= i
        elif score > 9000:
            if turn == 1:
                stone = 2
            elif turn == 2:
                stone = 1
            # print('evaluate: stone = ', stone)
            for i in range(10):
                if count[turn][i] > 0:
                    score += i
        return score

        # Bảng phân tích & đánh giá bảng theo 4 hướng: ngang, dọc, chéo (bên trái hoặc bên phải)
        # Trả về điểm chênh lệch giữa các người chơi dựa trên kết quả phân tích

    def __evaluate(self, board, turn):
        record = self.record
        count = self.count
        unanalyzed = self.unanalyzed
        analyzed = self.analyzed
        self.reset()
        # Phân tích theo 4 hướng
        for i in range(15):
            boardrow = board[i]
            recordrow = record[i]
            for j in range(15):
                if boardrow[j] != 0:
                    # Chưa phân tích theo chiều ngang
                    if recordrow[j][0] == unanalyzed:
                        self.__analysis_horizon(board, i, j)
                    # chưa phân tích theo chiều dọc
                    if recordrow[j][1] == unanalyzed:
                        self.__analysis_vertical(board, i, j)
                    # Chưa phân tích bên trái theo đường chéo
                    if recordrow[j][2] == unanalyzed:
                        self.__analysis_left(board, i, j)
                    # Chưa phân tích bên phải theo đường chéo
                    if recordrow[j][3] == unanalyzed:
                        self.__analysis_right(board, i, j)

        five = self.five
        four = self.four
        three = self.three
        two = self.two
        cFour = self.cFour
        cThree = self.cThree
        cTwo = self.cTwo

        check = {}

        # Đối với trắng hoặc đen, được tính toán số lần xuất hiện của các tình huống khác nhau (i.e., five, four, cFour, three, cThree, two, cTwo)
        for c in (five, four, cFour, three, cThree, two, cTwo):
            check[c] = 1
        # for each mỗi quân cờ trong bảng
        for i in range(15):
            for j in range(15):
                stone = board[i][j]
                if stone != 0:
                    # for 4 hướng
                    for k in range(4):
                        ch = record[i][j][k]
                        if ch in check:
                            count[stone][ch] += 1

        # Trả về điểm nếu có 5 quân thằng hàng
        O = 1
        X = 2
        # Lượt đi hiện tại là O
        if turn == O:
            if count[X][five]:
                return -9999
            elif count[O][five]:
                return 9999
        # Lượt đi hiện tại là X
        else:
            if count[O][five]:
                return -9999
            elif count[X][five]:
                return 9999

        # Nếu tồn tại 2 chongsi, nó tương đương với 1 huosi
        if count[O][cFour] >= 2:
            count[O][four] += 1
        if count[X][cFour] >= 2:
            count[X][four] += 1

        # Trả về điểm cho các trường hợp cụ thể
        wvalue = 0
        bvalue = 0
        win = 0
        # Lượt đi hiện tại là O
        if turn == O:
            if count[O][four] > 0:			# O huosi
                return 9990
            if count[O][cFour] > 0:			# O chongsi
                return 9980
            if count[X][four] > 0:			# X huosi
                return -9970
            if count[X][cFour] and count[X][three]:			# X chongsi & huosan
                return -9960
            if count[O][three] and count[X][cFour] == 0:  # O huosan & no X chongsi
                return 9950
            if (count[X][three] > 1 and  # X > 1 huosan &
                    count[O][cFour] == 0 and  # no O chongsi &
                    count[O][three] == 0 and  # no O huosan &
                    count[O][cThree] == 0):		# no O chongsan
                return -9940

            if count[O][three] > 1:			# O > 1 huosan
                wvalue += 2000
            elif count[O][three]:			# O 1 huosan
                wvalue += 200
            if count[X][three] > 1:			# X > 1 huosan
                bvalue += 500
            elif count[X][three]:			# X 1 huosan
                bvalue += 100

            if count[O][cThree]:					# O chongsan
                wvalue += count[O][cThree] * 10
            if count[X][cThree]:					# X chongsan
                bvalue += count[X][cThree] * 10
            if count[O][two]:						# O huo'er
                wvalue += count[O][two] * 4
            if count[X][two]:						# X huo'er
                bvalue += count[X][two] * 4
            if count[O][cTwo]:						# O chong'er
                wvalue += count[O][cTwo]
            if count[X][cTwo]:						# X chong'er
                bvalue += count[X][cTwo]

        # current turn is X
        else:
            if count[X][four] > 0:			# X huosi
                return 9990
            if count[X][cFour] > 0:			# X chongsi
                return 9980
            if count[O][four] > 0:			# O huosi
                return -9970
            if count[O][cFour] and count[O][three]:			# O chongsi & huosan
                return -9960
            if count[X][three] and count[O][cFour] == 0:  # X huosan & no O chongsi
                return 9950
            if (count[O][three] > 1 and  # O >1 huosan &
                    count[X][cFour] == 0 and  # no X chongsi &
                    count[X][three] == 0 and  # no X huosan &
                    count[X][cThree] == 0):		# no X chongsan
                return -9940

            if count[X][three] > 1:			# X >1 huosan
                bvalue += 2000
            elif count[X][three]:			# X 1 huosan
                bvalue += 200
            if count[O][three] > 1:			# O >1 huosan
                wvalue += 500
            elif count[O][three]:			# O 1 huosan
                wvalue += 100

            if count[X][cThree]:					# X chongsan
                bvalue += count[X][cThree] * 10
            if count[O][cThree]:					# O chongsan
                wvalue += count[O][cThree] * 10
            if count[X][two]:						# X huo'er
                bvalue += count[X][two] * 4
            if count[O][two]:						# O huo'er
                wvalue += count[O][two] * 4
            if count[X][cTwo]:						# X chong'er
                bvalue += count[X][cTwo]
            if count[O][cTwo]:						# O chong'er
                wvalue += count[O][cTwo]

        # Bao gồm trọng số cho mỗi ô
        # Thêm trọng số của 7 vào tâm, 6 vào hình vuông bên ngoài, sau đó 5, 4, 3, 2, 1, từ 0 đến ô vuông ngoài cùng.
        wc = 0
        bc = 0
        # Đối với mỗi giao điểm với một quân cờ, thêm trọng lượng
        for i in range(15):
            for j in range(15):
                stone = board[i][j]
                if stone != 0:
                    if stone == O:
                        wc += self.POS[i][j]
                    else:
                        bc += self.POS[i][j]
        # Thêm tổng trọng số vào tổng điểm
        wvalue += wc
        bvalue += bc

        # Trả về điểm khác nhau giữa các người chơi
        if turn == O:
            return wvalue - bvalue

        return bvalue - wvalue

    # Phân tích theo chiều ngang 

    def __analysis_horizon(self, board, i, j):
        line = self.line
        result = self.result
        record = self.record
        unanalyzed = self.unanalyzed
        # Thêm từng giao điểm liên tiếp vào dòng
        for x in range(15):
            line[x] = board[i][x]
        self.analysis_line(line, result, 15, j)
        for x in range(15):
            if result[x] != unanalyzed:
                record[i][x][0] = result[x]
        return record[i][j][0]

    # Phân tích theo chiều dọc 

    def __analysis_vertical(self, board, i, j):
        line = self.line
        result = self.result
        record = self.record
        unanalyzed = self.unanalyzed
        for x in range(15):
            line[x] = board[x][j]
        self.analysis_line(line, result, 15, i)
        for x in range(15):
            if result[x] != unanalyzed:
                record[x][j][1] = result[x]
        return record[i][j][1]

    # phân tích theo đường chéo bên trái 

    def __analysis_left(self, board, i, j):
        line = self.line
        result = self.result
        record = self.record
        unanalyzed = self.unanalyzed
        if i < j:
            x, y = j - i, 0
        else:
            x, y = 0, i - j
        k = 0
        while k < 15:
            if x + k > 14 or y + k > 14:
                break
            line[k] = board[y + k][x + k]
            k += 1
        self.analysis_line(line, result, k, j - x)
        for s in range(k):
            if result[s] != unanalyzed:
                record[y + s][x + s][2] = result[s]
        return record[i][j][2]

    # Phân tích theo đường chéo bên phải

    def __analysis_right(self, board, i, j):
        line = self.line
        result = self.result
        record = self.record
        unanalyzed = self.unanalyzed
        if 14 - i < j:
            x, y, realnum = j - 14 + i, 14, 14 - i
        else:
            x, y, realnum = 0, i + j, j
        k = 0
        while k < 15:
            if x + k > 14 or y - k < 0:
                break
            line[k] = board[y - k][x + k]
            k += 1
        self.analysis_line(line, result, k, j - x)
        for s in range(k):
            if result[s] != unanalyzed:
                record[y - s][x + s][3] = result[s]
        return record[i][j][3]

    # Phân tích một dòng, tìm ra các trường hợp khác nhau (tức là năm, bốn, ba, v.v.)

    def analysis_line(self, line, record, num, pos):
        unanalyzed = self.unanalyzed
        analyzed = self.analyzed
        three = self.three
        cThree = self.cThree
        four = self.four
        cFour = self.cFour

        while len(line) < 30:
            line.append(15)
        while len(record) < 30:
            record.append(unanalyzed)

        for i in range(num, 30):
            line[i] = 15
        for i in range(num):
            record[i] = unanalyzed

        if num < 5:
            for i in range(num):
                record[i] = analyzed
            return 0
        stone = line[pos]
        inverse = (0, 2, 1)[stone]
        num -= 1
        xl = pos
        xr = pos
        # Đường viền bên trái
        while xl > 0:
            if line[xl - 1] != stone:
                break
            xl -= 1
        # Đường viền bên phải
        while xr < num:
            if line[xr + 1] != stone:
                break
            xr += 1
        left_range = xl
        right_range = xr
        # Đường viền bên trái (không phải giao điểm giữa các quân cờ của đối thủ)
        while left_range > 0:
            if line[left_range - 1] == inverse:
                break
            left_range -= 1
        # Đường viền bên phải (không phải giao điểm giữa các quân cờ của đối thủ)
        while right_range < num:
            if line[right_range + 1] == inverse:
                break
            right_range += 1

        # Nếu phạm vi tuyến tính nhỏ hơn 5, trả về trực tiếp
        if right_range - left_range < 4:
            for k in range(left_range, right_range + 1):
                record[k] = analyzed
            return 0

        # Thiết lập thành đã phân tích
        for k in range(xl, xr + 1):
            record[k] = analyzed

        srange = xr - xl

        # Nếu 5 ô liên tiếp
        if srange >= 4:
            record[pos] = self.five
            return self.five

        # Nếu 4 ô liên tiếp
        if srange == 3:
            leftfour = False
            # Nếu ô trống ở bên trái
            if xl > 0:
                if line[xl - 1] == 0:
                    # huo'si
                    leftfour = True
            if xr < num:
                if line[xr + 1] == 0:
                    if leftfour:
                        # huo'si
                        record[pos] = self.four
                    else:
                        # chognsi
                        record[pos] = self.cFour
                else:
                    if leftfour:
                        # chongsi
                        record[pos] = self.cFour
            else:
                if leftfour:
                    # chongsi
                    record[pos] = self.cFour
            return record[pos]

        # Nếu 3 ô liên tiếp
        if srange == 2:
            left3 = False
            # Nếu ô trống ở bên trái
            if xl > 0:
                # Nếu ô trống ở bên trái
                if line[xl - 1] == 0:
                    if xl > 1 and line[xl - 2] == stone:
                        record[xl] = cFour
                        record[xl - 2] = analyzed
                    else:
                        left3 = True
                elif xr == num or line[xr + 1] != 0:
                    return 0
            if xr < num:
                # Nếu ô trống ở bên phải
                if line[xr + 1] == 0:
                    if xr < num - 1 and line[xr + 2] == stone:
                        # 11101 hoặc 22202 tương đương với chongsi
                        record[xr] = cFour
                        record[xr + 2] = analyzed
                    elif left3:
                        record[xr] = three
                    else:
                        record[xr] = cThree
                elif record[xl] == cFour:
                    return record[xl]
                elif left3:
                    record[pos] = cThree
            else:
                if record[xl] == cFour:
                    return record[xl]
                if left3:
                    record[pos] = cThree
            return record[pos]

        # Nếu 2 ô liên tiếp
        if srange == 1:
            left2 = False
            if xl > 2:
                # Nếu ô trống ở bên trái
                if line[xl - 1] == 0:
                    if line[xl - 2] == stone:
                        if line[xl - 3] == stone:
                            record[xl - 3] = analyzed
                            record[xl - 2] = analyzed
                            record[xl] = cFour
                        elif line[xl - 3] == 0:
                            record[xl - 2] = analyzed
                            record[xl] = cThree
                    else:
                        left2 = True
            if xr < num:
                # Nếu ô trống ở bên phải
                if line[xr + 1] == 0:
                    if xr < num - 2 and line[xr + 2] == stone:
                        if line[xr + 3] == stone:
                            record[xr + 3] = analyzed
                            record[xr + 2] = analyzed
                            record[xr] = cFour
                        elif line[xr + 3] == 0:
                            record[xr + 2] = analyzed
                            record[xr] = left2 and three or cThree
                    else:
                        if record[xl] == cFour:
                            return record[xl]
                        if record[xl] == cThree:
                            record[xl] = three
                            return record[xl]
                        if left2:
                            record[pos] = self.two
                        else:
                            record[pos] = self.cTwo
                else:
                    if record[xl] == cFour:
                        return record[xl]
                    if left2:
                        record[pos] = self.cTwo
            return record[pos]
        return 0
