import fileinput
import functools
import operator

from lark import Lark

parser = Lark(
    """
    ?start: product

    ?product: sum
        | product "*" sum -> mul

    ?sum: term
        | sum "+" term -> add

    ?term: NUMBER -> number
         | "(" product ")"

    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
    """
)

def eval(ast):
    if ast.data == 'number':
        return int(ast.children[0].value)
    elif ast.data == 'add':
        return functools.reduce(operator.add, map(eval, ast.children))
    elif ast.data == 'mul':
        return functools.reduce(operator.mul, map(eval, ast.children))
    else:
        raise ValueError(ast.data)

print(
    sum(
        eval(parser.parse(line.strip()))
        for line in fileinput.input()
    )
)
