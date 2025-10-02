 # Task Control Block
class TCB ():
    def __init__(self, id, cor, ingresso, duracao, eventos):
        self._id = id
        self._cor = cor
        self._ingresso = ingresso
        self._duracao = duracao
        self._prioridade = 0 
        self._eventos = []#eventos #Isso aqui nem mexe, é para o trab B só, mas já precisa estar definido
        self._estado = 'pronta'


    def __repr__(self):
        return f"TCB(id={self._id}, cor={self._cor}, ingresso={self._ingresso}, duracao={self._duracao}, prioridade={self.prioridade}, estado={self._estado} )"

    # Acho que deveriamos fazer isso dentro do parser mesmo, pq 
    # tipo, o parser já manda os dados prontos só pra iniciar o TCB
    def setConfigs(configs):
        pass 
        # //Vai receber um array, nao o array inteiro q tem no SistemaOperacional
        # //Provavelmente usa um stream la pra passar pra ca s as relevantes
        # //Dai vai salvando nas variaveis certas
    
    # Getters e setters
    @property
    def id(self):
        return self._id
    
    @property
    def cor(self):
        return self._cor
    
    @property
    def ingresso(self):
        return self._ingresso
    
    @property
    def duracao(self):
        return self._duracao
    
    @property
    def prioridade(self):
        return self._prioridade
      
    @property
    def estado(self):
        return self._estado
    
    @property 
    def eventos(self):
        return self._eventos