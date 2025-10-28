# ViewHTML.py - Gera gráfico em HTML com cores
from collections import defaultdict
import os
from datetime import datetime

def busca_tcb_por_id(id_tarefa, lista_todos_tcbs):
    for tcb_atual in lista_todos_tcbs:
        if str(tcb_atual.id) == str(id_tarefa):
            return tcb_atual
    return None

def gerar_grafico(historico, lista_todos_tcbs, nome_saida="grafico_escalonamento.html"):
    if not historico:
        print("Histórico vazio - não há dados para gerar gráfico")
        return
    
    # Construir blocos de tempo de execução
    blocos_tempo = defaultdict(list)
    tarefa_anterior = None
    inicio_bloco_atual = 0
    cor_anterior = "#888888"
    
    for registro in historico:
        tick_atual = registro['tick']
        tarefa_atual = registro['executando_id']
        cor_atual = registro.get('executando_cor', '#888888')

        if tarefa_atual != tarefa_anterior:
            if tarefa_anterior is not None and tarefa_anterior != "OCIOSA":
                duracao = tick_atual - inicio_bloco_atual
                if duracao > 0:
                    blocos_tempo[tarefa_anterior].append(
                        (inicio_bloco_atual, duracao, cor_anterior)
                    )
            
            inicio_bloco_atual = tick_atual
            cor_anterior = cor_atual

        tarefa_anterior = tarefa_atual

    # Último bloco
    if tarefa_anterior is not None and tarefa_anterior != "OCIOSA":
        tempo_fim_simulacao = historico[-1]['tick'] + 1
        duracao = tempo_fim_simulacao - inicio_bloco_atual
        if duracao > 0:
            blocos_tempo[tarefa_anterior].append(
                (inicio_bloco_atual, duracao, cor_anterior)
            )

    # Calcular blocos de espera
    blocos_espera = defaultdict(list)
    
    for tarefa_id, blocos in blocos_tempo.items():
        tcb_da_tarefa = busca_tcb_por_id(tarefa_id, lista_todos_tcbs)
        if tcb_da_tarefa is None:
            continue

        tempo_ingresso = tcb_da_tarefa.ingresso
        ponto_de_partida = tempo_ingresso
        
        blocos.sort(key=lambda x: x[0])

        for inicio_exec, duracao_exec, _ in blocos:
            if inicio_exec > ponto_de_partida:
                duracao_espera = inicio_exec - ponto_de_partida
                blocos_espera[tarefa_id].append(
                    (ponto_de_partida, duracao_espera, "#E5E7EB")
                )
            
            ponto_de_partida = inicio_exec + duracao_exec

    # Preparar dados para HTML
    todas_ids = list(blocos_tempo.keys())
    if not todas_ids:
        print("Nenhuma tarefa executou - gráfico vazio")
        return
        
    tarefas_ids_ordenadas = sorted(todas_ids)
    tempo_total = historico[-1]['tick'] + 1

    # Gerar HTML
    html_content = gerar_html(tarefas_ids_ordenadas, blocos_tempo, blocos_espera, tempo_total, historico)
    
    # Salvar arquivo
    with open(nome_saida, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Gráfico HTML salvo como {nome_saida}")
    print(f"Abra o arquivo no navegador para visualizar o gráfico!")

def gerar_html(tarefas_ids, blocos_tempo, blocos_espera, tempo_total, historico):
    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gráfico de Escalonamento</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .info-panel {{
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .stat-card {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            color: #7f8c8d;
            margin-top: 5px;
        }}
        
        .legenda {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
            padding: 15px;
            background: white;
            border-radius: 10px;
        }}
        
        .legenda-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .legenda-cor {{
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 2px solid #ddd;
        }}
        
        .grafico-container {{
            padding: 30px;
            overflow-x: auto;
        }}
        
        .linha-tarefa {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            height: 50px;
        }}
        
        .tarefa-label {{
            width: 80px;
            font-weight: bold;
            color: #2c3e50;
            text-align: right;
            padding-right: 15px;
        }}
        
        .linha-tempo {{
            display: flex;
            flex: 1;
            height: 40px;
            background: #f8f9fa;
            border-radius: 8px;
            overflow: hidden;
            position: relative;
            border: 1px solid #e9ecef;
        }}
        
        .bloco {{
            height: 100%;
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .bloco:hover {{
            transform: scale(1.05);
            z-index: 2;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }}
        
        .bloco.execucao {{
            border-right: 1px solid rgba(255,255,255,0.3);
        }}
        
        .bloco.espera {{
            background: #E5E7EB !important;
        }}
        
        .eixo-tempo {{
            display: flex;
            margin-left: 80px;
            margin-bottom: 20px;
        }}
        
        .tick-tempo {{
            flex: 1;
            text-align: center;
            font-size: 0.8em;
            color: #7f8c8d;
            border-top: 1px solid #bdc3c7;
            padding-top: 5px;
        }}
        
        .tick-tempo.principal {{
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .tooltip {{
            position: absolute;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.9em;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 10;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #7f8c8d;
            border-top: 1px solid #e9ecef;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}
            
            .grafico-container {{
                padding: 15px;
            }}
            
            .tarefa-label {{
                width: 60px;
                font-size: 0.9em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Gráfico de Escalonamento</h1>
            <div class="subtitle">Visualização do Escalonador de Tarefas</div>
        </div>
        
        <div class="info-panel">
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{len(tarefas_ids)}</div>
                    <div class="stat-label">Tarefas</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{tempo_total}</div>
                    <div class="stat-label">Ticks Totais</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(historico)}</div>
                    <div class="stat-label">Registros</div>
                </div>
            </div>
            
            <div class="legenda">
                <div class="legenda-item">
                    <div class="legenda-cor" style="background: #E5E7EB;"></div>
                    <span>Tempo de Espera</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background: #888888;"></div>
                    <span>CPU Ociosa</span>
                </div>
            </div>
        </div>
        
        <div class="grafico-container">
            <div class="eixo-tempo">
                {gerar_eixo_tempo(tempo_total)}
            </div>
            
            {gerar_linhas_tarefas(tarefas_ids, blocos_tempo, blocos_espera, tempo_total)}
        </div>
        
        <div class="footer">
            Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | 
            Sistema de Escalonamento
        </div>
    </div>
    
    <div id="tooltip" class="tooltip"></div>

    <script>
        function mostrarTooltip(elemento, texto) {{
            const tooltip = document.getElementById('tooltip');
            const rect = elemento.getBoundingClientRect();
            
            tooltip.innerHTML = texto;
            tooltip.style.left = (rect.left + rect.width / 2) + 'px';
            tooltip.style.top = (rect.top - 40) + 'px';
            tooltip.style.opacity = '1';
        }}
        
        function esconderTooltip() {{
            document.getElementById('tooltip').style.opacity = '0';
        }}
        
        // Adicionar eventos aos blocos
        document.addEventListener('DOMContentLoaded', function() {{
            const blocos = document.querySelectorAll('.bloco');
            blocos.forEach(bloco => {{
                bloco.addEventListener('mouseenter', function(e) {{
                    const texto = this.getAttribute('data-tooltip');
                    if (texto) {{
                        mostrarTooltip(this, texto);
                    }}
                }});
                
                bloco.addEventListener('mouseleave', esconderTooltip);
            }});
        }});
    </script>
</body>
</html>
"""

def gerar_eixo_tempo(tempo_total):
    ticks = ""
    for tick in range(0, tempo_total + 1):
        if tick % 5 == 0 or tick == tempo_total:
            classe = "tick-tempo principal"
            label = str(tick)
        else:
            classe = "tick-tempo"
            label = "•"
        ticks += f'<div class="{classe}">{label}</div>'
    return ticks

def gerar_linhas_tarefas(tarefas_ids, blocos_tempo, blocos_espera, tempo_total):
    linhas = ""
    
    for tarefa_id in tarefas_ids:
        # Combinar todos os blocos (espera + execução)
        todos_blocos = []
        
        # Adicionar blocos de espera
        if tarefa_id in blocos_espera:
            for inicio, duracao, cor in blocos_espera[tarefa_id]:
                todos_blocos.append(('espera', inicio, duracao, cor))
        
        # Adicionar blocos de execução
        if tarefa_id in blocos_tempo:
            for inicio, duracao, cor in blocos_tempo[tarefa_id]:
                todos_blocos.append(('execucao', inicio, duracao, cor))
        
        # Ordenar por tempo de início
        todos_blocos.sort(key=lambda x: x[1])
        
        # Preencher gaps com ociosidade
        blocos_completos = []
        tempo_atual = 0
        
        for tipo, inicio, duracao, cor in todos_blocos:
            # Gap antes deste bloco
            if inicio > tempo_atual:
                blocos_completos.append(('ocioso', tempo_atual, inicio - tempo_atual, '#f8f9fa'))
            
            blocos_completos.append((tipo, inicio, duracao, cor))
            tempo_atual = inicio + duracao
        
        # Gap final
        if tempo_atual < tempo_total:
            blocos_completos.append(('ocioso', tempo_atual, tempo_total - tempo_atual, '#f8f9fa'))
        
        # Gerar HTML dos blocos
        blocos_html = ""
        for tipo, inicio, duracao, cor in blocos_completos:
            if duracao > 0:
                largura = (duracao / tempo_total) * 100
                estilo = f"width: {largura}%; background: {cor};"
                
                if tipo == 'execucao':
                    tooltip = f"Tarefa {tarefa_id}<br>Executando: ticks {inicio}-{inicio+duracao-1}<br>Duração: {duracao} ticks"
                    classe = "bloco execucao"
                elif tipo == 'espera':
                    tooltip = f"Tarefa {tarefa_id}<br>Esperando: ticks {inicio}-{inicio+duracao-1}<br>Duração: {duracao} ticks"
                    classe = "bloco espera"
                else:
                    tooltip = f"Tarefa {tarefa_id}<br>Não ingressou ainda: ticks {inicio}-{inicio+duracao-1}"
                    classe = "bloco"
                
                blocos_html += f'<div class="{classe}" style="{estilo}" data-tooltip="{tooltip}"></div>'
        
        linhas += f'''
        <div class="linha-tarefa">
            <div class="tarefa-label">{tarefa_id}</div>
            <div class="linha-tempo">
                {blocos_html}
            </div>
        </div>
        '''
    
    return linhas
