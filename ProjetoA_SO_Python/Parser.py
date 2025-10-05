import os
from Enums import AlgoritmoEscalonamento, CorTarefa

class Parser:
    def __init__(self):
        pass
    
    def lerConfigs(self, nome_arquivo):
        path = os.path.dirname(os.path.abspath(__file__))
        nome_arquivo = os.path.join(path, nome_arquivo)

        try:
            with open(nome_arquivo, 'r') as arq:
                # Lê algoritmo e quantum
                alg_str, quantum_str = arq.readline().strip().split(';')
                # Converte para Enum e int
                algoritmo = AlgoritmoEscalonamento(alg_str)
                quantum = int(quantum_str)
                
                # Em linhas ficam as linhas com as tasks
                linhas = [] 
                for linha in arq:
                    linhas.append(linha.strip()) 
                return [algoritmo, quantum], linhas

        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return None, None
