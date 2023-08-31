import re
from collections import namedtuple

class Token(namedtuple("Token", ["n", "token", "raw"])):
    RE_SPACE = r"sp"
    RE_BACKSLASH = r"bS"
    RE_SINGLEQUOTE = r"sQ"
    RE_NEWLINE = r"nl"
    TOKENS = [RE_SPACE, RE_BACKSLASH, RE_SINGLEQUOTE, RE_NEWLINE, r"\S"]
    RE_TOKENS = r"|".join(TOKENS)
    RE_CAPTUREPATTERN = fr"((?P<number>\d*)(?P<token>{RE_TOKENS}))"
    TOKEN_MAP = {
        "sp": " ",
        "bS": "\\",
        "sQ": "'",
        "nl": "\n",
    }

    @classmethod
    def TokensFromString(cls, string):
        matches = re.finditer(cls.RE_CAPTUREPATTERN, string)
        return [cls.fromMatch(m) for m in matches]

    @classmethod
    def fromMatch(cls, m):
        n = m.group('number')
        t = m.group('token')
        if n:
            n = int(n)
        elif not n and t == cls.RE_NEWLINE:
            n = 1
        return cls(n, t, m.string[m.start():m.end()])
    
    def __str__(self):
        if self.token in self.TOKEN_MAP:
            return self.n * self.TOKEN_MAP[self.token]
        else:
            return self.n * self.token

t = input()
tokens = Token.TokensFromString(t)
print("".join(map(str, tokens)))
