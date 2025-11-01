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
                # Verifica qual eh o algoritmo correspondente, de for FIFO e tem quantum == RR
                if self.alteraAlgoritmo(algoritmo, quantum):
                    algoritmo = self.alteraAlgoritmo(algoritmo, quantum)
                # Em linhas ficam as linhas com as tasks
                linhas = [] 
                for linha in arq:
                    linhas.append(linha.strip()) 
                return [algoritmo, quantum], linhas

        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return None, None

    def alteraAlgoritmo(self, algoritmo, quantum):
        if (algoritmo == AlgoritmoEscalonamento.FCFS) & (quantum > 0):
            return AlgoritmoEscalonamento.ROUND_ROBIN
        # Existem outros casos tipo o SJF, mas como nao vamos implementar esses
        # Só altera se for o fifo com quatum msm
        return False        

