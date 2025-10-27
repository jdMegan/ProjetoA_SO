# Esse modulo View contem as funcoes necessarias para construir o grafico

import matplotlib.pyplot as plt # Parecido com matlab pra graficos
from collections import defaultdict # Cria as listas vazias ao inves de dar erro, se nao existirem

# Cor do tempo que a tarefa esta ociosa
COR_ESPERA = 'lightgray'

def busca_tcb_por_id(id_tarefa, lista_todos_tcbs):
    for tcb_atual in lista_todos_tcbs:
        if tcb_atual.id == id_tarefa:
            return tcb_atual
    return None # Se não achar

def gerar_grafico(historico, lista_todos_tcbs, nome_saida="grafico.png"):
        
    # verifica quem rodou e constroi os blocos de tempo de execucao
    blocos_tempo = defaultdict(list) # vai guardar os blocos de tempo que cada tarefa rodou.
    # os blocos sao as partes coloridas do grafico, onde aparece quem rodou
    # [t01: (começou, durou, cor), t02]

    tarefa_anterior = None
    inicio_bloco_atual = 0
    cor_anterior = None
    
    # Para cada instante do registro/tick...
    for indice, registro in enumerate(historico):
        tick_atual = registro['tick']
        tarefa_atual = registro['executando_id']
        cor_atual = registro.get('executando_cor', 'gray') # A cor da tarefa rodando, cinza se nao tiver

        if tarefa_atual != tarefa_anterior:
            # quer dizer q a anterior acabou de ser interrompida ou terminou
           #  só salva um bloco de tempo quando ele é interrompido por uma nova tarefa.
            if tarefa_anterior is not None and tarefa_anterior != "OCIOSA":
                duracao = tick_atual - inicio_bloco_atual # Calcula quanto tempo ela rodou
                if duracao > 0:
                    # Salva o bloco que acabou de rodar na lista da tarefa anterior.
                    blocos_tempo[tarefa_anterior].append(
                        (inicio_bloco_atual, duracao, cor_anterior)
                    )
            
            # começa um novo bloco da nova tarefa
            inicio_bloco_atual = tick_atual
            cor_anterior = cor_atual

        tarefa_anterior = tarefa_atual

    # como a tarefa soh salva um bloco de tempo la dentro do loop, 
    # tem q lidar com a ult tarefa aq fora
    
    if tarefa_anterior is not None and tarefa_anterior != "OCIOSA":

        # esta determinando o final do bloco
         # historico[-1] pega o último registro da lista, dai adiciona +1
        tempo_fim_simulacao = historico[-1]['tick'] + 1
    #   # Calculando a duração do último bloco
        duracao = tempo_fim_simulacao - inicio_bloco_atual

        # salva o bloco
        if duracao > 0:
            blocos_tempo[tarefa_anterior].append(
                (inicio_bloco_atual, duracao, cor_anterior)
            )

    # calcula o blocos de tempo de espera
    blocos_espera = defaultdict(list) #vai guardar os blocos de tempo que a tarefa ficou esperando (cinza)
    
    # Para cada tarefa que executou....
    for tarefa_id, blocos in blocos_tempo.items():
        # procuro o tcb dessa tarefa
        tcb_da_tarefa = busca_tcb_por_id(tarefa_id, lista_todos_tcbs)
        if tcb_da_tarefa is None: continue #se nao achar, pula

        tempo_ingresso = tcb_da_tarefa.ingresso 
        ponto_de_partida = tempo_ingresso
        
        # Ordena os blocos por tempo de inicio
        #  bloco eh (inicio_fatia_atual, duracao, cor_anterior), entao esta ordenando pelo [0] 
        # que eh o inicio_bloco_atual
        blocos.sort(key=lambda x: x[0]) 

        for inicio_exec, duracao_exec, _ in blocos:
            # Se o bloco de execução NÃO começa logo após o ponto de partida:
            if inicio_exec > ponto_de_partida:
                duracao_espera = inicio_exec - ponto_de_partida
                
                # Registra o bloco cinza de espera
                blocos_espera[tarefa_id].append(
                    (ponto_de_partida, duracao_espera, COR_ESPERA)
                )
            
            # O próximo ponto de partida para a espera é o fim deste bloco colorido.
            ponto_de_partida = inicio_exec + duracao_exec
            
    # Desenhar o grafico 
    todas_ids = list(blocos_tempo.keys())
    tarefas_ids_ordenadas = sorted(todas_ids, reverse=True) # Ordena de trás para frente no graf ta t05,t04
    
    # Cria uma figura(fundo) e os eixos
    fig, eixos = plt.subplots(figsize=(14, 6)) # tamanho da figura eh de 14x6 polegadas
    
    # define as posições Y para que cada tarefa tenha a sua linha
    tarefas_y_pos = range(len(tarefas_ids_ordenadas))[::-1] 
    # une a tarefas_ids_ordenadas com a tarefas_y_pos pelo id criando um dicionario t01 = 2, t02 = 3...
    # quer dizer que sempre q eu for escrever na t01 eu olho no dicionario e sei que preciso
    # escrever na posicao 2 do eixo Y
    y_map = {id: y for id, y in zip(tarefas_ids_ordenadas, tarefas_y_pos)}
    
    # impressao das barras
    for tarefa_id in tarefas_ids_ordenadas:
        # usa o dicionário y_map encontrando a posição no eixo Y, onde vai desenhar a tarefa
        y_pos = y_map[tarefa_id]
        
        # desenha os bloquinhos de espera cinzas primiero
        # se aa tarefa atual tem algum tempo de espera registrado no dicionário blocos_espera
        if tarefa_id in blocos_espera:
            for inicio, duracao, cor in blocos_espera[tarefa_id]:
                 # eixos.broken_barh desenha um bloco horizontal quebrado no eixo x
                 eixos.broken_barh(
                    [(inicio, duracao)], # Onde começa e quanto dura no eixo X
                    (y_pos - 0.4, 0.8),  # Posição vertical e altura no eixo Y
                    facecolors=(cor)     # Pinta de cinza
                )

        # desenha os blocos de execucao coloridos
        if tarefa_id in blocos_tempo:
            for inicio, duracao, cor in blocos_tempo[tarefa_id]:
                eixos.broken_barh(
                    [(inicio, duracao)],  
                    (y_pos - 0.4, 0.8),   
                    facecolors=(cor)      # Pinta com a cor da tarefa
                )

    # Cinfigura os labels do grafico
    # pega o ultimo tick + 1
    tempo_total = historico[-1]['tick'] + 1
    
    # Add os labels do eixo Y que sao os ids das tarefas
    # descobre onde escrever com o dicionario de mapa de posicoes tarefas_y_pos
    eixos.set_yticks(tarefas_y_pos)
    # pega os nomes das tarefas em tarefas_ids_ordenadas
    eixos.set_yticklabels(tarefas_ids_ordenadas) 
    # coloca o titulo do eixo Y
    eixos.set_ylabel("Tarefas")
    
    # Add os labels do eixo X que sao os ticks
    # coloca o titulo do eixo X
    eixos.set_xlabel("Tempo (Ticks do Relógio)")
    # define os ticks de 0 ate o final
    eixos.set_xlim(0, tempo_total)
    
    # Calcula os locais de cada tick.
    tick_locs = range(tempo_total + 1)
    # define a linha com os ticks
    eixos.set_xticks(tick_locs)
    # tranforma os ticks em string e add a label
    eixos.set_xticklabels([str(t) for t in tick_locs])
    
    # Coloca linhas pontilhadas verticais para ajudar a ler os ticks
    eixos.grid(True, axis='x', linestyle='--', alpha=0.6)

    plt.title("Gráfico")
    
    # Salva o desenho como um arquivo de imagem!
    plt.savefig(nome_saida)
    print(f"Gráfico salvo!")