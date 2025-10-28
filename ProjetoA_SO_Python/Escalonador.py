from Enums import AlgoritmoEscalonamento

class Escalonador:
    def __init__(self):
        self._quantum = None
        self._alg = None

    def escolherTarefa(self, listaProntas, tarefaExecutando):
        # DEBUG: Mostra informações da tarefa atual
        if tarefaExecutando:
            print(f"DEBUG: Tarefa atual: {tarefaExecutando.id}, "
                  f"Ingresso: {tarefaExecutando.ingresso}, "
                  f"Duraçã0: {tarefaExecutando.duracao}, "
                  f"TempoExec: {tarefaExecutando.tempoExecutando}, "
                  f"Duraçã0: {tarefaExecutando.duracaoRestante}, "
                  f"TempoVIda: {tarefaExecutando.tempoVida}, "     
                  f"PassouQuantum: {tarefaExecutando.passouQuantum(self._quantum)}")
        
        if self._alg == AlgoritmoEscalonamento.FCFS or self._alg == AlgoritmoEscalonamento.FSCS:
            # Primeiro checa se ja tem alguma tarefa selecionada e se ela ainda tem quantum
            if tarefaExecutando is None: 
                print("DEBUG: Nenhuma tarefa executando, pegando próxima da fila")
                tarefa_escolhida = listaProntas.getNext()
            elif tarefaExecutando.passouQuantum(self._quantum): 
                print(f"DEBUG: Tarefa {tarefaExecutando.id} passou do quantum! "
                      f"({tarefaExecutando.tempoExecutando} >= {self._quantum})")
                tarefaExecutando.resetQuantum()
                listaProntas.addTask(tarefaExecutando)
                tarefa_escolhida = listaProntas.getNext()
            else:
                print(f"DEBUG: Continuando com tarefa {tarefaExecutando.id}")
                tarefa_escolhida = tarefaExecutando 
            
            return tarefa_escolhida
        
        elif self._alg == AlgoritmoEscalonamento.PRIORIDADE_P:
            # Implementação futura
            pass
        
        elif self._alg == AlgoritmoEscalonamento.SRTF:
            # Implementação futura  
            pass
        
        return None

    def reajustaTarefa(self, tarefa, listaProntas):
        # Método mantido para compatibilidade
        pass

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
