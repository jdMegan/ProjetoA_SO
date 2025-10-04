 # Task Control Block
class TCB ():
    def __init__(self, id, cor, ingresso, duracao, eventos):
        self._id = id
        self._cor = cor
        self._ingresso = ingresso
        self._duracao = duracao
        self._prioridade = 0 
        if not eventos:
            self._eventos = []
        else:
            self._eventos = eventos
        
        #Ja que as tarefas sao criada em lote, antes mesmo de chegar a hora de começo delas
        #Acho q seria melhor ter um estado generico de carregada
        #Pra dai elas virarem pronta só quando chega na hora de começo
        #Vou criar um atributo FilaTarefas no SO só para as tarefas carregadas
        #Assim quma tarefa é criada ela vai pra la

        #Os estados e cores poderiam ser um ENUM
        self._estado = 'carregada'


    def __repr__(self):
        return f"TCB(id={self._id}, cor={self._cor}, ingresso={self._ingresso}, duracao={self._duracao}, prioridade={self.prioridade}, estado={self._estado} )"

    # Getters e setters
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self,id):
        if not id:
            raise ValueError("Sem id :^( )")
        self._id = id

    @property
    def cor(self):
        return self._cor
    @cor.setter
    def cor(self, cor):
        if not cor:
            raise ValueError("Sem cor :^( )")
        self._cor = cor
    
    @property
    def ingresso(self):
        return self._ingresso
    @ingresso.setter
    def ingresso(self, ingresso):
        if not ingresso:
            raise ValueError("Sem ingresso :^( )")
        self._ingresso = ingresso


    @property
    def duracao(self):
        return self._duracao
    @duracao.setter
    def duracao(self, duracao):
        if not duracao:
            raise ValueError("Sem duracao :^( )")
        self._duracao = duracao

    @property
    def prioridade(self):
        return self._prioridade
    @prioridade.setter
    def prioridade(self, prioridade):
        if not prioridade:
            raise ValueError("Sem prioridade :^( )")
        self._prioridade = prioridade

    @property
    def estado(self):
        return self._estado
    @estado.setter
    def estado(self, estado):
        if not estado:
            raise ValueError("Sem estado :^( )")
        self._estado = estado
    
    
    @property 
    def eventos(self):
        if eventos:
            return self._eventos #Pq se n tiver eventos, sla se isso realmente é necessario
    @eventos.setter
    def eventos(self, eventos):
        self._eventos = eventos
