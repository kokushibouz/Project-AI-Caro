import re
import os
import copy
from typing import Any, Iterable, List, Tuple

SIZE = 15
P1_VICTORY_PATTERN = re.compile(r"11111") #kiểm tra điều kiện thắng cho player1
P2_VICTORY_PATTERN = re.compile(r"22222") #kiểm tra điều kiện thắng cho player2

#các trường hợp kiểm tra cho player1
PATTERN_1 = re.compile(r"211110|011112")
PATTERN_2 = re.compile(r"011110")
PATTERN_3 = re.compile(r"01110")
PATTERN_4 = re.compile(r"2011100|0011102")
PATTERN_5 = re.compile(r"010110|011010")
PATTERN_6 = re.compile(r"0110|01010")

#các trường hợp kiểm tra cho player2
P2_PATTERN_1 = re.compile(r"122220|022221")
P2_PATTERN_2 = re.compile(r"022220")
P2_PATTERN_3 = re.compile(r"02220")
P2_PATTERN_4 = re.compile(r"1022200|0022201")
P2_PATTERN_5 = re.compile(r"020220|022020")
P2_PATTERN_6 = re.compile(r"0220|02020")

def spiral(n: int) -> List[Tuple[int, int]]: # tạo danh sách tọa độ các điểm trong ma trận
   
    dx, dy = 1, 0  # Starting increments
    x, y = 0, 0    # Starting location
    matrix = [[-1]*n for _ in range(n)] # khởi tạo ma trận cỡ nxn với các phần từ là -1 
    for i in range(n**2):
        matrix[x][y] = i
        nx, ny = x + dx, y + dy # tính toán tọa độ của ô tiếp theo 
        if 0 <= nx < n and 0 <= ny < n and matrix[nx][ny] == -1:
            x, y = nx, ny
        else: 
            dx, dy = -dy, dx
            x, y = x + dx, y + dy
    output = [(0, 0) for _ in range(n**2)]
    for i in range(n):
        for j in range(n):
            output[matrix[i][j]] = (i, j)
    return output

SPIRAL_ORDER = spiral(SIZE)[::-1]


def stringfy(matrix: List[List[int]]) -> str: # chuyển từ dạng list sang dạng chuỗi 
    string = ""
    for line in matrix:
        string += "".join(map(str, line)) + "\n"
    return string


class Board():

    def __init__(self, ai_player: int) -> None:
        self._board = [[0 for _ in range(SIZE)] for _ in range(SIZE)] #khởi tạo bàn cờ 15x15 (ma trận 15x15 có phần tử là 0)
        self._actual_player = 1 #khởi tạo player hiện tại
        self._ai_player = ai_player #khởi tạo player2
        
    def place_stone(self, position: Tuple[int, int]) -> None: #player hiện tại đặt quân cờ 
        x_coord, y_coord = position
        self._board[y_coord][x_coord] = self._actual_player
        self._actual_player = 1 if self._actual_player == 2 else 2 # chuyển lượt chơi sau mỗi lần đặt quân cờ 

    def is_empty(self, position: Tuple[int, int]) -> bool: #các vị trí chưa đặt quân trên bàn cờ sẽ có gt=0
        x_coord, y_coord = position
        return self._board[y_coord][x_coord] == 0 

    def _diagonals(self) -> List[List[int]]: #tạo danh sách các đường chéo /
        return [[self._board[SIZE - p + q - 1][q]
                 for q in range(max(p - SIZE + 1, 0), min(p + 1, SIZE))]
                for p in range(SIZE + SIZE - 1)]

    def _antidiagonals(self) -> List[List[int]]: # tạo danh sách các đường chéo \
        return [[self._board[p - q][q]
                 for q in range(max(p - SIZE + 1, 0), min(p + 1, SIZE))]
                for p in range(SIZE + SIZE - 1)]

    def _columns(self) -> List[List[int]]: # tạo danh sách các cột 
        return [[self._board[i][j]
                 for i in range(SIZE)]
                for j in range(SIZE)]

    def victory(self) -> bool: # kiểm tra chiến thắng
        whole_board = "\n".join( map(stringfy, [self._board, self._diagonals(), self._antidiagonals(), self._columns()]))
        if P1_VICTORY_PATTERN.search(whole_board):
            return 1 
        if P2_VICTORY_PATTERN.search(whole_board):
            return 2
        return False
        
    # tính toán điểm số cho nước đi tiếp theo
    def evaluate(self) -> int:
        whole_board = "\n".join( map(stringfy, [self._board, self._diagonals(), self._antidiagonals(), self._columns()]))
        p1_value = 0
        p2_value = 0
        if P1_VICTORY_PATTERN.search(whole_board): 
            p1_value += 2**25
        elif P2_VICTORY_PATTERN.search(whole_board):
            p2_value += 2**25

        # tính toán giá trị cho tất cả trường hợp của người chơi 1 (nếu xuất hiện trong bảng)
        p1_value += 37 * 56 * len(PATTERN_2.findall(whole_board))
        p1_value += 56 * len(PATTERN_1.findall(whole_board))
        p1_value += 56 * len(PATTERN_3.findall(whole_board))
        p1_value += 56 * len(PATTERN_4.findall(whole_board))
        p1_value += 56 * len(PATTERN_5.findall(whole_board))
        p1_value += len(PATTERN_6.findall(whole_board))

        # tính toán giá trị cho tất cả trường hợp của người chơi 2 (nếu xuất hiện trong bảng)
        p2_value += 37 * 56 * len(P2_PATTERN_2.findall(whole_board))
        p2_value += 56 * len(P2_PATTERN_1.findall(whole_board))
        p2_value += 56 * len(P2_PATTERN_3.findall(whole_board))
        p2_value += 56 * len(P2_PATTERN_4.findall(whole_board))
        p2_value += 56 * len(P2_PATTERN_5.findall(whole_board))
        p2_value += len(P2_PATTERN_6.findall(whole_board))
        
        return p1_value - p2_value \
            if self._ai_player == 1 \
            else p2_value - p1_value

    def adjacents(self) -> Iterable[Any]: #AI player
        actual_board = copy.deepcopy(self) #tạo bản sao của bàn cờ hiện tại
        for i, j in SPIRAL_ORDER:
            if actual_board.is_empty((i, j)): #nếu vị trí (i,j) trong bảng còn trống thì cho phép đặt quân cờ 
                actual_board.place_stone((i, j))
                yield actual_board #trả về trạng thái của bảng
                # thay đổi player
                actual_board._actual_player = \
                    1 if actual_board._actual_player == 2 else 2
                actual_board._board[j][i] = 0
