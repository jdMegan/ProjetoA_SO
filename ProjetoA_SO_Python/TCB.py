# Task Control Block
from Enums import EstadoTarefa, CorTarefa

class TCB:
    def __init__(self, id, cor, ingresso, duracao, eventos):
        self._id = id
        # Chega como int, vira ENUM
        self._cor = CorTarefa(cor)  
        self._ingresso = ingresso
        self._duracao = duracao
        # Quanto falta para terminar
        self._duracaoRestante = duracao
        self._prioridade = 0 
        self._eventos = eventos or []
        # Quando é criada tem sempre o estado carregada, é um ENUM
        self._estado = EstadoTarefa.CARREGADA
        # Quanto tempo desde que a tarefa entrou na fila de prontas pela primeira vez
        # Quando tempo seguido ela esteve executando, para controle do quantum
        self._tempoVida = 0
        self._tempoExecutando = 0

    def __repr__(self):
        return (
            f"TCB("
            f"id = {self._id}, "
            f"cor = {self._cor}, "
            f"ingresso = {self._ingresso}, "
            f"duracao = {self._duracao}, "
            f"duracaoRestante = {self._duracaoRestante}, "
            f"prioridade = {self._prioridade}, "
            f"estado = {self._estado}, "
            f"tempoVida = {self._tempoVida}), "
            f"tempoExecutando = {self._tempoExecutando}) "
        )
        
    # Getters e setters
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, valor):
        if not valor:
            raise ValueError("Sem id :^( )")
        self._id = valor
    
    @property
    def cor(self):
        #Retorna a cor, em hexcode, se estiver executando
        #Caso contrario retorna uma versao dessaturada
        if self._estado == EstadoTarefa.EXECUTANDO:
            return self._cor.paraHex()
        else:
            return self._dessaturarCor(self._cor.paraHex())
    
    @cor.setter
    def cor(self, valor):
        if not valor:
            raise ValueError("Sem cor :^( )")
        #Checa se a cor passada esta em ENUM ou em int, converte se necessario
        if isinstance(valor, CorTarefa):
            self._cor = valor
        else:
            self._cor = CorTarefa(valor)
    
    @property
    def ingresso(self):
        return self._ingresso
    
    @ingresso.setter
    def ingresso(self, valor):
        if valor is None:
            raise ValueError("Sem ingresso :^( )")
        self._ingresso = valor

    @property
    def duracao(self):
        return self._duracao
    
    @duracao.setter
    def duracao(self, valor):
        if valor is None:
            raise ValueError("Sem duracao :^( )")
        if valor <= 0:
            raise ValueError("Duração invalida :^( )")
        self._duracao = valor 

    @property
    def duracaoRestante(self):
        return self._duracaoRestante
    
    @duracaoRestante.setter
    def duracaoRestante(self, valor):
        if valor < 0:
            raise ValueError("Duração invalida :^( )")
        self._duracaoRestante = valor

    @property
    def prioridade(self):
        return self._prioridade
    
    @prioridade.setter
    def prioridade(self, valor):
        if valor is None:
            raise ValueError("Sem prioridade :^( )")
        self._prioridade = valor

    @property
    def estado(self):
        return self._estado
    
    @estado.setter
    def estado(self, valor):
        if not valor:
            raise ValueError("Sem estado :^( )")
        #Checa se é ENUM, converte se necessario
        if isinstance(valor, EstadoTarefa):
            self._estado = valor  
        else:
            self._estado = EstadoTarefa(valor)
        #print(self._estado)
        #print(type(self._estado))

    @property 
    def eventos(self):
        return self._eventos
    
    @eventos.setter
    def eventos(self, valor):
        self._eventos = valor

    @property
    def tempoExecutado(self):
        return self._tempoExecutado
    
    @tempoExecutado.setter
    def tempoExecutado(self, valor):
        if (valor < 0):                                  
            raise ValueError("Tempo inválido :^( )")  
        self._tempoExecutado = valor                   


    def _dessaturarCor(self, corHex):
       # Uma cor em hex tem o formato: "#FF8800"
       # Cada dois caracteres representa uma cor do rgb
       # Separa essas cores pra esmeecer elas
       # Esmeece
       # Transforma em hex
       # Retorna
        try:
            r = int(corHex[1:3], 16)
            g = int(corHex[3:5], 16)
            b = int(corHex[5:7], 16)
            
            # Fórmula de luminância para cinza
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            
            # Mistura 30% da cor original + 70% cinza
            r_des = int(r * 0.3 + gray * 0.7)
            g_des = int(g * 0.3 + gray * 0.7) 
            b_des = int(b * 0.3 + gray * 0.7)
            
            return f"#{r_des:02x}{g_des:02x}{b_des:02x}"
        except:
            return "#CCCCCC"  # Fallback para cinza

    def resetQuantum(self):
        #Reseta o contador de tempo no quantum
        self._tempoExecutado = 0

    def executarTick(self):
        # Incrementa tempo no quantum
        # Decrementa quanto ainda falta
        self._tempoExecutado += 1
        self._duracaoRestante -= 1

    def estaConcluida(self):
        #Verifica se esta concluida
        return self._duracaoRestante <= 0

    def concluirTarefa(self):
        #Marca a tarefa como concluida
        self._estado = EstadoTarefa.CONCLUIDA

    def verificaQuantum(self, quantum):
        #Verifica se a tarefa ja estourou o tempo
        return self._tempoExecutado >= quantum
