import os
import sys
from Enums import AlgoritmoEscalonamento, CorTarefa

class Parser:
    # Tem como função ler o arquivo txt e devolver as informacoes existentes
    
    def __init__(self):
        pass
    
    def lerConfigs(self, nome_arquivo):
        # Verifica see esta rodando no executavel pyinstaller
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
        # Se não esta no vscode
            base_dir = os.path.dirname(os.path.abspath(__file__))
        nome_arquivo = os.path.join(base_dir, nome_arquivo)        

        # Verifica see esta rodando no executavel pyinstaller
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        # Se não esta no vscode
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        nome_arquivo = os.path.join(base_dir, nome_arquivo)  

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

