import re
from enum import Enum
import math


class TokenType(Enum):
    INVALID = 'invalid'

    INT = 'int'
    FLOAT = 'float'

    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    MOD = '%'

    DOT = '.'
    COMMA = ','

    CHAR_LITERAL = 'char'

    E = 'e'
    PI = 'pi'


class Token:
    def __init__(self, token_type: TokenType, value):
        self.token_type: TokenType = token_type
        self.value: str = value


class Tokenizer:
    def __init__(self, source: str):
        source = source.lower().replace('^', '**').replace(',', '.')
        self.source = re.sub(r'\s', '', source)
        self.token: Token | None = None

        self.tokens: list[Token] = list()

    def _gen_tokens(self) -> list[Token]:
        for char in self.source:
            self.token = Token(TokenType.INVALID, char)
            match str(char):
                case '+':
                    self.token.token_type = TokenType.ADD
                case '-':
                    self.token.token_type = TokenType.SUB
                case '*':
                    self.token.token_type = TokenType.MUL
                case '/':
                    self.token.token_type = TokenType.DIV
                case '%':
                    self.token.token_type = TokenType.MOD

                case '.':
                    self.token.token_type = TokenType.DOT
                case ',':
                    self.token.token_type = TokenType.COMMA

                case 'e':
                    self.token.token_type = TokenType.E
                case 'π':
                    self.token.token_type = TokenType.PI

                case _:
                    if not char.isdigit():
                        continue
                    self.token.token_type = TokenType.INT

            if len(self.tokens) > 0:
                last_token = self.tokens[-1]
                if last_token.token_type == self.token.token_type:
                    last_token.value += self.token.value
                    continue
                elif last_token.token_type in [TokenType.INT, TokenType.FLOAT] and \
                        self.token.token_type in [TokenType.DOT, TokenType.COMMA, TokenType.INT]:
                    if last_token.token_type == TokenType.INT:
                        last_token.token_type = TokenType.FLOAT
                    last_token.value += self.token.value
                    continue
            if self.token.token_type in [TokenType.E, TokenType.PI]:
                math_type = str(self.token.token_type).replace('TokenType.', '').lower()
                self.token = Token(TokenType.FLOAT, str(eval(f'math.{math_type}')))
            self.tokens.append(self.token)

        for token in self.tokens:
            if token.token_type == TokenType.INVALID:
                self.tokens.remove(token)
        return self.tokens

    __call__ = _gen_tokens
