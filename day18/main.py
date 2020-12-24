import fileinput
import functools
import operator

digits = {str(i) for i in range(10)}

class ParseError(ValueError):
    pass

class Parser:
    """
    Parse the following grammar:

    digit          := [0-9]
    term           := digit | '(' expr ')'
    addition       := term '+' term ('+' term)*
    factor         := addition | term
    multiplication := factor '*' factor ('*' factor)*
    expr           := multiplication | addition | term

    Into an abstract syntax tree. For instance:
        5 * 4 + (3 * 2) =>
        [
          '*',
          ['int', 5],
          [
            '+',
            ['int', 4],
            [
              '*',
              ['int', 3],
              ['int', 2]
            ]
          ]
        ]
    """

    def __init__(self, string):
        self.tokens = []
        while string:
            token, string = string[0], string[1:].strip()
            self.tokens.append(token)

    def next(self, position, expected=None):
        """
        Read the next token, assert that the token is expected
        """
        try:
            token = self.tokens[position]
        except IndexError:
            raise ParseError(f'Nothing found, anything from {expected} was expected')
        if expected and not any(e == token for e in expected):
            raise ParseError(f"Unexpected '{token}', anything from {expected} was")
        else:
            return token, position + 1

    def term(self, position):
        """
        [0-9] | '(' expr ')'
        """
        token, position = self.next(position, expected=[*digits, '('])
        if token == '(':
            node, position = self.expr(position)
            _, position = self.next(position, expected=[')'])
            return node, position
        else:
            return ['int', int(token)], position

    def addition(self, position):
        """
        term '+' term ('+' term)*
        """
        nodes = []
        node, position = self.term(position)
        nodes.append(node)

        _, position = self.next(position, expected=['+'])

        node, position = self.term(position)
        nodes.append(node)

        while True:
            try:
                _, position = self.next(position, expected=['+'])
            except ParseError:
                break
            node, position = self.term(position)
            nodes.append(node)

        return ['+', *nodes], position

    def factor(self, position):
        """
        addition | term
        """
        try:
            return self.addition(position)
        except ParseError:
            return self.term(position)

    def multiplication(self, position):
        """
        factor '*' factor ('*' factor)*
        """
        nodes = []
        node, position = self.factor(position)
        nodes.append(node)

        _, position = self.next(position, expected=['*'])

        node, position = self.factor(position)
        nodes.append(node)

        while True:
            try:
                _, position = self.next(position, expected=['*'])
            except ParseError:
                break
            node, position = self.factor(position)
            nodes.append(node)

        return ['*', *nodes], position

    def expr(self, position):
        """
        multiplication | addition | term
        """
        try:
            return self.multiplication(position)
        except ParseError:
            try:
                return self.addition(position)
            except ParseError:
                return self.term(position)

    def root(self):
        """
        expr
        """
        node, position = self.expr(position=0)
        if position != len(self.tokens):
            raise ParseError(f'"{self.tokens[position:]}" is left unconsumed')
        else:
            return node

def eval(node):
    """
    Eval the resulting AST from the Parser.root
    """
    kind, *entries = node
    if kind == 'int':
        return entries[0]
    elif kind == '*':
        return functools.reduce(operator.mul, map(eval, entries))
    elif kind == '+':
        return functools.reduce(operator.add, map(eval, entries))

print(
    sum(
        eval(Parser(line.strip()).root())
        for line in fileinput.input()
    )
)
