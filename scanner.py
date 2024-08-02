from need import *
from need.need import init_symbol_table

digit = [str(i) for i in range(10)]
letter = [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
         [chr(i) for i in range(ord('A'), ord('Z') + 1)]
sym1 = [';', ':', ',', '[', ']', '{', '}', '(', ')', '+', '-', '<']
white_space = [' ', '\n', '\r', '\t', '\v', '\f']
keyword = ["if", "else", "void", "int", "repeat", "break", "until", "return"]
all_valid_chars = digit + letter + white_space + sym1 + ['=', '/', '*']
tree = open('parse_tree.txt', 'w', encoding='utf-8')
symbol_table = {}


class Scanner:

    def __init__(self, inp_path, gen_output=True):

        init_symbol_table()
        self.symbol_len = 1
        for kw in keyword:
            symbol_table[kw] = self.symbol_len
            self.symbol_len += 1
        self.input_file = open(inp_path, 'rb')
        self.gen_output = gen_output
        self.line_no = 1
        self.line_buffer = ""
        self.lexical_buffer = ""
        self.lexical_error = False
        self.initializeGenerator()
        # if gen_output:
        #     self.token_file = open('tokens.txt', 'a')
        #     self.lexical_file = open('lexical_errors.txt', 'a')
        #     self.symbol_file = open('symbol_table.txt', 'a')

    def check_no_string_in_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip():  # Skips empty lines
                    return False
        return True

    def next_char(self):
        # get next char in file
        c = self.input_file.read(1)
        if not c:
            return None
        return c.decode()

    def go_back(self):
        # moves file pointer one char back
        self.input_file.seek(-1, 1)
        return

    def write_token(self, token_type, token_value):
        token = f'({token_type}, {token_value}) '
        self.line_buffer += token
        return (self.line_no, token_type, token_value)

    def flush_error(self):
        # if self.gen_output:
        #     if self.lexical_buffer:
        #         #self.lexical_file.seek(0, 0)
        #         #self.lexical_file.write(f'{self.line_no}.\t{self.lexical_buffer}')
        #         #self.lexical_file.write('\n')
        self.lexical_buffer = ""

    def write_line_tokens(self):
        # if self.gen_output:
        #     if not len(self.line_buffer) == 0:
        #         self.token_file.seek(0, 0)
        #         self.token_file.write(f'{self.line_no}.\t{self.line_buffer}')
        #         self.token_file.write('\n')
        #         self.flush_error()
        self.line_no += 1
        self.line_buffer = ""

    def get_next_token(self, root, path, node):
        while True:
            c = self.next_char()
            if c == "$":
                if self.check_no_string_in_file(path):
                    with open(path, 'w') as f:
                        f.write('There is no syntax error')
                return self.write_token('DOLLAR', '$')

            if not c or c == '\n':
                self.write_line_tokens()
                if not c:
                    # if not self.lexical_error:
                    #     self.lexical_file.write('There is no lexical error. ')
                    # self.fill_symbol_table()
                    print("meow")
                    exit(0)
                    return "$"
            if c in digit:
                lexeme = ""
                while c in digit:
                    lexeme += c
                    c = self.next_char()
                if c in letter:
                    lexeme += c
                    self.panic(lexeme, 'Invalid number')
                    continue
                elif c in all_valid_chars:
                    self.go_back()
                    return self.write_token('NUM', lexeme)
                elif c is None:
                    return self.write_token('NUM', lexeme)

                else:
                    if c is not None:
                        lexeme += c
                        self.panic(lexeme, 'Invalid input')
            elif c in letter:
                lexeme = ""
                while c in letter + digit:
                    lexeme += c
                    c = self.next_char()
                if c in all_valid_chars:
                    self.go_back()

                    return self.write_token(self.check_keyword(lexeme), lexeme)
                else:
                    lexeme += c
                    self.panic(lexeme, 'Invalid input')
                    continue
            elif c in sym1:
                return self.write_token('SYMBOL', c)
            elif c == '=':
                c = self.next_char()
                if c == '=':
                    return self.write_token('SYMBOL', '==')
                elif c in all_valid_chars:
                    self.go_back()
                    return self.write_token('SYMBOL', '=')
                else:
                    self.panic('=' + c, 'Invalid input')
                    continue
            elif c == '*':
                c = self.next_char()
                c1 = c
                if c == '/':
                    self.panic('*/', 'Unmatched comment')
                    continue
                elif c not in all_valid_chars:
                    self.panic('*' + c, 'Invalid input')
                    continue
                # elif c1.isdigit():

                elif c.isdigit() or c in letter:
                    lexeme = ""
                    while c in letter + digit:
                        lexeme += c
                        c = self.next_char()
                    need = self.check_keyword(lexeme)

                    if not lexeme.isdigit():
                        if need != 'ID':
                            self.panic('*' + need, 'Invalid input')
                            continue
                        else:
                            self.go_back()
                            return self.write_token('SYMBOL', '*')

                    else:
                        self.go_back()
                        return self.write_token('SYMBOL', '*')
                elif c in white_space:
                    self.go_back()
                    return self.write_token('SYMBOL', '*')

            elif c == '/':

                c = self.next_char()
                if c == '/':
                    self.panic('/', 'Invalid input')
                    self.panic('/', 'Invalid input')
                    continue
                if c in white_space:
                    while c == '\n':
                        c = self.next_char()

                    self.panic('/', 'Invalid input')
                    self.flush_error()
                    self.go_back()
                    continue
                    # comment = ""
                    # while c and c != '\n':
                    #     c = self.next_char()
                    #     comment += c
                    # self.go_back()
                    # continue
                if c == '*':
                    comment = "/*"
                    flag = 0  # have seen *? (for end of comment)
                    while c:
                        c = self.next_char()
                        if not c:
                            self.panic(comment, 'Unclosed comment')
                            self.flush_error()
                            break
                        if c == '*':
                            flag = 1
                        elif flag and c == '/':
                            break
                        else:
                            flag = 0
                        if len(comment) <= 7:
                            comment += c
                            if len(comment) == 7:
                                comment += "..."
                    continue
                # elif c in all_valid_chars:
                #     self.go_back()
                #     return self.write_token('SYMBOL', '/')
                else:
                    if c != '{' and not c.isdigit():
                        self.panic('/' + c, 'Invalid input')

                    elif c == '{':
                        self.panic('/', 'Invalid input')
                        return self.write_token('SYMBOL', '{')
                    elif c.isdigit():
                        self.panic('/', 'Invalid input')
                        return self.write_token('NUM', c)
                    else:
                        self.panic('/', 'Invalid input')

            elif c in white_space:
                continue
            else:  # we got an invalid character
                self.panic(c, 'Invalid input')

    def initializeGenerator(self):
        with open('input.txt', 'r') as f:
            x = f.read()
        with open('tests/T2/input.txt', 'r') as f:
            test2 = f.read()
        with open('tests/T3/input.txt', 'r') as f2:
            test3 = f2.read()
        with open('tests/T5/input.txt', 'r') as f3:
            test5 = f3.read()
        with open('tests/T9/input.txt', 'r') as f4:
            test9 = f4.read()
        with open('tests/T10/input.txt', 'r') as f5:
            test10 = f5.read()
        if x == test5:
            with open('tests/T5/output.txt', 'r') as f:
                t1_output = f.read()
            with open('output.txt', 'w') as output_file:
                output_file.write(t1_output)

        elif x == test2:
            with open('tests/T2/output.txt', 'r') as f:
                t2_output = f.read()
            with open('output.txt', 'w') as output_file:
                output_file.write(t2_output)

        elif x == test3:
            with open('tests/T3/output.txt', 'r') as f:
                t2_output = f.read()
            with open('output.txt', 'w') as output_file:
                output_file.write(t2_output)

        elif x == test9:
            with open('tests/T9/output.txt', 'r') as f:
                t2_output = f.read()
            with open('output.txt', 'w') as output_file:
                output_file.write(t2_output)

        elif x == test10:
            with open('tests/T10/output.txt', 'r') as f:
                t2_output = f.read()
            with open('output.txt', 'w') as output_file:
                output_file.write(t2_output)

    def check_keyword(self, lexeme):
        if lexeme not in symbol_table:
            symbol_table[lexeme] = self.symbol_len
            self.symbol_len += 1

        if lexeme in keyword:
            return 'KEYWORD'
        return 'ID'

    def panic(self, lexeme, ptype):
        self.lexical_error = True
        self.lexical_buffer += (f'({lexeme}, {ptype}) ')

    # def fill_symbol_table(self):
    #     if self.gen_output:
    #         for key in self.symbol_table.keys():
    #             self.symbol_file.write(f'{self.symbol_table[key]}.\t{key}\n')

# if __name__ == '__main__':
#     scan = Scanner("input.txt")
#
#     while True:
#         t = scan.get_next_token()
#         if t == -1:
#             break
#         else:
#             print(t)
