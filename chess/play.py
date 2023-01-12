import sys
import random
import pygame
import pygame.gfxdraw
from pygame.locals import *
from .chess import Chessboard, BlackChessman, WhiteChessman, offset, Point

SIZE = 30  # 棋盘每个点时间的间隔
LINE_POINTS = 19  # 棋盘每行/每列点数
OUTER_WIDTH = 20  # 棋盘外宽度
BORDER_WIDTH = 6  # 边框宽度
INSIDE_WIDTH = 6  # 边框跟实际的棋盘之间的间隔
BORDER_LENGTH = SIZE * (LINE_POINTS - 1) + INSIDE_WIDTH * 2 + BORDER_WIDTH  # 边框线的长度
START_X = START_Y = OUTER_WIDTH + int(BORDER_WIDTH / 2) + INSIDE_WIDTH  # 网格线起点（左上角）坐标
SCREEN_HEIGHT = SIZE * (LINE_POINTS - 1) + OUTER_WIDTH * 2 + BORDER_WIDTH + INSIDE_WIDTH * 2  # 游戏屏幕的高
SCREEN_WIDTH = SCREEN_HEIGHT + 200  # 游戏屏幕的宽

# 棋子半径
RADIUS = SIZE // 2 - 2
RADIUS2 = SIZE // 2 + 2

# 颜色设置
CHESSBOARD_COLOR = (0XDE, 0XBA, 0X74)  # 棋盘颜色
BLACK_COLOR = (0, 0, 0)  # 黑棋颜色
WHITE_COLOR = (255, 255, 255)  # 白棋颜色
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (0, 0, 255)

RIGHT_INFO_POS_X = SCREEN_HEIGHT + RADIUS2 * 2 + 10


def displayText(screen, font, x, y, text, fcolor=(255, 255, 255)):
    img_text = font.render(text, True, fcolor)
    screen.blit(img_text, (x, y))


def play():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("五子棋")

    font1 = pygame.font.SysFont("SimHei", 32)
    font2 = pygame.font.SysFont("SimHei", 72)
    fwidth, fheight = font2.size("黑方获胜")

    chessboard = Chessboard(LINE_POINTS)
    cur_runner = BlackChessman
    winner = None
    computer = AI(LINE_POINTS, WhiteChessman)

    black_win_count = 0
    white_win_count = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if winner is not None:
                        winner = None
                        cur_runner = BlackChessman
                        chessboard = Chessboard(LINE_POINTS)
                        computer = AI(LINE_POINTS, WhiteChessman)
            elif event.type == MOUSEBUTTONDOWN:
                if winner is None:
                    pressed_array = pygame.mouse.get_pressed()
                    if pressed_array[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        click_point = getClickPoint(mouse_pos)
                        if click_point is not None:
                            if chessboard.canDrop(click_point):
                                winner = chessboard.drop(cur_runner, click_point)
                                if winner is None:
                                    cur_runner = getNext(cur_runner)
                                    computer.getOpponentDrop(click_point)
                                    AI_point = computer.aiDrop()
                                    winner = chessboard.drop(cur_runner, AI_point)
                                    if winner is not None:
                                        white_win_count += 1
                                    cur_runner = getNext(cur_runner)
                                else:
                                    black_win_count += 1
                        else:
                            print("超出棋盘区域")

        # 画棋盘
        drawChessboard(screen)

        # 画棋盘上已有的棋子
        for i, row in enumerate(chessboard.chessboard):
            for j, cell in enumerate(row):
                if cell == BlackChessman.value:
                    drawChessman(screen, Point(j, i), BlackChessman.color)
                elif cell == WhiteChessman.value:
                    drawChessman(screen, Point(j, i), WhiteChessman.color)

        drawRightInfo(screen, font1, black_win_count, white_win_count)

        if winner:
            displayText(screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2,
                        winner.name + "获胜", RED_COLOR)

        pygame.display.flip()


def getNext(cur_runner):
    if cur_runner == BlackChessman:
        return WhiteChessman
    else:
        return BlackChessman


# 画棋盘
def drawChessboard(screen):
    # 填充棋盘背景色
    screen.fill(CHESSBOARD_COLOR)
    # 画棋盘网格线外的边框
    pygame.draw.rect(screen, BLACK_COLOR, (OUTER_WIDTH, OUTER_WIDTH, BORDER_LENGTH, BORDER_LENGTH), BORDER_WIDTH)
    # 画网格线
    for i in range(LINE_POINTS):
        pygame.draw.line(screen, BLACK_COLOR, (START_Y, START_Y + SIZE * i),
                         (START_Y + SIZE * (LINE_POINTS - 1), START_Y + SIZE * i), 1)
    for j in range(LINE_POINTS):
        pygame.draw.line(screen, BLACK_COLOR, (START_X + SIZE * j, START_X),
                         (START_X + SIZE * j, START_X + SIZE * (LINE_POINTS - 1)), 1)
    # 画星位和天元
    for i in (3, 9, 15):
        for j in (3, 9, 15):
            if i == j == 9:
                radius = 5
            else:
                radius = 3
            pygame.gfxdraw.aacircle(screen, START_X + SIZE * i, START_Y + SIZE * j, radius, BLACK_COLOR)
            pygame.gfxdraw.filled_circle(screen, START_X + SIZE * i, START_Y + SIZE * j, radius, BLACK_COLOR)


# 画棋子
def drawChessman(screen, point, stone_color):
    pygame.gfxdraw.aacircle(screen, START_X + SIZE * point.x, START_Y + SIZE * point.y, RADIUS, stone_color)
    pygame.gfxdraw.filled_circle(screen, START_X + SIZE * point.x, START_Y + SIZE * point.y, RADIUS, stone_color)


# 画右侧信息显示
def drawRightInfo(screen, font, black_win_count, white_win_count):
    drawChessmanPos(screen, (SCREEN_HEIGHT + RADIUS2, START_X + RADIUS2), BlackChessman.color)
    drawChessmanPos(screen, (SCREEN_HEIGHT + RADIUS2, START_X + RADIUS2 * 4), WhiteChessman.color)

    displayText(screen, font, RIGHT_INFO_POS_X, START_X + 3, "玩家(先)", BLUE_COLOR)
    displayText(screen, font, RIGHT_INFO_POS_X, START_X + RADIUS2 * 3 + 3, "电脑(后)", BLUE_COLOR)

    displayText(screen, font, SCREEN_HEIGHT, SCREEN_HEIGHT - RADIUS2 * 8, '战况：', BLUE_COLOR)
    drawChessmanPos(screen, (SCREEN_HEIGHT + RADIUS2, SCREEN_HEIGHT - int(RADIUS2 * 4.5)), BlackChessman.color)
    drawChessmanPos(screen, (SCREEN_HEIGHT + RADIUS2, SCREEN_HEIGHT - RADIUS2 * 2), WhiteChessman.color)
    displayText(screen, font, RIGHT_INFO_POS_X, SCREEN_HEIGHT - int(RADIUS2 * 5.5) + 3, f'{black_win_count} 胜',
                BLUE_COLOR)
    displayText(screen, font, RIGHT_INFO_POS_X, SCREEN_HEIGHT - RADIUS2 * 3 + 3, f'{white_win_count} 胜', BLUE_COLOR)


def drawChessmanPos(screen, pos, stone_color):
    pygame.gfxdraw.aacircle(screen, pos[0], pos[1], RADIUS2, stone_color)
    pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], RADIUS2, stone_color)


# 根据鼠标点击位置，返回游戏区坐标
def getClickPoint(click_pos):
    pos_x = click_pos[0] - START_X
    pos_y = click_pos[1] - START_Y
    if pos_x < -INSIDE_WIDTH or pos_y < -INSIDE_WIDTH:
        return None
    x = pos_x // SIZE
    y = pos_y // SIZE
    if pos_x % SIZE > RADIUS:
        x += 1
    if pos_y % SIZE > RADIUS:
        y += 1
    if x >= LINE_POINTS or y >= LINE_POINTS:
        return None

    return Point(x, y)


class AI:
    def __init__(self, LINE_POINTS, chessman):
        self._my = chessman
        self._LINE_POINTS = LINE_POINTS
        self._opponent = BlackChessman if chessman == WhiteChessman else WhiteChessman
        self._chessboard = [[0] * LINE_POINTS for _ in range(LINE_POINTS)]

    def getOpponentDrop(self, point):
        self._chessboard[point.y][point.x] = self._opponent.value

    def aiDrop(self):
        point = None
        score = 0
        for i in range(self._LINE_POINTS):
            for j in range(self._LINE_POINTS):
                if self._chessboard[j][i] == 0:
                    _score = self.getScore(Point(i, j))
                    if _score > score:
                        score = _score
                        point = Point(i, j)
                    elif _score == score and _score > 0:
                        r = random.randint(0, 100)
                        if r % 2 == 0:
                            point = Point(i, j)
        self._chessboard[point.y][point.x] = self._my.value
        return point

    def getScore(self, point):
        score = 0
        for o in offset:
            score += self.getDirectionScore(point, o[0], o[1])
        return score

    def getDirectionScore(self, point, x_offset, y_offset):
        count = 0  # 落子处我方连续子数
        _count = 0  # 落子处对方连续子数
        space = None  # 我方连续子中有无空格
        _space = None  # 对方连续子中有无空格
        both = 0  # 我方连续子两端有无阻挡
        _both = 0  # 对方连续子两端有无阻挡

        # 如果是 1 表示是边上是我方子，2 表示敌方子
        flag = self.getPieceColor(point, x_offset, y_offset, True)
        if flag != 0:
            for step in range(1, 6):
                x = point.x + step * x_offset
                y = point.y + step * y_offset
                if 0 <= x < self._LINE_POINTS and \
                        0 <= y < self._LINE_POINTS:
                    if flag == 1:
                        if self._chessboard[y][x] == self._my.value:
                            count += 1
                            if space is False:
                                space = True
                        elif self._chessboard[y][x] == self._opponent.value:
                            _both += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break  # 遇到第二个空格退出
                    elif flag == 2:
                        if self._chessboard[y][x] == self._my.value:
                            _both += 1
                            break
                        elif self._chessboard[y][x] == self._opponent.value:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                    # 遇到边也就是阻挡
                    if flag == 1:
                        both += 1
                    elif flag == 2:
                        _both += 1

        if space is False:
            space = None
        if _space is False:
            _space = None

        _flag = self.getPieceColor(point, -x_offset, -y_offset, True)
        if _flag != 0:
            for step in range(1, 6):
                x = point.x - step * x_offset
                y = point.y - step * y_offset
                if 0 <= x < self._LINE_POINTS and 0 <= y < self._LINE_POINTS:
                    if _flag == 1:
                        if self._chessboard[y][x] == self._my.value:
                            count += 1
                            if space is False:
                                space = True
                        elif self._chessboard[y][x] == self._opponent.value:
                            _both += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break  # 遇到第二个空格退出
                    elif _flag == 2:
                        if self._chessboard[y][x] == self._my.value:
                            _both += 1
                            break
                        elif self._chessboard[y][x] == self._opponent.value:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                    # 遇到边也就是阻挡
                    if _flag == 1:
                        both += 1
                    elif _flag == 2:
                        _both += 1

        if count == 4:
            score = 10000
        elif _count == 4:
            score = 9000
        elif count == 3:
            if both == 0:
                score = 1000
            elif both == 1:
                score = 100
            else:
                score = 0
        elif _count == 3:
            if _both == 0:
                score = 900
            elif _both == 1:
                score = 90
            else:
                score = 0
        elif count == 2:
            if both == 0:
                score = 100
            elif both == 1:
                score = 10
            else:
                score = 0
        elif _count == 2:
            if _both == 0:
                score = 90
            elif _both == 1:
                score = 9
            else:
                score = 0
        elif count == 1:
            score = 10
        elif _count == 1:
            score = 9
        else:
            score = 0

        if space or _space:
            score /= 2

        return score

    # 判断指定位置处在指定方向上是我方子、对方子、空
    def getPieceColor(self, point, x_offset, y_offset, next_runner):
        x = point.x + x_offset
        y = point.y + y_offset
        if 0 <= x < self._LINE_POINTS and 0 <= y < self._LINE_POINTS:
            if self._chessboard[y][x] == self._my.value:
                return 1
            elif self._chessboard[y][x] == self._opponent.value:
                return 2
            else:
                if next_runner:
                    return self.getPieceColor(Point(x, y), x_offset, y_offset, False)
                else:
                    return 0
        else:
            return 0
