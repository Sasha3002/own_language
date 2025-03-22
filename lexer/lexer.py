from lexer.tokens import Token, TokenType, Symbol
from lexer.source import Source
from errors.errors import InvalidTokenError, ExceedsMaxLengthError, UndefEscapeChar


class Lexer:
    def __init__(self, source, #is_file: bool = False, 
                 max_int_length: int = 15, 
                 max_float_length: int = 15, 
                 max_string_length: int = 10 ** 5) -> None:
        """
        Initializes the token with the specified data source.
        
        :param source: The data source (file or string).
        :param is_file: Whether the source is a file.
        :param max_int_length: The maximum length of the integer.
        :param max_float_length: The maximum length of a floating point number.
        :param max_string_length: Maximum length of the string.
        """
        self.source = source
        self.MAX_INT_LENGTH = max_int_length
        self.MAX_FLOAT_LENGTH = max_float_length
        self.MAX_STRING_LENGTH = max_string_length

   


    def _try_build_identifier(self) -> Token:
        if self.source.get_current_char().isalpha():
            builder = []
            position = self.source.get_position()
            while self.source.get_current_char().isalnum() or self.source.get_current_char() == '_':
                if len(builder) >= self.MAX_STRING_LENGTH:
                    raise ExceedsMaxLengthError(self.source.get_position()[0], self.source.get_position()[1], 'Identifier')
                builder.append(self.source.get_current_char())
                self.source.get_next_char()
            value = ''.join(builder)
            return Token(type=Symbol.keywords.get(value, TokenType.IDENTIFIER), value=value, pos=position)
 


    def _parse_escape_sequence(self) -> str:
        self.source.get_next_char()  # Read the next character after '\'
        match self.source.get_current_char():
            case 'n':
                return '\n'
            case 't':
                return '\t'
            case '\\':
                return '\\'
            case '"':
                return '\"'
            case "'":
                return "\'"
            case _:
                raise UndefEscapeChar(self.source.get_position()[0], self.source.get_position()[1], self.source.get_current_char())
                # If the character is not supported throw an error
                #raise ValueError(f"Unsupported escape sequence: \\{self.source.get_current_char()}")
            
    def _try_build_string(self) -> Token:
        if self.source.get_current_char() == '"':
            builder = []
            position = self.source.get_position()
            self.source.get_next_char()  # skip onen '
            while self.source.get_current_char() != '"' and self.source.get_current_char() != '':
                if len(builder) >= self.MAX_STRING_LENGTH:
                    raise ExceedsMaxLengthError(self.source.get_position()[0], self.source.get_position()[1], 'String')
                if self.source.get_current_char() == '\\':
                    char_to_add = self._parse_escape_sequence()
                else:
                    char_to_add = self.source.get_current_char()
                builder.append(char_to_add)
                self.source.get_next_char()
            if self.source.get_current_char() != '"':
                raise ValueError('String not closed')
            self.source.get_next_char()  # skip closing '
            value = ''.join(builder)
            return Token(type=TokenType.STRING_VALUE, value=value, pos=position)

    def _try_build_comment(self) -> Token:
        if self.source.get_current_char() == '#':
            builder = []
            position = self.source.get_position()
            self.source.get_next_char()
            while self.source.get_current_char() != '\n' and self.source.get_current_char() != '':
                if len(builder) >= self.MAX_STRING_LENGTH:
                    raise ExceedsMaxLengthError(self.source.get_position()[0], self.source.get_position()[1], 'Comment')
                builder.append(self.source.get_current_char())
                self.source.get_next_char()
            value = ''.join(builder)
            return Token(type=TokenType.COMMENT, value=value, pos=position)


    def _try_build_number(self) -> Token:
        if self.source.get_current_char().isdecimal():
            builder = []
            position = self.source.get_position()
            while self.source.get_current_char().isdecimal(): #mamy budowac watrosc int przez obecna wart *10 + next wart
                if len(builder) >= self.MAX_INT_LENGTH:
                    raise ExceedsMaxLengthError(self.source.get_position()[0], self.source.get_position()[1], 'Integer')
                builder.append(self.source.get_current_char())
                self.source.get_next_char()
            if self.source.get_current_char() == '.':
                builder.append(self.source.get_current_char())
                self.source.get_next_char()
                while self.source.get_current_char().isdecimal():
                    if len(builder) >= self.MAX_FLOAT_LENGTH:
                        raise ExceedsMaxLengthError(self.source.get_position()[0], self.source.get_position()[1], 'Float')
                    builder.append(self.source.get_current_char())
                    self.source.get_next_char()
                return Token(type=TokenType.FLOAT_VALUE, value=float(''.join(builder)), pos=position)
            return Token(type=TokenType.INT_VALUE, value=int(''.join(builder)), pos=position)


    def _try_build_chars(self) -> Token:
        value = self.source.get_current_char() + self.source.seek_next()
        position = self.source.get_position()
        if token_type:= Symbol.double_chars.get(value):
            self.source.get_next_char()
            self.source.get_next_char()
        elif token_type:= Symbol.chars.get(self.source.get_current_char()):
            value = self.source.get_current_char()
            self.source.get_next_char()
        else:
            return None
        return Token(type=token_type, value=value, pos=position)

    def _try_build_eof(self) -> Token:
        if self.source.get_current_char() == '':
            position = (self.source.get_position()[0] + 1, self.source.get_position()[1])
            return Token(type=TokenType.EOF, value=None, pos=position)

    def get_next_token(self) -> Token:
        while (self.source.get_current_char().isspace()):
            self.source.get_next_char()
        for fun in [self._try_build_identifier,
                    self._try_build_string,
                    self._try_build_comment,
                    self._try_build_number,
                    self._try_build_chars,
                    self._try_build_eof]:
            token = fun()
            if token:
                return token
        raise InvalidTokenError(self.source.get_position()[0], self.source.get_position()[1], self.source.get_current_char())

    def get_all_tokens(self) -> list[Token]:
        self.source.set_start_position()
        tokens = []
        token = self.get_next_token()
        while token.type != TokenType.EOF:
            tokens.append(token)
            token = self.get_next_token()
        tokens.append(token)
        return tokens
