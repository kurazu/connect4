import itertools
import abc
import io


class Player:

    def __init__(self, symbol):
        self.symbol = symbol

    def ask_move(self, board):
        can_move = False
        while not can_move:
            move = input(
                f'[{self.symbol}] Insert token in column '
                f'(0-{board.COLUMNS - 1}):'
            )
            column = int(move)
            can_move = board.can_put(column)
            if can_move:
                return column


class Board:
    ROWS = 6
    COLUMNS = 7
    WINNING_SEQUENCE = 4

    def __init__(self):
        self.data = [
            [] for _ in range(self.COLUMNS)
        ]

    def get(self, column, row):
        stack = self.data[column]
        if row < len(stack):
            return stack[row]
        else:
            return None

    def can_put(self, column):
        assert 0 <= column < self.COLUMNS
        stack = self.data[column]
        return len(stack) < self.ROWS

    def put(self, column, player):
        assert 0 <= column < self.COLUMNS
        stack = self.data[column]
        assert len(stack) < self.ROWS
        row = len(stack)
        stack.append(player)
        return self.find4(column, row, player)

    def __str__(self):
        buf = io.StringIO()
        buf.write('   |')
        for col in range(self.COLUMNS):
            buf.write(f'_{col}_|')
        buf.write('\n')
        for row in reversed(range(self.ROWS)):
            buf.write(f'{row}. |')
            for col in range(self.COLUMNS):
                player = self.get(col, row)
                if player:
                    symbol = player.symbol
                else:
                    symbol = ' '
                buf.write(' ')
                buf.write(symbol)
                buf.write(' |')
            buf.write('\n')
        return buf.getvalue()

    def is_full(self):
        return all(len(stack) == self.ROWS for stack in self.data)

    def find4(self, column, row, player):
        return (
            self.find_horizontal(column, row, player) or
            self.find_vertical(column, row, player) or
            self.find_diagonal_45_deg(column, row, player) or
            self.find_diagonal_135_deg(column, row, player)
        )

    def find_horizontal(self, column, row, player):
        columns = self.seq(start=column - 1, step=-1, limit=self.COLUMNS)
        rows = itertools.repeat(row)
        left_matching = self.count_matching(columns, rows, player)

        columns = self.seq(start=column + 1, step=+1, limit=self.COLUMNS)
        right_matching = self.count_matching(columns, rows, player)
        matching = left_matching + 1 + right_matching
        print(
            f'HORIZONTAL from column={column}, row={row} '
            f'left {left_matching} + 1 + right {right_matching} = {matching}'
        )
        return matching >= self.WINNING_SEQUENCE

    def find_vertical(self, column, row, player):
        columns = itertools.repeat(column)
        rows = self.seq(start=row - 1, step=-1, limit=self.ROWS)
        down_matching = self.count_matching(columns, rows, player)
        matching = down_matching + 1
        print(
            f'VERTICAL from column={column}, row={row} '
            f'down {down_matching} + 1 = {matching}'
        )
        return matching >= self.WINNING_SEQUENCE

    def find_diagonal_45_deg(self, column, row, player):
        columns = self.seq(start=column + 1, step=+1, limit=self.COLUMNS)
        rows = self.seq(start=row + 1, step=+1, limit=self.ROWS)
        right_up_matching = self.count_matching(columns, rows, player)

        columns = self.seq(start=column - 1, step=-1, limit=self.COLUMNS)
        rows = self.seq(start=row - 1, step=-1, limit=self.ROWS)
        left_down_matching = self.count_matching(columns, rows, player)

        matching = right_up_matching + 1 + left_down_matching
        print(
            f'DIAGONAL45 from column={column}, row={row} '
            f'right up {right_up_matching} + 1 + '
            f'left down {left_down_matching} = {matching}'
        )
        return matching >= self.WINNING_SEQUENCE

    def find_diagonal_135_deg(self, column, row, player):
        columns = self.seq(start=column - 1, step=-1, limit=self.COLUMNS)
        rows = self.seq(start=row + 1, step=+1, limit=self.ROWS)
        left_up_matching = self.count_matching(columns, rows, player)

        columns = self.seq(start=column + 1, step=+1, limit=self.COLUMNS)
        rows = self.seq(start=row - 1, step=-1, limit=self.ROWS)
        right_down_matching = self.count_matching(columns, rows, player)

        matching = left_up_matching + 1 + right_down_matching
        print(
            f'DIAGONAL135 from column={column}, row={row} '
            f'lef up {left_up_matching} + 1 + '
            f'right down {right_down_matching} = {matching}'
        )
        return (
            matching >= self.WINNING_SEQUENCE
        )

    def seq(self, start, step, limit):
        current = start
        while current >= 0 and current < limit:
            yield current
            current += step

    def count_matching(self, columns, rows, player):
        count = 0
        for column, row in zip(columns, rows):
            value = self.get(column, row)
            if value != player:
                break
            count += 1
        return count


class Game:

    def __init__(self, players):
        self.board = Board()
        self.players = players

    def run(self):
        for current_player in itertools.cycle(self.players):
            print(self.board)
            column = current_player.ask_move(self.board)
            win = self.board.put(column, current_player)
            if win:
                print(f'Player {current_player.symbol} wins!')
                break
            if self.board.is_full():
                print('Draw')
                break
        print(self.board)


def main():
    p1 = Player('X')
    p2 = Player('O')
    game = Game([p1, p2])
    game.run()


if __name__ == '__main__':
    main()
