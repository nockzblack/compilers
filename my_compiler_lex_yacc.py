# -----------------------------------------------------------------------------
# my_compiler_lex_yacc_.py
#
# -----------------------------------------------------------------------------


# DONE Sistema de tipos
# DONE Sistema de tipos -> Int
# DONE Sistema de tipos -> Float
# DONE Sistema de tipos -> String
# DONE Sistema de tipos -> Bolean

# DONE Operaciones
# DONE Operaciones Aritmeticas
# DONE Operaciones de Comparación
# DONE Operaciones Booleaneas
# DONE Operaciones de Bloques

# TODO Operaciones permitidas entre el sistema de tipos
# TODO Flujo de Control
# TODO Flujo de Control -> if
# TODO Flujo de Control -> else
# TODO Flujo de Control -> elif
# TODO Flujo de Control -> while
# TODO Flujo de Control -> for

# DONE ; al final de cada sentenca
# DONE Es permitido el declarar y asignar una variable en la misma linea
# TODO Arbol Sintactico
# TODO Salida Código de 3 direcciones


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
    'bool': 'BOOLDEC',
    'string': 'STRINGDEC',
    'print': 'PRINTFUNC',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
}

tokens = [
    'INUMBER', 'FNUMBER', 'NAME', 'BOOL', 'STRING', 'SEMICOLON',
    'EQUAL', 'NOTEQUAL', 'GREATERTHAN', 'LESSTHAN', 'GREATEREQUAL', 'LESSEQUAL', 'ANDAND', 'OROR',
] + list(reserved.values())


# Tokens
def t_BOOL(t):
    r'true|false'
    return t


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


def t_STRING(t):
    r'".*"'
    return t


t_SEMICOLON = r';'
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_GREATEREQUAL = r'>='
t_LESSEQUAL = r'<='
t_GREATERTHAN = r'>'
t_LESSTHAN = r'<'
t_ANDAND = r'&&'
t_OROR = r'\|\|'
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
abstractTree = []


class Node:
    val = ''
    type = ''
    children = []

    def __init__(self, val, type, children):
        self.val = val
        self.type = type
        self.children = children


def print_p(p):
    try:
        print("P[0] -> ", p[0])
        print("P[1] -> ", p[1])
        print("P[2] -> ", p[2])
        print("P[3] -> ", p[3])
        print("P[4] -> ", p[4])
    except:
        pass


def p_code(p):
    '''code : statement SEMICOLON
            | flow '''
    p[0] = p[1]


def p_block(p):
    '''block : code block
             | code '''
    p[0] = p[1]


def p_statement_declare_int(p):
    '''statement : INTDEC NAME is_assing '''
    if type(p[3]) == float:
        print("Not possible to assing float to int var")
    else:
        names[p[2]] = {"type": "INT", "value": p[3]}
        # var = Node(p[3], '=', [p[3]])
        # n = Node(p[2], 'INT', [var, p[3]])
        # abstractTree.append(n)


def p_statement_declare_float(p):
    'statement : FLOATDEC NAME is_assing'
    names[p[2]] = {"type": "FLOAT", "value": float(p[3])}


def p_statement_declare_bool(p):
    'statement : BOOLDEC NAME is_assing'
    if p[3] == "false":
        names[p[2]] = {"type": "BOOL", "value": False}
    elif p[3] == "true":
        names[p[2]] = {"type": "BOOL", "value": True}


def p_statement_declare_string(p):
    'statement : STRINGDEC NAME is_assing'
    names[p[2]] = {"type": "STRING", "value": str(p[3])}


def p_is_assing(p):
    '''is_assing : "=" expression
                | '''
    p[0] = 0
    if len(p) > 2:
        p[0] = p[2]


def p_stament_print(p):
    '''statement : PRINTFUNC '(' expression ')' '''
    print("p_stament_print")
    print(p[3])


def p_statement_assign(p):
    'statement : NAME "=" expression'
    if p[1] not in names:
        print("You must declare a var before use it")
    else:
        names[p[1]]["value"] = p[3]


def p_boolexpr_andornot(p):
    '''expression : expression ANDAND expression
                | expression OROR expression '''
    print("p_boolexpr_andornot")

    if p[2] == '&&':
        p[0] = p[1] and p[3]
    elif p[2] == '||':
        p[0] = p[1] or p[3]


def p_bool_expression_comparison(p):
    '''expression : expression EQUAL expression
                | expression NOTEQUAL expression
                | expression GREATERTHAN expression
                | expression LESSTHAN expression
                | expression LESSEQUAL expression
                | expression GREATEREQUAL expression'''

    print("p_bool_expression_comparison")

    if p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '/' expression
                  | expression '*' expression
                  | expression '^' expression '''

    print("p_expression_binop")

    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '^':
        p[0] = p[1] ** p[3]


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


def p_expression_bool(p):
    "expression : BOOL"
    print("p_expression_bool")
    p[0] = p[1]


def p_expression_string(p):
    "expression : STRING"
    print("p_expression_string")
    p[0] = p[1][1:len(p[1]) - 1]


def p_expression_name(p):
    "expression : NAME"
    print("p_expression_name")
    try:
        p[0] = names[p[1]]["value"]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_flow_if(p):
    ''' flow : IF '(' expression ')' '{' block '}' elif else '''
    p[0] = p[1]


def p_flow_elif(p):
    '''elif : ELIF '(' expression ')' '{' block '}' else
            | '''
    p[0] = p[1]


def p_flow_else(p):
    '''else : ELSE '{' block '}'
            | '''
    p[0] = p[1]


def p_error(p):
    if p:
        print(p)
        print("Syntax error at line '%s' character '%s'" %
              (p.lineno, p.lexpos))
    else:
        print("Syntax error at EOF")


yacc.yacc(debug=True)

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

"""

# File input
lines = []
with open('code.txt') as file:
    lines = file.readlines()

for line in lines:
    if line != '\n':
        yacc.parse(line)
print('Compiled successfully')
