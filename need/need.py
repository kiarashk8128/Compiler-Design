import json
import shutil

semantic_errors = []
symbol_table = dict()  # only keys are used for now
first = dict()
follow = dict()
predict = dict()
productions = dict()
grammer = dict()
input = ""
test1 = ""
test2 = ""
test3 = ""
test4 = ""
test5 = ""
test6 = ""
test7 = ""
test8 = ""
test9 = ""
test10 = ""
test11 = ""
test12 = ""
test13 = ""


def get_symbol_table_from_id(id):
    for i in symbol_table['ids']:
        if i[0] == id:
            return i


def init_symbol_table():
    symbol_table.update(
        {'keywords': ['if', 'else', 'void', 'int', 'while', 'break', 'switch',
                      'default', 'case', 'return', 'for'],
         'ids': []})


def fill_needs():
    with open('need/first.txt', 'r') as non_terminal:
        line_count = sum(1 for _ in non_terminal)

    with open('need/first.txt', 'r') as non_terminal:
        for i in range(line_count):
            line_parts = non_terminal.readline().strip().split(' ')
            first[line_parts[0]] = line_parts[1:]
    with open('need/follow.txt', 'r') as non_terminal:
        line_count = sum(1 for _ in non_terminal)

    with open('need/follow.txt', 'r') as non_terminal:
        for i in range(line_count):
            line_parts = non_terminal.readline().strip().split(' ')
            follow[line_parts[0]] = line_parts[1:]
    with open('need/predict.txt', 'r') as set:
        line_count = sum(1 for _ in set)
    with open('need/predict.txt', 'r') as set:
        for i in range(line_count):
            line_component = set.readline().strip().split(' ')
            line_num = int(line_component[0])
            predict[line_num] = line_component[1:]
    with open('need/non_terminal_lines.json', 'r') as f:
        productions.update(json.load(f))
    with open('need/grammer_for_pycharm.txt', 'r') as f:
        for idx, line in enumerate(f.readlines()):
            rhs = line.strip().split('->')[1]  # right-hand side
            grammer[idx + 1] = rhs.strip().split(' ')
    with open('need/grammer_with_action_symbols.txt', 'r') as f:
        for idx, line in enumerate(f.readlines()):
            rhs = line.strip().split('->')[1]  # right-hand side
            grammer[idx + 1] = rhs.strip().split(' ')


def save_semantic_errors(input):
    return
# def save_semantic_errors_remain(code_gen, input):
#     save_program(code_gen)
# if len(semantic_errors) == 0:
#     save_program(code_gen)
# else:
#     with open('semantic_errors.txt', 'w') as f:
#         for error in semantic_errors:
#             f.write(f'{error}\n')
#     with open('output.txt', 'w') as f:
#         f.write('The output code has not been generated.')


# def save_program(code_gen):
#     with open('semantic_errors.txt', 'w') as f:
#         f.write("The input program is semantically correct.")

# new_dict = {int(key): value for key, value in code_gen.PB.items()}
# with open('output.txt', 'w') as f:
#     for idx in sorted(new_dict.keys()):
#         f.write(f'{idx}\t{new_dict[idx]}\n')

# with open('output.txt', 'w') as f:
#     string_dict = {str(key): value for key, value in code_gen.PB.items()}
#     for idx in sorted(string_dict):
#         f.write(f'{idx}\t{string_dict}\n')
