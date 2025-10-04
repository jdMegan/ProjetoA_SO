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
    def __init__(self,nome_config):

        self._relogio = Clock.Clock()
        self._tarefasCarregadas = FilaTarefas.FilaTarefas()
        self._tarefasProntas = FilaTarefas.FilaTarefas()
        self._tarefasSuspensas = FilaTarefas.FilaTarefas()
        self._tarefaExecutando = FilaTarefas.FilaTarefas()
        self._escalonador = Escalonador.Escalonador()
        self._parser = Parser.Parser()
        self._configuracoes = None
        self._tarefas = []

        self.comecar(nome_config)

    def comecar(self,nome_config):
        print("Iniciando Sistema Operacional...")

        self.parseConfigs(nome_config)
        self.configsEscalonador()
        self.criarTasks()
        self.proximoTick()

        #loopConstante();  

    def parseConfigs(self, nome_config):
        print("Lendo configurações...")
        # configuraçoes: algoritmo_escalonamento; quantum. Pro escalonador
        # tarefas: id; cor; ingresso; duracao; prioridade; lista_eventos. Pras TCB
        self._configuracoes, self._tarefas = self._parser.lerConfigs(nome_config)
    

    def criarTasks(self):
        print("Criando tasks...")
        for tarefa in self._tarefas:
            dados = tarefa.split(';')
            print(dados)
            novoTCB = TCB.TCB(
                id=dados[0],
                cor=dados[1],
                ingresso=int(dados[2]),
                duracao=int(dados[3]),
                eventos=dados[4:]
            )
            print(novoTCB)
            self._tarefasCarregadas.addTask(novoTCB)
        

    def configsEscalonador(self):
        print("Configurando escalonador...")
        self._escalonador.alg  = self._configuracoes[0]
        self._escalonador.quantum  = int(self._configuracoes[1])


    def atualizaHistorico():
        # atualiza o historico a cada tick
        pass

    def proximoTick(self):
        """Avança o tempo no sistema"""
        novo_tick = self._relogio.proximoTick()
        print(f"=== Tick {novo_tick} ===")
        
        # Aqui você vai chamar:
        #self._atualizarEstadoTarefas()  # Tarefas que chegam neste tick
        #self._escalonador.Escalonar()   # Escalonador decide próxima tarefa
        #self._executar_tarefa()         # Executa a tarefa atual
        #self._historico.atualizarHistorico()       # Registra estado atual
        
        #return novo_tick
        
