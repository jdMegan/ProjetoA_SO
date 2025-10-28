# ViewASCII.py - Versão alternativa sem matplotlib
from collections import defaultdict

COR_ESPERA = '█'
COR_EXECUCAO = '▓'
COR_OCIOSA = '░'

def busca_tcb_por_id(id_tarefa, lista_todos_tcbs):
    for tcb_atual in lista_todos_tcbs:
        if str(tcb_atual.id) == str(id_tarefa):
            return tcb_atual
    return None

def gerar_grafico_ascii(historico, lista_todos_tcbs):
    if not historico:
        print("Histórico vazio - não há dados para gerar gráfico")
        return
    
    # Construir blocos de tempo
    blocos_tempo = defaultdict(list)
    tarefa_anterior = None
    inicio_bloco_atual = 0
    
    for registro in historico:
        tick_atual = registro['tick']
        tarefa_atual = registro['executando_id']

        if tarefa_atual != tarefa_anterior:
            if tarefa_anterior is not None and tarefa_anterior != "OCIOSA":
                duracao = tick_atual - inicio_bloco_atual
                if duracao > 0:
                    blocos_tempo[tarefa_anterior].append((inicio_bloco_atual, duracao))
            
            inicio_bloco_atual = tick_atual
        tarefa_anterior = tarefa_atual

    # Último bloco
    if tarefa_anterior is not None and tarefa_anterior != "OCIOSA":
        tempo_fim_simulacao = historico[-1]['tick'] + 1
        duracao = tempo_fim_simulacao - inicio_bloco_atual
        if duracao > 0:
            blocos_tempo[tarefa_anterior].append((inicio_bloco_atual, duracao))

    # Gerar gráfico ASCII
    todas_tarefas = sorted(list(blocos_tempo.keys()))
    tempo_total = historico[-1]['tick'] + 1
    
    print("\n" + "="*60)
    print("GRÁFICO DE ESCALONAMENTO (ASCII)")
    print("="*60)
    print(f"Legenda: {COR_EXECUCAO} = Executando | {COR_ESPERA} = Espera | {COR_OCIOSA} = Ocioso")
    print("="*60)
    
    for tarefa_id in todas_tarefas:
        linha = f"{tarefa_id:>5} | "
        
        for tick in range(tempo_total):
            executando = False
            for inicio, duracao in blocos_tempo[tarefa_id]:
                if inicio <= tick < inicio + duracao:
                    linha += COR_EXECUCAO
                    executando = True
                    break
            
            if not executando:
                # Verificar se a tarefa já ingressou
                tcb = busca_tcb_por_id(tarefa_id, lista_todos_tcbs)
                if tcb and tick >= tcb.ingresso:
                    linha += COR_ESPERA
                else:
                    linha += COR_OCIOSA
        
        print(linha)
    
    # Linha do tempo
    linha_tempo = "      | "
    for tick in range(tempo_total):
        if tick % 5 == 0:
            linha_tempo += str(tick)
        else:
            linha_tempo += " "
    
    print(" " * 7 + "-" * (tempo_total + 1))
    print(linha_tempo)
    print("="*60)

# Função compatível com a interface original
def gerar_grafico(historico, lista_todos_tcbs, nome_saida="grafico.txt"):
    gerar_grafico_ascii(historico, lista_todos_tcbs)
    
    # Salvar em arquivo também
    with open(nome_saida, 'w') as f:
        import sys
        from io import StringIO
        
        old_stdout = sys.stdout
        sys.stdout = string_buffer = StringIO()
        
        gerar_grafico_ascii(historico, lista_todos_tcbs)
        
        sys.stdout = old_stdout
        f.write(string_buffer.getvalue())
    
    print(f"Gráfico ASCII salvo como {nome_saida}")
