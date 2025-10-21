from Enums import AlgoritmoEscalonamento

class Escalonador:
    def __init__(self):
        self._quantum = None
        self._alg = None
        self._quantum_atual = 0 # O quantum soh se ""mexe"" se uma tarefa receber o processador, 
        # a tarefa recebe o quantum inteiro (self._quantum), e vai perdendo ele, decrementando a cada tick
        self._tar_quantum_anterior = None # Armazena a ultima tarefa q rodou no quantum,
        # sempre q zera o quantum atualiza

    #Os tipos de algoritimo poderiam ser um ENUM, implementar isso no futuro

    #Recebe a lista de prontas, escolhe uma, retorna ela pro so por na lista de executando
    def escolherTarefa(self, listaProntas):
        # Na real nem tem um  algoritmo FSCS o nome certo é FCFS mesmo ou FIFO
        # Mas como no arquivo dele ta errado, melhor manter os dois pq nao da pra saber oq ele vai pedir no arquivo de config na apresentacao
        if self._alg == AlgoritmoEscalonamento.FCFS or self._alg == AlgoritmoEscalonamento.FSCS:
            tarefa_escolhida = listaProntas.getNext()
            if self._quantum_atual > 0: # Se ainda tiver quantum, continua rodando
                self.decrementaQuantumAtual()
            # elif self._quantum_atual == 0:
            #     print(tarefa_escolhida)
            #     print("resetou o quantum")
            #     self.resetaQuantumAtual()
            return tarefa_escolhida
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
    def reajustaTarefa(self, tarefa, listaProntas): # Nome pessimo, pensar dps
        # Apos a execução/tick tem q ""tratar a tarefa"" verificar se ela continua executando ou volta para o final da fila de prontas
        # Se ainda estiver no quatum, bota ela no inicio da fila denovo
        if self._alg == AlgoritmoEscalonamento.FCFS or self._alg == AlgoritmoEscalonamento.FSCS:
            print('entrou no REAJUSTE \n')
            print("o quantum agr é: ", self._quantum_atual)
            if(self._quantum_atual == 0): #atualiza a ultima tarefa
                self._tar_quantum_anterior = tarefa
            # Se ainda tiver quantum e ela nao foi a ultima a executar
            print("self._tar_quantum_anterior=", self._tar_quantum_anterior)
            print((self._quantum_atual <= self._quantum) & (tarefa is not self._tar_quantum_anterior))
            if (self._quantum_atual <= self._quantum) & (tarefa is not self._tar_quantum_anterior):
                listaProntas.addFirstTask(tarefa)
            else:
                if(tarefa.duracaoRestante > 0):
                    listaProntas.addTask(tarefa)
                print("resetou o quantum em baixooooo")
                self.resetaQuantumAtual()
                print(self._quantum_atual)
        elif self._alg == AlgoritmoEscalonamento.PRIORIDADE_P:
            # Implementação futura
            pass
        elif self._alg == AlgoritmoEscalonamento.SRTF:
            # Implementação futura 
            pass
        return None
        
    def decrementaQuantumAtual(self):
        self._quantum_atual -= 1
    
    def resetaQuantumAtual(self):
        self._quantum_atual = self._quantum

    def atualizaTarQuantumAnterior(self, tarefa):
        self._tar_quantum_anterior = tarefa
            
    
    

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
    


