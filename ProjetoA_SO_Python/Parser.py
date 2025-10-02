import os

class Parser():
    def __init__(self):
        pass
    
    # Cria os novos TCBs baseados no arquivo
    def criaTarefa(self, linha):
        #crio a tarefa pronta e meto na lista de prontas do SO
        print(linha)
    
    def lerConfigs(self, nome_arquivo):
        # Não sei pq mas n ta achando o arquivo na mesma pasta, então vai ter q add o caminho todo
        path = os.path.dirname(os.path.abspath(__file__))
        nome_arquivo = os.path.join(path, nome_arquivo)

        try:
            # Lê o arquivo linha linha por linha
            with open(nome_arquivo, 'r') as arq:
                # Lê a primeira linha: algoritmo_escalonamento;quantum
                # alg_qtm fica como uma lista com os dois itens
                alg_qtm = arq.readline().split()
                # Lista para conter todas as infos das tarefinhas
                linhas = [] 
                for linha in arq:
                    linhas.append(linha.strip()) # Cada linha vai ser armazenada como 1 item da lista
                return alg_qtm, linhas

        except Exception as e:
            print("Erro ao ler o arquivo")   


