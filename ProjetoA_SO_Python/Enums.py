from enum import Enum

class EstadoTarefa(Enum):
    CARREGADA = "carregada"
    PRONTA = "pronta"
    EXECUTANDO = "executando"
    SUSPENSA = "suspensa"
    CONCLUIDA = "concluida"
    
    def __str__(self):
        return self.value

class AlgoritmoEscalonamento(Enum):
    FCFS = "FCFS"
    SJF = "SJF"
    SRTF = "SRTF" 
    PRIORIDADE_P = "PRIOP"
    ROUND_ROBIN = "RR"
    
    def __str__(self):
        return self.value

class CorTarefa(Enum):
    VERMELHO = 0
    VERDE = 1
    AZUL = 2
    AMARELO = 3
    ROXO = 4
    LARANJA = 5
    ROSA = 6
    CIANO = 7
    
    def paraHex(self):
        cores_hex = {
            0: "#FF0000", 1: "#00FF00", 2: "#0000FF", 3: "#FFFF00",
            4: "#800080", 5: "#FFA500", 6: "#FFC0CB", 7: "#00FFFF",
        }
        return cores_hex.get(self.value, "#888888")
    
    def __str__(self):
        return str(self.value)
