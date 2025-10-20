# FilaTarefas.py

class FilaTarefas:
    def __init__(self):
        # Internamente só uma lista normal
        self._tarefas = []

    def addTask(self, tcb):
        #Adiciona uma tarefa ao final da fila
        self._tarefas.append(tcb)

    def addFirstTask(self, tcb):
        #Adiciona uma tarefa no inicio da fila
        self._tarefas.insert(0, tcb)

    def removeTask(self, tcb):
        #Remove uma tarefa específica da fila
        if tcb in self._tarefas:
            self._tarefas.remove(tcb)

    def getNext(self):
        #Retorna e remove a próxima tarefa da fila (FIFO por padrão)
        if not self.isEmpty():
            return self._tarefas.pop(0)
        return None

    def peekNext(self):
        #Retorna a próxima tarefa sem remover
        if not self.isEmpty():
            return self._tarefas[0]
        return None

    def getAll(self):
        #Retorna a lista de tarefas (cópia)
        return list(self._tarefas)

    def isEmpty(self):
        #Retorna True se a fila está vazia  
        return len(self._tarefas) == 0

    def __len__(self):
        #Permite usar len(fila)
        return len(self._tarefas)

    def __repr__(self):
        return f"FilaTarefas({self._tarefas})"
    
    def __iter__(self):
        return iter(self._tarefas)
