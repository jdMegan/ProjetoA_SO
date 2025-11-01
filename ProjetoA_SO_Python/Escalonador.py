from Enums import AlgoritmoEscalonamento

class Escalonador:
    def __init__(self):
        self._quantum = None
        self._alg = None

    def escolherTarefa(self, listaProntas, tarefaExecutando):
        if self._alg == AlgoritmoEscalonamento.FCFS:
            if( tarefaExecutando is None or tarefaExecutando.estaConcluida()):
                return listaProntas.getNext()
            return tarefaExecutando

        elif self._alg == AlgoritmoEscalonamento.FSCS or self._alg == AlgoritmoEscalonamento.ROUND_ROBIN:
            # Round Robin (FSCS)
            if (tarefaExecutando is None or tarefaExecutando.estaConcluida()):
                return listaProntas.getNext()
            elif tarefaExecutando.passouQuantum(self._quantum):
                tarefaExecutando.resetQuantum()
                listaProntas.addTask(tarefaExecutando)
                return listaProntas.getNext()
            else:
                return tarefaExecutando

        elif self._alg == AlgoritmoEscalonamento.SRTF:
            # Shortest Remaining Time First (preemptivo)
            if tarefaExecutando and tarefaExecutando.estaConcluida():
                tarefaExecutando = None            
            todas = listaProntas.getAll()
            tarefa_anterior = tarefaExecutando
            if tarefa_anterior:
                todas.append(tarefa_anterior)
            if not todas:
                return None 
            tarefa_menor_dur = min(todas, key=lambda t: (t.duracaoRestante, t.ingresso)) # quando tem empate na duracao restante olha para quem entrou primeiro
            # Se a tarefa escolhida é a mesma que já estava na CPU, não faz nada.
            if tarefa_menor_dur == tarefa_anterior:
                return tarefa_anterior           
            # Se a melhor tarefa é dif da que esta executando eh pq teve preempcao            
            if tarefa_anterior is not None:
                if not tarefa_anterior.estaConcluida():
                    tarefa_anterior.estado = "pronta"
                    listaProntas.addTask(tarefa_anterior) # Volta para a fila de pronta
            # A nova tarefa n pode ficar na fila e na CPU
            if listaProntas.contem(tarefa_menor_dur):
                listaProntas.removeTask(tarefa_menor_dur)
            return tarefa_menor_dur

        elif self._alg == AlgoritmoEscalonamento.PRIORIDADE_P:
            if tarefaExecutando and tarefaExecutando.estaConcluida():
                tarefaExecutando = None
            # Maior prioridade numérica executa primeiro
            todas = listaProntas.getAll()
            if tarefaExecutando:
                todas.append(tarefaExecutando)
            if not todas:
                return None 
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
