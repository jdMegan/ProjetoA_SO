"""
 A classe Sistema Operacional simulara . . . o sistema operacional. Logo ela que coordenara as outras classes.
 Cabe ao sistema operacional receber a requisiçao de tarefa, que sera feita via um documento .txt com as informaçoes da tarefa, e entao chamar o Parser para extrair os dados.
 O sistema operacional entao ira, com esses dados, criar os TCBs coloca los na Fila e chamar o Escalonador.
 Alem disso o sistema operacional tambem tera um Clock para a passagem de tick, seja em loop ou em modo debbuger, e tera um Historico para salvar o estado das tarefaz em cada momento.
 """
import Clock
import FilaTarefas
import Parser
import Escalonador
import TCB
class SistemaOperacional:
    def __init__(self,nome_config):
        self._relogio = Clock.Clock()
        #As tarefas são divididas em objetos FilaTarefas dependendo do seu estado
        self._tarefasCarregadas = FilaTarefas.FilaTarefas()
        self._tarefasProntas = FilaTarefas.FilaTarefas()
        self._tarefasSuspensas = FilaTarefas.FilaTarefas()
        self._tarefaExecutando = None # Variavel vazia, a principio nada executando
        self._escalonador = Escalonador.Escalonador()
        self._parser = Parser.Parser()
        #Configuraçoes do escalonador e das tarefas, respectivamente
        self._configuracoes = None
        self._tarefas = []
        #Recebe o nome do arquivo com as configurações para começar
        self.comecar(nome_config)

    def comecar(self,nome_config):
        print("Iniciando Sistema Operacional...")
        print("=== Tick 0 ===")
        #Configuraçoes
        self.parseConfigs(nome_config)
        self.configsEscalonador()
        self.criarTasks()
        #Começa loop
        self.loopConstante();  

    def parseConfigs(self, nome_config):
        print("Lendo configurações...")
        # Configuraçoes: algoritmo_escalonamento; quantum. Pro escalonador
        # Tarefas: id; cor; ingresso; duracao; prioridade; lista_eventos. Pras TCB
        self._configuracoes, self._tarefas = self._parser.lerConfigs(nome_config)

    def criarTasks(self):
        print("Criando tasks...")
        #_tarefas é um list
        #Cada elemento é um string com dados de uma unica task separados por ;
        #Aqui separa esses dados e usa para criar task
        for tarefa in self._tarefas:
            dados = tarefa.split(';')
            print(dados)

             # Acho q aqui tem um problema, não podemos assumir que os eventos sempre iniciam no indice 4
                # Pq teoricamente nesse lugar eh pra vir as prioridades e nao os eventos, 
                # mesmo q nesse arquivo ele n tenho adicionado as prioridades nelhor botar alguma logica pra pegar isso,
                # vai q na apresentacao ele usa um arq com prioridades, dai quebra o trab kkk
            prioridade1 = 0
            eventos = None
            if len(dados) > 4:
                # Quer dizer q existe valor de prioridade ou algum evento
                # Se for um numero eh prio, se nao eh um evento
                if dados[4].isdigit():
                    prioridade1 = dados[4]
                    # Do indice 5 em diante eh evento
                    eventos= dados[5:]
                else:
                    eventos1 = dados[4:]

            novoTCB = TCB.TCB(
                id=dados[0],
                cor=int(dados[1]),  # O TCB converte pra Enum
                ingresso=int(dados[2]),
                duracao=int(dados[3]),
                # eventos=dados[4:]
                prioridade = prioridade1,
                eventos = eventos1
            )
            print(novoTCB)
            self._tarefasCarregadas.addTask(novoTCB)

    def configsEscalonador(self):
        print("Configurando escalonador...")
        self._escalonador.alg = self._configuracoes[0] #ENUM
        self._escalonador.quantum = self._configuracoes[1] #int

    def atualizaHistorico():
        # Atualiza o historico a cada tick
        pass

    def proximoTick(self):
        #Avança o tempo
        novoTick = self._relogio.proximoTick()
        print(f"=== Tick {novoTick} ===")

    def atualizaCarregadas(self, tickAtual):
        #Cria uma lista temporaria para poder remover durante a iteração
        # Reformulei pq estava meio confuso de ler
        # mover = [t for t in self._tarefasCarregadas.getAll() if t.ingresso == tickAtual]
        mover = []
        lista_carregadas = self._tarefasCarregadas.getAll()

        for t in lista_carregadas:
            if t.ingresso == tickAtual:
                mover.append(t)

        #As que ingresso no tickAtual vao para a fila de prontas
        for t in mover:
            t.estado = "pronta"
            self._tarefasProntas.addTask(t)
            self._tarefasCarregadas.removeTask(t)       
   
    def loopConstante(self):
        # No momento o loop para qndo todas as tarefas estiverem na fila de prontas
        # No futuro vai parar quando nao tiver mais nenhuma pronta e executando
        # while not (self._tarefasCarregadas.isEmpty() 
        #   and self._tarefasProntas.isEmpty() 
        #   and self._tarefaExecutando.isEmpty()):
        while not self._tarefasCarregadas.isEmpty() :
            #Ve se alguma tarefa entra agora
            self.atualizaCarregadas(self._relogio.tickAtual)
            
            # Escalonador decide próxima tarefa
            print("TAREFAS PRONTAS NESSE TICK = ", self._tarefasProntas.getAll())
            taferaExecutar = self._escalonador.escolherTarefa(self._tarefasProntas)  
            print("TAREFA A EXECUTAR = ", taferaExecutar) 
            self._tarefaExecutando = taferaExecutar

            # Aumenta o tempo de vida de todas as tarefas prontas, suspensas, executando
            for tarefa in self._tarefasProntas:
                tarefa._tempoVida += 1
            for tarefa in self._tarefasSuspensas:
                tarefa._tempoVida += 1
            if(self._tarefaExecutando is not None):
                self._tarefaExecutando._tempoVida += 1

            
            # Executa a tarefa atual
            self.executarTarefa(taferaExecutar)

            # Atualiza hitorico
            ####self._historico.atualizarHistorico()
            #???

            # Como manter a mesma tarefa quando o tick acaba, mas o quantum dela não acabou?? tem q ver

            #Passa o tempo
            self.proximoTick()

    #Isso ta errado
    #Não faz mto sentido tarefaExecutando estar em uma lista ja q é só uma tarefa executando por vez
    #Mas n sei. . . tranformar ela em um atributo entao?
    # Boa ideia!! Alterei para uma variavel/atrib simples

    def executarTarefa(self, tafera):
        # Nos priemiros ticks a tarefa vem vazia dai da erro
        if(tafera is not None):
            print("siutação da tarefa antes de exec  \n", "tafera._tempoExecutando=", tafera._tempoExecutando, "\n", "tafera.duracaoRestante=", tafera.duracaoRestante, "\n", "tafera._tempoVida=",tafera._tempoVida)
            tafera._tempoExecutando += 1
            tafera.duracaoRestante -= 1
            if (tafera.duracaoRestante == 0):
                tafera.estado = "concluida"
                # Quando é concluida é "removida" da memoria
                tafera = None
            print("siutação da tarefa DPS de exec  \n", "tafera._tempoExecutando=", tafera._tempoExecutando, "\n", "tafera.duracaoRestante=", tafera.duracaoRestante, "\n", "tafera._tempoVida=",tafera._tempoVida )


    #     self._tarefaExecutando.tempoExecutando += 1
    #     self._tarefaExecutando.duracaoRestante -= 1
    #     # Se concluir
    #     if (self._tarefaExecutando.duracaoRestante == 0):
    #        self._tarefaExecutando.estado = "concluida"
    #         # Quando é concluida é "removida" da memoria
    #        self._tarefaExecutando = None
