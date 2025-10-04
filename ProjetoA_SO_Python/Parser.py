import os
"""Levando em conta que o Parser é apenas um unico metodo
talvez valesse a pena mover isso para o SistemaOperacional e desfazer essa classe"""
class Parser():
    def __init__(self):
        pass
    
    def lerConfigs(self, nome_arquivo):
        path = os.path.dirname(os.path.abspath(__file__))
        nome_arquivo = os.path.join(path, nome_arquivo)

        try:
            with open(nome_arquivo, 'r') as arq:
                alg_qtm = arq.readline().strip().split(';')
                linhas = [] 
                for linha in arq:
                    linhas.append(linha.strip()) 
                return alg_qtm, linhas

        except Exception as e:
            print("Erro ao ler o arquivo")   




