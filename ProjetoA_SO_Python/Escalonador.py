from Enums import AlgoritmoEscalonamento

class Escalonador:
    def __init__(self):
        self._quantum = None
        self._alg = None
        self._quantum_atual = 0

#Os tipos de algoritimo poderiam ser um ENUM, implementar isso no futuro

    #Recebe a lista de prontas, escolhe uma, retorna ela pro so por na lista de executando
    def escolherTarefa(self, listaProntas):
        # Na real nem tem um  algoritmo FSCS o nome certo é FCFS mesmo ou FIFO
        # Mas como no arquivo dele ta errado, melhor manter os dois pq nao da pra saber oq ele vai pedir no arquivo de config na apresentacao
        if self._alg == AlgoritmoEscalonamento.FCFS or self._alg == AlgoritmoEscalonamento.FSCS:
            self._quantum_atual += 1
            return listaProntas.getNext()
        elif self._alg == AlgoritmoEscalonamento.PRIORIDADE_P:
            # N espera o pelo quantum acabar, se entrar alguma tarefa, ela preempta a outra
            # Implementação futura
            pass
        elif self._alg == AlgoritmoEscalonamento.SRTF:
            # Implementação futura  
            pass
        return None
    
    # Cada algoritmo vai ter um jeito de lidar com a tarefa por tick
    # Por exemplo, no FIFO ele soh checa se ainda tem tempo no quantum e mantem, se nao tiver, e volta para o final da fila de prontas    
    def reajustaTarefaFCFS(self, tarefa, listaProntas): # Nome pessimo, pensar dps
        # Apos a execução tem q ""tratar a tarefa"" verificar se ela continua executando ou volta para o final da fila de prontas
        # Se ainda estiver no quatum, bota ela no inicio denovo
        print('entrou no REAJUSTE \n')
        if self._quantum_atual < self._quantum:
            listaProntas.addFirstTask(tarefa)
            print("after reajsute lista de PROINTAS = ", listaProntas)
        else:
            self._quantum_atual = 0
            
    

    # Getters e setters
    @property 
    def quantum(self):
        return self._quantum
    @quantum.setter
    def quantum(self, quantum):
        self._quantum = quantum

    @property 
    def alg(self):
        return self._alg
    @alg.setter
    def alg(self, alg):
        self._alg = alg

