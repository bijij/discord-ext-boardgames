import re
from typing import Union

from discord.ext import commands

__all__ = ('regional_indicator',  'keycap_digit', 'Cell', 'Board')


def regional_indicator(i):
    """Returns a regional indicator emoji given an index."""
    if isinstance(i, str):
        i = ord(i.upper()) - ord('A')
    return chr(0x1f1e6 + i)


def keycap_digit(i):
    """Returns a keycap digit emoji given an index."""
    if i == 10:
        return '\N{keycap ten}'
    return str(i) + '\N{combining enclosing keycap}'


class Cell(commands.Converter):
    """Returns the index of a cell."""

    @classmethod
    async def convert(self, ctx: commands.Context, argument: str):
        if re.match(r'[A-z]\d+', argument):
            return (int(argument[1:]) - 1, ord(argument[0].upper()) - 65)

        raise commands.BadArgument('Could not determine cell!')


class Board:
    """Simple emoji grid with row and column markers.

    size_x: int
        The width of the board, must be between 1 and 26.
    size_y: int
        The height of the board, must be between 1 and 10.
    fill_with: str
        An emoji to fill the board with by default.
    """

    pivot = '\N{black circle for record}'
    spacer = '\N{black large square}'

    def __init__(self, size_x, size_y, fill_with='\N{white large square}'):
        if not 1 <= size_x <= 26:
            raise ValueError('Boards can have a maximum width of 26.')
        if not 1 <= size_y <= 10:
            raise ValueError('Boards can have a maximum height of 10.')

        self.size_x = size_x
        self.size_y = size_y
        self._state = [[fill_with] * size_x] * size_y

    def __getitem__(self, ij):
        i, j = ij
        return self._state[j][i]

    def __iter__(self):
        return self._state

    def __len__(self):
        return self.size_x * self.size_y

    def __str__(self):
        # Setup column guide
        out = self.pivot + self.spacer
        for i, _ in enumerate(self._state[0]):
            out += '​' + regional_indicator(i)
        out += '\n' + self.spacer * (len(self._state) + 2)

        for y, row in enumerate(self._state):
            # Setup row guide
            out += '\n' + keycap_digit(y+1) + self.spacer
            for cell in row:
                out += str(cell)

        return out