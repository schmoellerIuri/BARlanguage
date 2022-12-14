import sys

import ply.yacc as yacc
from scanner import tokens
import error

class SemanticErrorConstants:
    errorThrown = False

# Parsing rules
precedence = (
    ('left','ABRIRPAR','FECHARPAR'),
    ('left','OPLOGIC'),
    ('left','OPMAT'),
    )

#nomes de variaveis declaradas
nomes = []

def p_empty(p):
    'empty :'
    pass

def p_fim_de_instrucao(p):
    'fim_de_instrucao : PONTOVIRGULA'

def p_literal(p):
    '''literal : numero
               | LITERAL
                '''

def p_numero(p):
    '''numero : Nb_IN
              | Nb_IN PONTO Nb_IN'''

def p_programa(p):
    'programa : sequencia_declaracoes'

def p_tipo(p):
    '''tipo : CHAR
            | FLOAT
            | STRING
            | INT'''

def p_sequencia_declaracoes(p):
    '''sequencia_declaracoes : declaracao sequencia_declaracoes
                             | declaracao'''

def p_declaracao(p):
    '''declaracao : funcao
                  | declaracao_variavel'''

def p_declaracao_variavel(p):
    '''declaracao_variavel : tipo sequencia_especificacao_var fim_de_instrucao'''

def p_lista_declaracao_var(p):
    '''lista_declaracao_var : declaracao_variavel lista_declaracao_var
                            | empty'''

def p_especificacao_var(p):
    '''especificacao_var : ID ATRIB expressao
                         | ID'''
    if(p[1] not in nomes):
        nomes.append(p[1])
    elif len(p) > 2:
        error.SameNameError(p)

def p_sequencia_especificacao_var(p):
    '''sequencia_especificacao_var : especificacao_var VIRGULA sequencia_especificacao_var
                                   | especificacao_var'''

def p_parametro(p):
    '''parametro : tipo ID'''
    nomes.append(p[2])

def p_lista_parametro(p):
    '''lista_parametro : sequencia_parametro
                       | empty'''

def p_sequencia_parametro(p):
    '''sequencia_parametro : parametro VIRGULA sequencia_parametro
                           | parametro'''

def p_funcao(p):
    '''funcao : tipo ID ABRIRPAR lista_parametro FECHARPAR ABRIRCHAVE bloco_codigo FECHARCHAVE'''

def p_expressao(p):
    'expressao : ABRIRPAR expressao FECHARPAR'

def p_expressao_literal(p):
    'expressao : literal'

def p_expressao_variavel(p):
    'expressao : ID'
    if(p[1] not in nomes and not SemanticErrorConstants.errorThrown):
        SemanticErrorConstants.errorThrown = True
        print("Erro semântico - Variavel '%s' não declarada na linha %d" % (p[1],p.lineno(1) - error.ErrorConstants.lineNumbers))

def p_expressao_funcao(p):
    'expressao : chamada_funcao'

def p_expressao_logica(p):
    '''expressao : expressao OPLOGIC expressao'''

def p_expressao_matematica(p):
    '''expressao : expressao OPMAT expressao'''

def p_define_subchamada_expressao(p):
    'expressao : subchamada_expressao fim_de_instrucao'

def p_lista_expressao(p):
    '''lista_expressao : sequencia_expressao
                        | empty'''

def p_sequencia_expressao(p):
    '''sequencia_expressao : expressao VIRGULA sequencia_expressao
                           | expressao'''

def p_atribuicao(p):
    '''atribuicao : ID ATRIB expressao'''
    if(p[1] not in nomes and not SemanticErrorConstants.errorThrown):
        SemanticErrorConstants.errorThrown = True
        print("Erro semântico - Variavel '%s' não declarada na linha %d" % (p[1],p.lineno(1)-error.ErrorConstants.lineNumbers))
    
def p_chamada_funcao(p):
    '''chamada_funcao : ID ABRIRPAR sequencia_especificacao_var FECHARPAR'''
    
def p_estrutura(p):
    '''estrutura : condicional
                 | repeticao
                 | retorno
                 | atribuicao fim_de_instrucao
                 | subchamada_expressao fim_de_instrucao
                 | escrever fim_de_instrucao
                 | ler fim_de_instrucao
                 | chamada_funcao fim_de_instrucao'''

def p_lista_estrutura(p):
    '''lista_estrutura : estrutura lista_estrutura
                       | empty'''

def p_condicional(p):
    '''condicional : IF ABRIRPAR expressao FECHARPAR ABRIRCHAVE bloco_codigo FECHARCHAVE
                   | IF ABRIRPAR expressao FECHARPAR ABRIRCHAVE bloco_codigo FECHARCHAVE ELSE ABRIRCHAVE bloco_codigo FECHARCHAVE'''

def p_repeticao(p):
    '''repeticao : WHILE ABRIRPAR expressao FECHARPAR ABRIRCHAVE bloco_codigo FECHARCHAVE'''

def p_retorno(p):
    '''retorno : RETURN fim_de_instrucao
               | RETURN expressao fim_de_instrucao'''

def p_subchamada_expressao(p):
    '''subchamada_expressao : ID ABRIRPAR lista_expressao FECHARPAR'''

def p_escrever(p):
    '''escrever : PRINT ABRIRPAR lista_expressao FECHARPAR'''

def p_ler(p):
    '''ler : SCAN ABRIRPAR ID FECHARPAR'''
    if(p[3] not in nomes and not SemanticErrorConstants.errorThrown):
        SemanticErrorConstants.errorThrown = True
        print("Erro semântico - Variavel '%s' não declarada na linha %d" % (p[3],p.lineno(3)-error.ErrorConstants.lineNumbers))

def p_bloco_codigo(p):
    '''bloco_codigo : lista_declaracao_var lista_estrutura'''

def p_error(t):
        parser.errok()
        error.unknownError(t)

def p_var_declaration_error(p):
    'declaracao_variavel : tipo especificacao_var'
    error.NoSemicolonError(p)


parser=yacc.yacc(start='programa')