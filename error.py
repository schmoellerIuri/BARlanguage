import ply.yacc as yacc

class ErrorConstants:
    lineNumbers = 0
    errorThrown = False

def unknownError(t):
    if ErrorConstants.errorThrown: return
    if t:
         print("Erro sintatico próximo a '%s', na linha %d" % (t.value, t.lineno - ErrorConstants.lineNumbers))
         ErrorConstants.errorThrown = True
    else:
         print("Erro sintatico próximo a EOF")
         raise SystemExit

def NoSemicolonError(t):
    print("Erro sintático - Falta de ponto e vírgula, próximo a linha %d" % (t.lexer.lineno - ErrorConstants.lineNumbers))

def SameNameError(t):
    print("Erro semântico - Variaveis com o mesmo nome em '%s', próximo a linha %d" % (t[1], t.lineno(1) - ErrorConstants.lineNumbers))