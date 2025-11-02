import SistemaOperacional

print("Iniciando Sistema Operacional...")

caminho = input("Digite caminho para o arquivo de configurações: ").strip()

so = SistemaOperacional.SistemaOperacional(caminho)

try:
    so = SistemaOperacional.SistemaOperacional(caminho)
except Exception as e:
    print("Erro no caminho, o arquivo não foi encontrado.")
