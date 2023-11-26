from ast_parser import ASTParser

class BaseOperator():

    def __init__(self, language: str):

        self.parser = ASTParser() 
        self.parser.set_language(language)
       
    def parse(self, code_snippet):
        tree = self.parser.parse(bytes(code_snippet, "utf8"))
        return tree