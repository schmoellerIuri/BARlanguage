from pathlib import Path
from sintatic import parser
from scanner import lex
from error import ErrorConstants

code = file = Path("teste.txt").read_text()

lex.input(code)
for tok in iter(lex.token, None):
    print(repr(tok.type), repr(tok.value))

ErrorConstants.lineNumbers = lex.lexer.lineno

print("--------------------ERROS--------------------")    

parser.parse(code)