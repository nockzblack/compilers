# -----------------------------------------------------------------------------
# my_compiler_lex_yacc_.py
#
# -----------------------------------------------------------------------------

import ply.yacc as yacc
import ply.lex as lex
import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
    'NAME', 'INUMBER', 'FNUMBER', 'INTDEC', 'FLOATDEC', 'PRINTFUNC'
)

literals = ['=', '+', '-', '(', ')']

# Tokens
t_INTDEC = r'int'
t_FLOATDEC = r'float'
t_PRINTFUNC = r'print'
t_NAME = r'[a-eg-hj-oq-z]'

# FIXME: there is a bug on vars that are in the tokens strings


def t_FNUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}


def p_statement_declare_int(p):
    'statement : INTDEC NAME'
    names[p[2]] = {"type": "INT", "value": 0}


def p_statement_declare_float(p):
    'statement : FLOATDEC NAME'
    names[p[2]] = {"type": "FLOAT", "value": 0}


def p_stament_print(p):
    '''statement : PRINTFUNC '(' expression ')' '''
    print(p[3])


def p_statement_assign(p):
    'statement : NAME "=" expression'
    if p[1] not in names:
        print("You must declare a var before use it")
    else:
        names[p[1]]["value"] = p[3]


def p_statement_expr(p):
    'statement : expression'
    # print(p[1])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_inumber(p):
    "expression : INUMBER"
    print("Integer")
    p[0] = p[1]


def p_expression_fnumber(p):
    "expression : FNUMBER"
    print("Float")
    p[0] = p[1]


def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]["value"]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


yacc.yacc()

""" 
# Read file and compile
f = open("code.txt")
code = f.read()
yacc.parse(code)
"""

# Module to read from comamnd line
while 1:
    try:
        s = raw_input('compiler > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)
