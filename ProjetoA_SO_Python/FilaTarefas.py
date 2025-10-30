class FilaTarefas:
    def __init__(self):
        self._tarefas = []

    def addTask(self, tcb):
        self._tarefas.append(tcb)

    def addFirstTask(self, tcb):
        self._tarefas.insert(0, tcb)

    def removeTask(self, tcb):
        if tcb in self._tarefas:
            self._tarefas.remove(tcb)

    def getNext(self):
        if not self.isEmpty():
            return self._tarefas.pop(0)
        return None

    def peekNext(self):
        if not self.isEmpty():
            return self._tarefas[0]
        return None

    def getAll(self):
        return list(self._tarefas)

    def isEmpty(self):
        return len(self._tarefas) == 0

    def __len__(self):
        return len(self._tarefas)

    def __iter__(self):
        return iter(self._tarefas)

    def __repr__(self):
        return f"FilaTarefas({self._tarefas})"
