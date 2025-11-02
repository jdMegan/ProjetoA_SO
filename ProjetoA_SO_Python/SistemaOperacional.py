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
        print("=== Sistema Operacional Iniciado ===")
        print("")

        #Opção do modo debug
        self.configurarModoDebug()
        if (self._modo_debug):
            print("--- Tick 0 ---")
        
        self.parseConfigs(nome_config)
        if self._configuracoes is None:
            print("ERRO: Configurações inválidas! Encerrando sistema.")
            input()
            sys.exit(1)
        self.configsEscalonador()
        self.criarTasks()
        self.loopConstante()
        input()
        sys.exit(1)

    def parseConfigs(self, nome_config):
        if (self._modo_debug):
            print("-> Lendo configurações...")
        self._configuracoes, self._tarefas = self._parser.lerConfigs(nome_config)

    def criarTasks(self):
        if (self._modo_debug):
            print("-> Criando tarefas: ")
        for linha in self._tarefas:
            dados = linha.split(';')
            if len(dados) < 5:
                print(f"  AVISO: Linha ignorada - {linha}")
                continue
            id = dados[0]
            cor = int(dados[1])
            ingresso = int(dados[2])
            duracao = int(dados[3])
            test = None

            # Aqui é para caso não tenha prioridade nem eventos
            prioridade = int(dados[4]) if len(dados) > 4 and dados[4].isdigit() else 0
            eventos = dados[5:] if len(dados) > 5 else []

            # Tarefa criada e salva, esperando a hora de ingresso
            novo = TCB.TCB(id, cor, ingresso, duracao, prioridade, eventos)
            self._tarefasCarregadas.addTask(novo)
            self._todos_tcbs.append(novo)
            if self._modo_debug:
                print(f"  [+] {id} | Ingresso: {ingresso} | Duração: {duracao} | Pri: {prioridade} | Cor: {cor} | Eventos: {eventos} | Estado: {novo.estado.value}")


    def configsEscalonador(self):        
        self._escalonador.alg = self._configuracoes[0]
        self._escalonador.quantum = self._configuracoes[1]
        if (self._modo_debug):
            print("-> Configurações do escalonador:")
            print(f"  Algoritmo: {self._escalonador.alg.value}")
            print(f"  Quantum: {self._escalonador.quantum}")
            print("")

    def atualizaCarregadas(self, tickAtual):
        # Lista temporaria para poder mudar a lista enquanto itera
        mover = []
        for t in self._tarefasCarregadas.getAll():
            if t.ingresso == tickAtual:
                mover.append(t)
        for t in mover:
            t.estado = "pronta"
            self._tarefasProntas.addTask(t)
            self._tarefasCarregadas.removeTask(t)
            if (self._modo_debug):
                print(f"  Tarefa {t.id} -> PRONTA (tick {tickAtual})")


    def loopConstante(self, modo_debug=False):
        # Enquanto ainda existirem tarefas
        while (not self._tarefasCarregadas.isEmpty() or 
               not self._tarefasProntas.isEmpty() or 
               self._tarefaExecutando is not None):

            # Atualiza tarefas para esse tick
            tick_atual = self._relogio.tickAtual
            self.atualizaCarregadas(tick_atual)
            if self._modo_debug:
                if not self._tarefasProntas.isEmpty():
                    tarefas_prontas_ids = [t.id for t in self._tarefasProntas.getAll()]
                    print(f"  Prontas: {tarefas_prontas_ids}")
                else:
                    print("  Prontas: [vazia]")

            # Chama o escalonador
            self._tarefaExecutando = self._escalonador.escolherTarefa(self._tarefasProntas, self._tarefaExecutando)
 
            if self._tarefaExecutando:
                if self._modo_debug:
                    print(f"  Executando: {self._tarefaExecutando.id}")
                self.executarTarefa(self._tarefaExecutando, self._tarefasProntas)
            else:
                if self._modo_debug:
                    print("  Executando: [None]")

            # Envelhece as outras tarefas
            for tarefa in self._tarefasProntas:
                tarefa.incrementaTempoVida()
            for tarefa in self._tarefasSuspensas:
                tarefa.incrementaTempoVida()

            self.registrarTickNoHistorico()
            
            if (self._modo_debug):
                input("  [ENTER para continuar] ")
            self.proximoTick()

        if (self._modo_debug):
            print("")
            print("=== Execução concluída ===")
            print("")
        tt, tw = self.calcularMetricas()
        View.gerar_grafico(self._historico, self._todos_tcbs, self._escalonador._alg, tt, tw)

    def executarTarefa(self, tarefa, listaProntas):
        tarefa.estado = "executando"
        tarefa.executarTick()
        if self._modo_debug:
            if tarefa.estaConcluida():
                print(f"    >> Tarefa {tarefa.id} CONCLUÍDA")
            else:
                print(f"    >> Tarefa {tarefa.id} executou | Restante: {tarefa.duracaoRestante}")
        if tarefa.estaConcluida():
            tarefa.concluirTarefa(self._relogio.tickAtual)

    def proximoTick(self):
        novoTick = self._relogio.proximoTick()
        if (self._modo_debug):
            print("")
            print(f"--- Tick {novoTick} ---")

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
        if self._modo_debug:
            print("-> Atualizando historico:")

            # Separa as tarefas que não foram concluidas
            tarefas_ativas = []
            for t in self._todos_tcbs:
                if t.estado.value != "concluida":
                    estado = t.estado.value
                    tarefas_ativas.append(f"{t.id}({estado},{t.duracaoRestante})")
            
            #Concatena a lista em string e printa
            if tarefas_ativas:
                print(f"  Estado atual das tarefas e tempo restante:")
                print(f"    >> {', '.join(tarefas_ativas)}")
        

    def configurarModoDebug(self):
        try:
            print("Configuração:")
            entrada = input("  Modo debug? (0=Não, 1=Sim): ").strip()
            
            if entrada == "1":
                self._modo_debug = True
                print("  Modo debug: ATIVADO")
            elif entrada == "0":
                self._modo_debug = False
                print("  Modo debug: DESATIVADO")
            else:
                self._modo_debug = False
                print("  AVISO: Opção inválida. Modo debug: DESATIVADO.")
                
        except Exception as e:
            self._modo_debug = False
            print("  AVISO: Erro na entrada. Modo debug: DESATIVADO.")
        print("")

    def calcularMetricas(self):
        # Calcula tempo medio de vida (tt) e tempo medio de espera (tw)  
        tarefas_concluidas = [t for t in self._todos_tcbs if t.estaConcluida()]
        if not tarefas_concluidas:
            print("Erro ao calcular métricas : Nenhuma tarefa concluída.")
            return 0, 0
        
        soma_tt = 0
        soma_tw = 0
        
        # Calcula tt e tw
        for t in tarefas_concluidas:
            tt_t0x= t.tempo_conclusao - t.ingresso
            soma_tt += tt_t0x

            tw_t0x = tt_t0x - t.duracao
            soma_tw += tw_t0x     

        # Calcula as medias
        num_tarefas = len(tarefas_concluidas)
        tt = soma_tt / num_tarefas
        tw = soma_tw / num_tarefas
        
        print("=== Métricas ===")
        print(f"Turnaround Time: {tt:.2f}")
        print(f"Waiting Time: {tw:.2f}")
        return tt, tw
