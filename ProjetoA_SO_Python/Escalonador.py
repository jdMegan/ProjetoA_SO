class Escalonador():
    def __init__(self):
        self._quantum = None
        self._alg = None

#Os tipos de algoritimo poderiam ser um ENUM, implementar isso no futuro

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
