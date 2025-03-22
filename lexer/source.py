class Source:
    EOL = ['\n', '\r']

    def __init__(self, stream) -> None:
        self.stream = stream
        #self.check_EOL = False
        self.column = 0
        self.line = 1
        self.current_char = chr(2)
        self.get_next_char()

    def get_current_char(self) -> str:
        """Returns the current character."""
        return self.current_char
    

    def seek_next(self) -> str:
           """
           Returns the next character without changing the current position.
           """
           current_position = self.stream.tell()
           next_char = self.stream.read(1)
           self.stream.seek(current_position)
           return next_char


    
    def get_next_char(self) -> str:
        if self.current_char in self.EOL:
            self.line +=1
            self.column = 0
        if self.current_char == '':
            return self.current_char
        self.current_char = self.stream.read(1)
        if self.current_char == '\r':
            next_char = self.seek_next()
            if next_char == '\n':  # Check if next character is '\n'
                self.stream.read(1)  # skip '\n'
                self.current_char = '\n'  # Store as a single character   
            else:
                self.current_char = '\n'
        #if self.current_char != '': #and not self.check_EOL:
        self.column += 1
        #if self.check_EOL:
        #    self.line += 1
        #    self.column = 1
        #if self.get_current_char() in self.EOL: 
        #    self.check_EOL = True
        #else:
        #    self.check_EOL = False
        return self.current_char

    def get_position(self) -> tuple:
        """Returns the current position (column, row)."""
        return (self.column, self.line)

    def set_start_position(self) -> None:
        """
        Resets the stream to the beginning.
        """
        self.column = 0
        self.line = 1
        self.stream.seek(0)
        self.current_char = self.get_next_char()

    def get_line(self, line: int) -> str:
        """
        Returns the text of a specific string
        :param line: Line number (strat with 1).
        """
        current_position = self.stream.tell()
        self.stream.seek(0)
        for _ in range(line - 1):
            self.stream.readline()
        readed_line = self.stream.readline()
        self.stream.seek(current_position)
        return readed_line

    def read(self, size=-1):
        return self.stream.read(size)

    def seek(self, offset, whence=0):
        return self.stream.seek(offset, whence)

    def tell(self):
        return self.stream.tell()
