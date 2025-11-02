from Enums import AlgoritmoEscalonamento

class Escalonador:
    def __init__(self):
        self._quantum = None
        self._alg = None

    def escolherTarefa(self, listaProntas, tarefaExecutando):
        # Define de acordo com cada algoritmo qual a proxima
        # tarefa a ser executada
        if self._alg == AlgoritmoEscalonamento.FCFS:
            if( tarefaExecutando is None or tarefaExecutando.estaConcluida()):
                return listaProntas.getNext()
            return tarefaExecutando

        elif self._alg == AlgoritmoEscalonamento.ROUND_ROBIN:
            #Se não tem tarefa executando, ou ela concluiu, pega a proxima
            if (tarefaExecutando is None or tarefaExecutando.estaConcluida() ):
                return listaProntas.getNext()
            
            # Tem tarefa executando não concluida, mas acabou o quantum
            # Volta pra fila e pega a proxima
            elif tarefaExecutando.passouQuantum(self._quantum):
                tarefaExecutando.resetQuantum()
                listaProntas.addTask(tarefaExecutando)
                return listaProntas.getNext()
            
            #Se tem tarefa, não concluida, com quantum, continua
            else:
                return tarefaExecutando


        elif self._alg == AlgoritmoEscalonamento.SRTF:
            # Tem tarefa e ela terminou
            # Ela some
            if tarefaExecutando and tarefaExecutando.estaConcluida():
                tarefaExecutando = None 
                
            #Lista de todas as tarefas          
            todas = listaProntas.getAll()

            #Caso a tarefa não tenha sido concluida ela entra para a consideração
            tarefa_anterior = tarefaExecutando
            if tarefa_anterior:
                todas.append(tarefa_anterior)
                
            #Se não tem tarefa para considerar retorna none
            if not todas:
                return None 

            # Checando a menor duração
            # t.ingresso para caso de empate
            tarefa_menor_dur = min(todas, key=lambda t: (t.duracaoRestante, t.ingresso))
            
            # Se a tarefa escolhida é a mesma que já estava na CPU, não faz nada.
            if tarefa_menor_dur == tarefa_anterior:
                return tarefa_anterior       
                    
            # Se não, troca 
            # Se a tarefa q perdeu o processador ainda existe, ela volta pra prontas
            if tarefa_anterior is not None:
                if not tarefa_anterior.estaConcluida():
                    tarefa_anterior.estado = "pronta"
                    listaProntas.addTask(tarefa_anterior)

                # A nova tarefa n pode ficar na fila e na CPU
            if listaProntas.contem(tarefa_menor_dur):
                listaProntas.removeTask(tarefa_menor_dur)
            return tarefa_menor_dur


        elif self._alg == AlgoritmoEscalonamento.PRIORIDADE_P:
            # Tem tarefa e ela terminou
            # Ela some
            if tarefaExecutando and tarefaExecutando.estaConcluida():
                tarefaExecutando = None
            
            #Atualiza ista de todas as tarefas  
            todas = listaProntas.getAll()
            if tarefaExecutando:
                todas.append(tarefaExecutando)
            if not todas:
                return None
            
            # Pega a maior prioridade independendo de ingrasso, quantum, etc.
            # Tem q dar um jeito de fazer com q em caso de empate escolha a com id menor ?
            tarefa_maior_prio = max(todas, key=lambda t: t.prioridade)
            
            # Se a tarefa escolhida é a mesma que já estava na CPU, não faz nada.
            if tarefa_maior_prio == tarefaExecutando:
                return tarefaExecutando
            
            # Se a melhor tarefa é dif da que esta executando eh pq teve preempcao            
            if tarefaExecutando is not None:
                if not tarefaExecutando.estaConcluida():
                    tarefaExecutando.estado = "pronta"
                    listaProntas.addTask(tarefaExecutando) # Volta para a fila de pronta
            
            # A nova tarefa n pode ficar na fila e na CPU
            if listaProntas.contem(tarefa_maior_prio):
                listaProntas.removeTask(tarefa_maior_prio)
            return tarefa_maior_prio

        return None

    @property
    def quantum(self): return self._quantum
    @quantum.setter
    def quantum(self, q): self._quantum = q
    @property
    def alg(self): return self._alg
    @alg.setter
    def alg(self, a): self._alg = a
