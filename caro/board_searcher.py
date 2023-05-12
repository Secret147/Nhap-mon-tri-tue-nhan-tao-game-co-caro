from board_evaluator import BoardEvaluator


class BoardSearcher(object):
	"""Board searcher tìm kiếm nước đi kế tiếp tốt nhất"""

	def __init__ (self):
		self.evaluator = BoardEvaluator()
		self.board = [ [ 0 for n in range(15) ] for i in range(15) ]
		self.gameover = 0
		self.overvalue = 0
		self.maxdepth = 3	# Đặt độ sâu tối đa thành 3 để thời gian chạy cho mỗi lần di chuyển không quá dài
							# Độ sâu: 1 - <1 giây, 2 - vài giây, 3 - tối đa 4 phút


	def genMoves(self, turn):
		"""
			Tạo tất cả các nước đi hợp pháp cho bảng hiện tại.
			Lưu trữ điểm và vị trí của mỗi nước đi trong danh sách ở định dạng (score, i, j)
		"""
		moves = []
		board = self.board
		POSES = self.evaluator.POS
		for i in range(15):
			for j in range(15):
				if board[i][j] == 0:
					score = POSES[i][j]
					moves.append((score, i, j))
	
		moves.sort(reverse=True)	# Sắp xếp các nước đi theo thứ tự ngược lại, tức là với điểm số giảm dần
		return moves
	

	def __search(self, turn, depth, alpha = -0x7fffffff, beta = 0x7fffffff):
		"""	
			Tìm kiếm đệ quy, trả về điểm tốt nhất.
			Thuật toán Minimax với sự cắt tỉa alpha-beta.
			0x7fffffff == (2 ^ 31) -1, cho biết một giá trị lớn
		"""

		# Trường hợp cơ sở: độ sâu là 0
		# Đánh giá bảng và trả lại
		if depth <= 0:
			score = self.evaluator.evaluate(self.board, turn)
			return score

		# Nếu trò chơi kết thúc, trả về điểm ngay lập tức
		score = self.evaluator.evaluate(self.board, turn)
		if abs(score) >= 9999 and depth < self.maxdepth: 
			return score

		# Tạo các bước di chuyển mới
		moves = self.genMoves(turn)
		bestmove = None

		# Cho tất cả các bước di chuyển hiện tại len(move) == số giao điểm trống trên bảng hiện tại
		# Trường hợp xấu nhất là O (m ^ n) hoặc O (m! / (m-n)!), m = số điểm trống, n = độ sâu (số bước tiếp theo mà chương trình này dự đoán)
		for score, row, col in moves:

			# Nhãn hiện tại di chuyển lên bảng
			self.board[row][col] = turn
			
			# Tính lượt tiếp theo
			if turn == 1:
				nturn = 2
			elif turn == 2:
				nturn = 1
			
			# DFS, trả vềđiểm  và vị trí nước đi
			score = - self.__search(nturn, depth - 1, -beta, -alpha)

			# Xóa nước đi hiện tại trên bảng
			self.board[row][col] = 0

			# Tính nước đi với điểm tốt nhất
			# Cắt tỉa alpha beta: loại bỏ các nút được đánh giá bằng thuật toán minimax
			# Trong cây tìm kiếm, loại bỏ các nhánh không thể ảnh hưởng đến quyết định cuối cùng.
			if score > alpha:
				alpha = score
				bestmove = (row, col)
				if alpha >= beta:
					break
		
		# Nếu độ sâu là độ sâu tối đa, ghi lại nước đi tốt nhất
		if depth == self.maxdepth and bestmove:
			self.bestmove = bestmove

		# Trả lại điểm số tốt nhất hiện tại và nước đi tương ứng của nó
		return alpha

	# Tìm kiếm cụ thể
	# Tham số: turn (lượt đi): 1 (O) / 2 (X), depth (độ sâu)
	def search(self, turn, depth=3):
		self.maxdepth = depth
		self.bestmove = None
		score = self.__search(turn, depth)
		if abs(score) > 8000:
			self.maxdepth = depth
			score = self.__search(turn, 1)
		row, col = self.bestmove
		return score, row, col