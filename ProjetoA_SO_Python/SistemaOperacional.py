import sys
import Clock
import FilaTarefas
import Parser
import Escalonador
import TCB
import View
from Enums import AlgoritmoEscalonamento

class SistemaOperacional:
    def __init__(self, nome_config):
        self._relogio = Clock.Clock()
        self._tarefasCarregadas = FilaTarefas.FilaTarefas()
        self._tarefasProntas = FilaTarefas.FilaTarefas()
        self._tarefasSuspensas = FilaTarefas.FilaTarefas()
        self._tarefaExecutando = None
        self._escalonador = Escalonador.Escalonador()
        self._parser = Parser.Parser()
        self._configuracoes = None
        self._tarefas = []
        self._historico = []
        self._todos_tcbs = []
        self._modo_debug = False

        self.comecar(nome_config)

    def comecar(self, nome_config):
        print("Iniciando Sistema Operacional...")

        #Opção do modo debug
        self.configurarModoDebug()

        if (self._modo_debug):
            print("=== Tick 0 ===")
        self.parseConfigs(nome_config)
        if self._configuracoes is None:
            print("Encerrando o sistema!")
            sys.exit(1)
        self.configsEscalonador()
        self.criarTasks()
        self.loopConstante()

    def parseConfigs(self, nome_config):
        if (self._modo_debug):
            print("Lendo configurações...")
        self._configuracoes, self._tarefas = self._parser.lerConfigs(nome_config)

    def criarTasks(self):
        if (self._modo_debug):
            print("Criando tasks...")
        for linha in self._tarefas:
            dados = linha.split(';')
            if len(dados) < 5:
                print(f"Linha inválida: {linha}")
                continue
            id = dados[0]
            cor = int(dados[1])
            ingresso = int(dados[2])
            duracao = int(dados[3])

            # Aqui é para caso não tenha prioridade nem eventos
            prioridade = int(dados[4]) if len(dados) > 4 and dados[4].isdigit() else 0
            eventos = dados[5:] if len(dados) > 5 else []

            novo = TCB.TCB(id, cor, ingresso, duracao, prioridade, eventos)
            self._tarefasCarregadas.addTask(novo)
            self._todos_tcbs.append(novo)
            if (self._modo_debug):
                print(f"TCB criado: {novo}")

    def configsEscalonador(self):        
        self._escalonador.alg = self._configuracoes[0]
        self._escalonador.quantum = self._configuracoes[1]
        if (self._modo_debug):
            print(f"Configurando escalonador...")
            print(f"Algoritmo: {self._escalonador.alg}, Quantum: {self._escalonador.quantum}")

    def atualizaCarregadas(self, tickAtual):
        mover = []
        for t in self._tarefasCarregadas.getAll():
            if t.ingresso == tickAtual:
                mover.append(t)
        for t in mover:
            t.estado = "pronta"
            self._tarefasProntas.addTask(t)
            self._tarefasCarregadas.removeTask(t)
            if (self._modo_debug):
                print(f"Tarefa {t.id} movida para PRONTA no tick {tickAtual}")

    def loopConstante(self, modo_debug=False):
        while (not self._tarefasCarregadas.isEmpty() or 
               not self._tarefasProntas.isEmpty() or 
               self._tarefaExecutando is not None):

            tick_atual = self._relogio.tickAtual
            self.atualizaCarregadas(tick_atual)
            if (self._modo_debug):
                if not self._tarefasProntas.isEmpty() :
                    print("TAREFAS PRONTAS:", [t.id for t in self._tarefasProntas.getAll()])

            self._tarefaExecutando = self._escalonador.escolherTarefa(self._tarefasProntas, self._tarefaExecutando)
 
            if self._tarefaExecutando:
                if (self._modo_debug):
                    print(f"TAREFA A EXECUTAR: {self._tarefaExecutando.id}")
                self.executarTarefa(self._tarefaExecutando, self._tarefasProntas)

            for tarefa in self._tarefasProntas:
                tarefa.incrementaTempoVida()
            for tarefa in self._tarefasSuspensas:
                tarefa.incrementaTempoVida()

            self.registrarTickNoHistorico()
            self.proximoTick()

            if (self._modo_debug):
                input("Pressione ENTER para avançar...")

        if (self._modo_debug):
            print("=== TODAS AS TAREFAS CONCLUÍDAS ===")
        View.gerar_grafico(self._historico, self._todos_tcbs)

    def executarTarefa(self, tarefa, listaProntas):
        tarefa.estado = "executando"
        tarefa.executarTick()
        if (self._modo_debug):
            print(f"{tarefa.id} executou (restante {tarefa.duracaoRestante})")
        if tarefa.estaConcluida():
            tarefa.concluirTarefa()

    def proximoTick(self):
        novoTick = self._relogio.proximoTick()
        if (self._modo_debug):
            print(f"\n=== Tick {novoTick} ===")

    def registrarTickNoHistorico(self):
        tick = self._relogio.tickAtual
        id_exec = self._tarefaExecutando.id if self._tarefaExecutando else "OCIOSA"
        cor_exec = self._tarefaExecutando.cor if self._tarefaExecutando else "#888888"

        registro = {
            'tick': tick,
            'executando_id': id_exec,
            'executando_cor': cor_exec,
            'tarefas': [
                {'id': t.id, 'estado': t.estado.value, 'restante': t.duracaoRestante}
                for t in self._todos_tcbs
            ]
        }
        self._historico.append(registro)
        if (self._modo_debug):
            print(f"[HISTÓRICO] Tick {tick}: CPU -> {id_exec}")

    def configurarModoDebug(self):
        try:
            entrada = input("Digite 0 para modo normal e 1 para modo debug: ").strip()
            
            if entrada == "1":
                self._modo_debug = True
                print("Modo debug ATIVADO")
            elif entrada == "0":
                self._modo_debug = False
                print("Modo normal ATIVADO")
            else:
                # Entrada inválida - usa padrão e mostra aviso
                self._modo_debug = False
                print("Opção inválida. Indo para o modo normal por padrão.")
                
        except Exception as e:
            self._modo_debug = False
            print("Erro na entrada. Indo para o modo normal por padrão.")
