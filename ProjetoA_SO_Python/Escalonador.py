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
            # Maior prioridade numérica executa primeiro
            if not listaProntas.isEmpty():
                todas = listaProntas.getAll()
                if tarefaExecutando:
                    todas.append(tarefaExecutando)
                return max(todas, key=lambda t: t.prioridade)
            return tarefaExecutando

        return None

    @property
    def quantum(self): return self._quantum
    @quantum.setter
    def quantum(self, q): self._quantum = q
    @property
    def alg(self): return self._alg
    @alg.setter
    def alg(self, a): self._alg = a
