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

literals = ['=', '+', '-', '*', '/', '(', ')']
reserved = {
    'int': 'INTDEC',
    'float': 'FLOATDEC',
    'print': 'PRINTFUNC'
}

tokens = [
    'INUMBER', 'FNUMBER', 'NAME'
] + list(reserved.values())


# Tokens
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')    # Check for reserved words
    return t


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
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}


def print_p(p):
    try:
        print("P[0] -> ", p[0])
        print("P[1] -> ", p[1])
        print("P[2] -> ", p[2])
        print("P[3] -> ", p[3])
    except:
        pass


def p_statement_declare_int(p):
    '''statement : INTDEC NAME is_assing '''
    print("p_statement_declare_int")
    names[p[2]] = {"type": "INT", "value": p[3]}


def p_statement_declare_float(p):
    'statement : FLOATDEC NAME'
    names[p[2]] = {"type": "FLOAT", "value": 0}


def p_is_assing(p):
    '''is_assing : "=" expression 
                | '''
    p[0] = 0
    if len(p) >= 2:
        p[0] = p[2]


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
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_inumber(p):
    "expression : INUMBER"
    p[0] = p[1]


def p_expression_fnumber(p):
    "expression : FNUMBER"
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
        print(p)
        print("Syntax error at line '%s' character '%s'" %
              (p.lexpos, p.lineno))
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
