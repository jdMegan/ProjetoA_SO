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
class SistemaOperacional():
    def __init__(self):

        self._relogio = Clock.Clock()
        self._tarefasProntas = FilaTarefas.FilaTarefas()
        self._tarefasSuspensas = FilaTarefas.FilaTarefas()
        self._tarefaExecutando = FilaTarefas.FilaTarefas()
        self._escalonador = Escalonador.Escalonador()
        self._parser = Parser.Parser()
        self._configuracoes = None # Referente as configs de algoritmo e quantum
        #Ao inves de 1 variavel _configuracoes achei melhor uma variavel para as configs e outra p as tarfeas
        self._tarefas = [] # Lista que armazena as tarefas do arquivo txt

        # Criar uma classe Historico, dai o SO tem um historico e a cada tick ele manda oq tem em cada FilaTarefas pro historico pra dps o Historico poder criar o grafico  
        #self._Historico = Historico()

    # Metodo que simula a passagem de tick's
    # Presume-se que sempre tera uma tarefa sendo executada ate todas serem executadas. Entao esse sera o parametro para o loop
    # def loopConstante(self):
    #     while not self._tarefaExecutando.isEmpty():
    #         self._relogio.nextTick()
    
    # Metodo que simula a passagem de tick's no modo debugger
    # Provavelmente o ideal seria de algum modo que ele ler a entrada do teclado para ir pro proximo tick
    # Mas so ir chamando ela no terminal n tem problema por hora
    # def loopDebbuger(self):
    #     self._relogio.nextTick();    
        
    # Metodo que comeca tudo
    # Começa o relogio e o loop. 
    # O loop acaba se no tiver tarefa executando, entao ele tem q ser a ultima coisa a ser chamada
    # Chama o parseConfigs para ler as configuraçes
    # !!!!Criar alguma funçao q le as configuraçoes e separa elas em arrays pra cada uma das coisas sabe, uma por objeto uma pro escalonado
    # !!!!Ou a gente pode so usar stream sla
    # !!!!Tem que ver isso
    # Passa as configuraçes para o escalonador
    # Cria as tasks
    # Poe as tasks na fila

    def comecar(self, nome_config):
        self.parseConfigs(nome_config)
        self.configsEscalonador()
        self.criarTasks()
#         loopConstante();  

    def parseConfigs(self, nome_config):
        # as configuraçoes serao na ordem algoritmo_escalonamento;quantum 
        # enquanto as tarefas serão uma lista com id;cor;ingresso;duracao;prioridade;lista_eventos de cada uma
        self._configuracoes, self._tarefas = self._parser.lerConfigs(nome_config)
        # algoritmo_escalonamento e quantum vai pro escalonador
        # sao criadas TCB's com  id;cor;ingresso;duracao;prioridade;lista_eventos e cada TCB criada vai pra lista de prontas

    def criarTasks(self):
        # vai criando TCB's e mandando pro listaProntas
        # Para cada tarefa da lista de tarefas
        for tarefa in self._tarefas:
            print(tarefa.split(';'))
            print('foi')
            # novoTCB = TCB.TCB(tarefa.split(';'))
        # Talvez fazer uma funçao so pra mandar pro lista prontas
        # nem precisa achoo
            # self.__tarefasProntas.append(novoTCB) #joga pro final da fila

    def configsEscalonador(self):
        pass
        # Manda pro escalonador o quantum e o tipo de algoritimo

    def atualizaHistorico():
        pass
        # atualiza o historico a cada tick


