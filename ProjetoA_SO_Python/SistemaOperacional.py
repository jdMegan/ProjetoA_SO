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
import View

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
        self._historico = [] # O historico vai consistir em uma lista de "registro" do estado de cada tick
        #Configuraçoes do escalonador e das tarefas, respectivamente
        self._configuracoes = None
        self._tarefas = []
        self._todos_tcbs = []
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
        for tarefa in self._tarefas:
            dados = tarefa.split(';')
            print(f"Dados da tarefa: {dados}")

            # Lógica para prioridade e eventos
            prioridade = 0
            eventos = []
            
            if len(dados) > 4:
                # Se o quarto elemento é um dígito, é prioridade
                if dados[4].isdigit():
                    prioridade = int(dados[4])
                    # Do índice 5 em diante são eventos
                    eventos = dados[5:] if len(dados) > 5 else []
                else:
                    # Do índice 4 em diante são eventos
                    eventos = dados[4:]

            # CORREÇÃO: Use a classe TCB diretamente do módulo
            novoTCB = TCB.TCB(
                id=dados[0],
                cor=int(dados[1]),
                ingresso=int(dados[2]),
                duracao=int(dados[3]),
                prioridade=prioridade,
                eventos=eventos
            )
            print(f"TCB criado: {novoTCB}")
            self._tarefasCarregadas.addTask(novoTCB)
            self._todos_tcbs.append(novoTCB)

    def configsEscalonador(self):
        #print("Configurando escalonador...")
        #self._escalonador.alg = self._configuracoes[0] #ENUM
        #self._escalonador.quantum = self._configuracoes[1] #int
        #self._escalonador._quantum_atual = self._configuracoes[1]
        
        print("Configurando escalonador...")
        self._escalonador.alg = self._configuracoes[0]  # ENUM
        self._escalonador.quantum = self._configuracoes[1]  # int
        print(f"Algoritmo: {self._escalonador.alg}, Quantum: {self._escalonador.quantum}")


    def atualizaHistorico():
        # Atualiza o historico a cada tick
        pass

    def proximoTick(self):
        #Avança o tempo
        novoTick = self._relogio.proximoTick()
        print(f"\n=== Tick {novoTick} ===")

    def atualizaCarregadas(self, tickAtual):
      # Cria uma lista temporaria para poder remover durante a iteração
        mover = []
        lista_carregadas = self._tarefasCarregadas.getAll()

        for t in lista_carregadas:
            if t.ingresso == tickAtual:
                mover.append(t)

       # As que ingresso no tickAtual vao para a fila de prontas
        for t in mover:
            t.estado = "pronta"
            self._tarefasProntas.addTask(t)
            self._tarefasCarregadas.removeTask(t)
            print(f"Tarefa {t.id} movida para PRONTA no tick {tickAtual}")

    def loopConstante(self):
        # Para quando não há mais tarefas para executar
        while (not self._tarefasCarregadas.isEmpty() or 
            not self._tarefasProntas.isEmpty() or 
            self._tarefaExecutando is not None):
            
            # Ve se alguma tarefa entra agora
            self.atualizaCarregadas(self._relogio.tickAtual)
            
            # VERIFICA SE TAREFA ATUAL TERMINOU (ANTES do escalonador)
            if self._tarefaExecutando and self._tarefaExecutando.estaConcluida():
                print(f"=== TAREFA {self._tarefaExecutando.id} CONCLUÍDA ===")
                self._tarefaExecutando.estado = "concluida"
                self._tarefaExecutando = None
            
            # Escalonador decide próxima tarefa, se houver alguma pronta
            if not self._tarefasProntas.isEmpty() or self._tarefaExecutando is not None:
                print("TAREFAS PRONTAS: ", [t.id for t in self._tarefasProntas.getAll()])
                
                tarefaExecutar = self._escalonador.escolherTarefa(
                    self._tarefasProntas, 
                    self._tarefaExecutando
                )
                
                # CORREÇÃO: Só faz o swap se for uma tarefa diferente E a atual não estiver concluída
                if (tarefaExecutar and 
                    tarefaExecutar != self._tarefaExecutando and 
                    self._tarefaExecutando and 
                    not self._tarefaExecutando.estaConcluida()):
                    
                    print(f"Tarefa {self._tarefaExecutando.id} volta para fila de prontas")
                    self._tarefaExecutando.estado = "pronta"
                    self._tarefaExecutando.resetQuantum()
                    # CORREÇÃO: Remove antes de adicionar para evitar duplicação
                    self._tarefasProntas.removeTask(self._tarefaExecutando)
                    self._tarefasProntas.addTask(self._tarefaExecutando)
                
                self._tarefaExecutando = tarefaExecutar
                
                if self._tarefaExecutando:
                    print(f"TAREFA A EXECUTAR: {self._tarefaExecutando.id}")
                    print(f"QUANTUM ATUAL: {self._tarefaExecutando.tempoExecutando}/{self._escalonador.quantum}")
                    
                    self.executarTarefa(self._tarefaExecutando, self._tarefasProntas)
            
            # Aumenta o tempo de vida de todas as tarefas prontas
            for tarefa in self._tarefasProntas:
                tarefa.incrementaTempoVida()
            for tarefa in self._tarefasSuspensas:
                tarefa.incrementaTempoVida()

            # Registra o estado do tick no historico para montar o grafico dps
            self.registrarTickNoHistorico()

            #Passa o tempo
            self.proximoTick()
        
        # Acaba e gera o grafico
        print("=== TODAS AS TAREFAS CONCLUÍDAS ===")
        View.gerar_grafico(self._historico, self._todos_tcbs)


    def executarTarefa(self, tarefa, listaProntas):
        if tarefa is not None:
            tarefa.estado = "executando"
            tarefa.executarTick()
            print(f"{tarefa.id} executou... (Restante: {tarefa.duracaoRestante})")

            if tarefa.estaConcluida():
                print(f"=== TAREFA {tarefa.id} CONCLUÍDA! ===")
                tarefa.estado = "concluida"
                tarefa.concluirTarefa()
                self._tarefaExecutando = None

    def registrarTickNoHistorico(self):
        tick_atual = self._relogio.tickAtual

        if(self._tarefaExecutando is not None):
            id_executando = self._tarefaExecutando.id
            cor_executando = self._tarefaExecutando.cor
        else:
            id_executando = "OCIOSA"
            cor_executando = "CINZA"

        ids_prontas = [t.id for t in self._tarefasProntas.getAll()]
        ids_suspensas= [t.id for t in self._tarefasSuspensas.getAll()]

        # Cria e add o "registro" do tick no historico
        registro = {
            'tick': tick_atual,
            'executando_id': id_executando,
            'executando_cor': cor_executando,
            'prontas': ids_prontas,
            'suspensas': ids_suspensas
        }
        self._historico.append(registro)
        
        print(f"[HISTÓRICO] Tick {tick_atual}: CPU -> {id_executando}")
        print(f"Registro: {registro}")
        print(f"Prontas: {[t.id for t in self._tarefasProntas.getAll()]}")
