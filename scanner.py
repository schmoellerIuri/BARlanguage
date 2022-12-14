from pathlib import Path
from ply import *

'''
palavras reservadas
'''

reserved = {
	'INT'	:	'GARRAFA',
    'STRING' : 'LATAO',
    'CHAR' : 'LATA',
    'FLOAT' : 'LITRAO',
	'IF'	:	'CERVEJINHA_HOJE',
	'ELSE'	:	'VOU_NAO',
	'RETURN':	'ZEROU_POR_HOJE',
	'WHILE'	:	'MAIS_UMA',
	'PRINT' :	'DESCE_REDONDO',
	'SCAN' :	'BEBER'
}

tokens = ['LITERAL', 'ATRIB', 'OPLOGIC', 'PONTOVIRGULA', 'VIRGULA', 'ABRIRCHAVE',
 'FECHARCHAVE', 'ABRIRPAR', 'FECHARPAR', 'Nb_IN', 'Nb_FL', 'OPMAT', 'ID', 'PONTO'
 ]+ list(reserved.keys())

'''
tokens e simbolos
'''
t_OPMAT = r'(-)|(\*)|(/)|(\++)'
t_ATRIB = r'(=)'
t_OPLOGIC = r'(&&)|(\#\#)|(<=)|(>=)|(==)|(<)|(>)'
t_PONTOVIRGULA = r';'
t_VIRGULA = r','
t_ABRIRPAR = r'\('
t_FECHARPAR = r'\)'
t_ABRIRCHAVE = r'(\{)'
t_FECHARCHAVE = r'(\})'
t_PONTO = r'(\.)'
t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved.values():
        key = {i for i in reserved.keys() if reserved[i]==t.value}
        t.type = str(key).replace('{\'', '').replace('\'}','')
    return t


def t_LITERAL(t):
	r'\"([^\\\n]|(\\.))*?\"'
	return t

def t_Nb_IN(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_Nb_FL(t):
	r'[+-]?[0-9]+\.[0-9]+'
	t.value = float(t.value)
	return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Erro léxico - Caractere ilegal: '%s'" % t.value[0])
    t.lexer.skip(1)

def t_COMMENT_MONOLINE(t):
    r'//.*'
    pass
    # No return value. Token discarded

def t_code_comment(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass

lex.lex()




