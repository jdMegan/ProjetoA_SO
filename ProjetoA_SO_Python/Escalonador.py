from Enums import AlgoritmoEscalonamento

class Escalonador:
    def __init__(self):
        self._quantum = None
        self._alg = None

#Os tipos de algoritimo poderiam ser um ENUM, implementar isso no futuro

    #Recebe a lista de prontas, escolhe uma, retorna ela pro so por na lista de executando
    def escolherTarefa(self, listaProntas):
        # Na real nem tem um  algoritmo FSCS o nome certo é FCFS mesmo ou FIFO
        # Mas como no arquivo dele ta errado, melhor manter os dois pq nao da pra saber oq ele vai pedir no arquivo de config na apresentacao
        if self._alg == AlgoritmoEscalonamento.FCFS or self._alg == AlgoritmoEscalonamento.FSCS:
            return listaProntas.getNext()
        elif self._alg == AlgoritmoEscalonamento.PRIORIDADE_P:
            # Implementação futura
            pass
        elif self._alg == AlgoritmoEscalonamento.SRTF:
            # Implementação futura  
            pass
        return None
    
    


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

