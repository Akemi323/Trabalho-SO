import sys

class Memoria:
    def __init__(self , tam):
        self.tam = tam
        self.mem = [0] * tam

class MMU:
    def __init__(self, memoria, tab_particao, lista_processos):
        self.memoria = memoria
        self.tab_particao = tab_particao
        self.lista_processos = lista_processos

class Tab_particao:
    def __init__():
        pass

class processo:
    def __init__(self, pid, endereco):
        self.PID = pid
        self.endereco = endereco

def ler_arquivo():
    pass

def first():
    #Aloca no primeiro espaço disponivel
    pass
    # chamar o arquivo, ler a quatidade de processos, ler os processos, 
    # salvar as proximas operacoes numa lista for op em operacoes
    # aloca..... first
    # libera ... first
    # 

def worst():
    pass

def best():
    pass

def buddy():
    pass



def main():
    #arg 1 = estrategia de alocacao
    #arg 2 = caminho do arquivo de entrada
    #Leitura do arquivo de entrada
    #Inicialização da memória RAM, dos processos e da tabela de partição
    #Tratamento de requisições - escrita no arquivo de log de saída
    #Encerramento da simulação