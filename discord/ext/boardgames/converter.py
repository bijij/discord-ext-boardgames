import re

from discord.ext import commands

__all__ = ('Cell')


class Cell(commands.Converter):
    """Returns the index of a cell."""

    @classmethod
    async def convert(self, ctx: commands.Context, argument: str) -> str:
        if re.match(r'[A-z]\d+', argument):
            return (int(argument[1:]) - 1, ord(argument[0].upper()) - 65)

        raise commands.BadArgument('Could not determine cell!')
