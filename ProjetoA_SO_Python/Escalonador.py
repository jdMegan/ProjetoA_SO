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
            if not listaProntas.isEmpty():
                todas = listaProntas.getAll()
                if tarefaExecutando:
                    todas.append(tarefaExecutando)
                return min(todas, key=lambda t: t.duracaoRestante)
            return tarefaExecutando

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
                    listaProntas.addTask(tarefaExecutando) # Volta para o final
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
