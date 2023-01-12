from collections import namedtuple

Chessman = namedtuple("Chessman", "name value color")
Point = namedtuple("Point", "x y")
BlackChessman = Chessman("黑子", 1, (0, 0, 0))
WhiteChessman = Chessman("白子", 2, (255, 255, 255))
offset = [(1, 0), (0, 1), (1, 1), (1, -1)]


class Chessboard:
    def __init__(self, line_points):
        self.line_points = line_points
        self._chessboard = [[0] * line_points for _ in range(line_points)]

    def getChessboard(self):
        return self._chessboard

    chessboard = property(getChessboard)

    # 判断是否可落子
    def canDrop(self, point):
        return self._chessboard[point.y][point.x] == 0

    def drop(self, chessman, point):
        """落子并返回战况"""
        print(f"{chessman.name}: ({point.x}, {point.y})")
        self._chessboard[point.y][point.x] = chessman.value

        if self.win(point):
            print(f"{chessman.name}获胜")
            return chessman

    def win(self, point):
        """判断是否获胜"""
        cur_value = self._chessboard[point.y][point.x]
        for o in offset:
            if self.getCountOnDirection(point, cur_value, o[0], o[1]):
                return True

    def getCountOnDirection(self, point, value, x_offset, y_offset):
        count = 1
        for step in range(1, 5):
            x = point.x + step * x_offset
            y = point.y + step * y_offset

            if 0 <= x < self.line_points and \
                    0 <= y < self.line_points and \
                    self._chessboard[y][x] == value:
                count += 1
            else:
                break
        for step in range(1, 5):
            x = point.x - step * x_offset
            y = point.y - step * y_offset
            if 0 <= x < self.line_points and \
                    0 <= y < self.line_points and \
                    self._chessboard[y][x] == value:
                count += 1
            else:
                break

        return count >= 5
