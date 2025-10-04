class Clock():
    def __init__(self):
        self._tick = 1
        self._tickAtual = 0

    def proximoTick(self):
        """Avança o tempo e retorna o novo tickAtual"""
        self._tickAtual += self._tick
        return self._tickAtual
    
    @property
    def tickAtual(self):
        return self._tickAtual
    
    @property
    def tick(self):
        return self._tick
    @tick.setter
    def tick(self, valor):
        if valor <= 0:
            raise ValueError("Tick deve ser positivo")
        self._tick = valor
