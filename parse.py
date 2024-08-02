from need import need
from code_gen import CodeGenerator
from anytree import Node, RenderTree

keyword = ["if", "else", "void", "int", "repeat", "break", "until", "return"]
sym1 = ['*', ',', ';', ',', '[', ']', '{', '}', '(', ')', '+', '-', '<', '=']
file = open('syntax_errors.txt', 'w')
path = 'syntax_errors.txt'
tree = open('parse_tree.txt', 'w', encoding='utf-8')

node = Node('Program')
count = 1


def is_action_symbol(word: str):
    return word.startswith('#')


class Parser:
    def __init__(self, scanner, input, code_generator):

        self.scanner = scanner
        self.input = input
        self.code_generator = code_generator
        # self.code_generator = CodeGenerator(input)
        need.fill_needs()
        self.root = node
        self.lookahead = None
        self.unexpected_eof_reached = False

    def run(self):
        self.lookahead = self.get_next_token()
        self.call_procedure(self.root, self.root)

    def get_next_token(self):
        token = self.scanner.get_next_token(self.root, path, node)
        while not token:
            token = self.scanner.get_next_token(self.root, path, node)
        return token

    def call_procedure(self, non_terminal: Node, parent: Node):

        for rule_number in need.productions[non_terminal.name]:
            if (self.lookahead[2] in need.predict[rule_number] \
                    or self.lookahead[1] in need.predict[rule_number]):
                if self.lookahead[2] == '$':

                    Node('epsilon', non_terminal)
                    Node("$", self.root)
                    for pre, fill, node in RenderTree(self.root):
                        tree.write("%s%s\n" % (pre, node.name))
                    tree.close()
                    x = open('parse_tree.txt', 'r')
                    y = x.read()
                    x.close()
                    z = open('parse_tree.txt', 'w')
                    z.write(y[:-1])
                    z.close()
                    file.close()

                self.call_rule(non_terminal, rule_number)
                break
        else:
            if self.lookahead[2] in need.follow[non_terminal.name] or self.lookahead[1] in need.follow[
                non_terminal.name]:
                parent.children = [child for child in parent.children if child.name != non_terminal.name]
                file.write(f'#{self.lookahead[0]} : syntax error, missing {non_terminal.name}\n')

            else:
                if self.lookahead[2] == '$':
                    file.write(f'#{self.lookahead[0]} : syntax error, Unexpected EOF\n')
                    self.unexpected_eof_reached = True
                    # for child in parent.children:
                    #     child.name
                    #     print(child)
                    parent.children = [child for child in parent.children if child.name != non_terminal.name]
                    for pre, fill, node in RenderTree(self.root):
                        tree.write("%s%s\n" % (pre, node.name))
                    # Writing the modifiyed line in the file
                    tree.close()
                    x = open('parse_tree.txt', 'r')
                    y = x.read()
                    x.close()
                    z = open('parse_tree.txt', 'w')
                    z.write(y[:-1])
                    z.close()
                    file.close()
                    return

                illegal_lookahead = self.lookahead[2]
                if self.lookahead[1] in ['NUM', 'ID']:
                    illegal_lookahead = self.lookahead[1]

                file.write(f'#{self.lookahead[0]} : syntax error, illegal {illegal_lookahead}\n')
                self.lookahead = self.get_next_token()
                self.call_procedure(non_terminal, parent)

    def call_rule(self, parent, rule):
        for part in need.grammer[rule]:
            if self.unexpected_eof_reached:
                return
            if is_action_symbol(part):
                self.code_generator.call_routine(part, self.lookahead, self.input)
            elif part in need.productions.keys():
                node = Node(part, parent=parent)
                self.call_procedure(node, parent)
            else:
                self.call_match(part, parent)

    def call_match(self, expected_token, parent):
        correct = False
        if expected_token in ['NUM', 'ID']:
            if self.lookahead[1] == expected_token:
                correct = True
            else:
                correct = False
        elif (expected_token in keyword) or (expected_token == '$' or expected_token == '==' or expected_token in sym1):
            if self.lookahead[2] == expected_token:
                correct = True
            else:
                correct = False

        if correct:
            Node(f'({self.lookahead[1]}, {self.lookahead[2]})', parent=parent)
            self.lookahead = self.get_next_token()
        elif expected_token == 'EPSILON':
            Node('epsilon', parent=parent)
        elif expected_token == '$':
            Node('$', parent=parent)
        else:
            file.write(f'#{self.lookahead[0]} : syntax error, missing {expected_token}\n')

