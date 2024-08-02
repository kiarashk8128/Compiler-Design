import need.need
from scanner import Scanner
from parse import Parser
from code_gen import CodeGenerator
import test 


def run_compiler():
    scanner = Scanner(input)
    code_generator = CodeGenerator(input)
    parse = Parser(scanner, input, code_generator)
    parse.run()



input = 'input.txt'


if __name__ == '__main__':
    run_compiler()
