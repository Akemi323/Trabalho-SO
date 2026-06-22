import sys
import os

class Memoria:
    def __init__(self , tam):
        self.tam = tam
        self.mem = [0] * tam
        self.tab_particao = []
        self.mmu = MMU()

    def adicionar_particao(self, pid: str, base: int, lim: int):
        self.tab_particao.append([pid, base, lim])
    
    def remover_particao(self, pid: str):
        for i in range(len(self.tab_particao)):
            if self.tab_particao[i][0] == pid:
                self.tab_particao.pop(i)

class MMU:
    #def __init__(self, memoria, tab_particao, lista_processos):
    #    self.memoria = memoria
    #    self.tab_particao = tab_particao
    #    self.lista_processos = lista_processos
        
    @staticmethod
    #sera que assim nao resolve? pq com o while acho que ia ficar muito maior o codigo
    def traduz(pid: str, end_virtual: int, memoria: Memoria):
        for particao in memoria.tab_particao:
            if particao[0] == pid:
                base = particao[1]
                limite = particao[2]
                if end_virtual >= limite:
                    print('Segmentation Fault')
                    return None
                return base + end_virtual
        
class processo:
    def __init__(self, pid: str, tamanho: int):
        self.PID = pid
        self.tamanho = tamanho


def ler_arquivo(caminho: str):
    '''
    Função que lê o arquivo de entrada e retorna uma lista com as informações nele
    4 - Quant de processos
    p01;p02;p03;p04 - PID dos processos
    aloca p01 1000 
    aloca p02 1000  
    aloca p03 1000
    libera p02
    aloca p04 500
    acessa p04 0
    '''
    with open (caminho, "r") as arq:
        arquivo = []
        arquivo.append(int(arq.readline()))
        arquivo.append(arq.readline().strip().split(";"))
        
        for linha in arq:
            arquivo.append(linha.strip().split(" "))
    return arquivo


def first(operacoes: list, memoria: Memoria):
    logs = []
    for op in operacoes:
        print(op)
        if op[0] == 'aloca':
            pid = op[1]
            tam = int(op[2])
            first_aloca(pid, tam, memoria)

            particao = memoria.tab_particao[-1] #pega a ultima particao
            inicio = particao[1]
            fim = inicio + particao[2] - 1
            logs.append(formata_saida('aloca', pid, inicio, fim))
        elif op[0] == 'acessa': 
            memoria.mmu.traduz(op[1], int(op[2]), memoria)
        else:
            verifica_libera(op[1], memoria)
    return logs


def first_acessa(pid: str, end_virtual: int, memoria: Memoria):
    memoria.mmu.traduz(pid, end_virtual, memoria.trab_particao)

def first_aloca(pid: str, tamanho: int, memoria: Memoria):
    if not memoria.tab_particao:
        alocacao(0, tamanho, pid, memoria) # aloca no comeco
    else:
        espacos = verifica_espaco(memoria)
        print(pid)
        print(espacos)
        i = 0
        achou = False
        while i < len(espacos) and not achou:
            if tamanho <= espacos[i][1]:
                achou = True
            else:
                i += 1
        if achou:
            alocacao(espacos[i][0], tamanho, pid, memoria) #aloca no espaco que achou
        else:
            ultimo = (len(memoria.tab_particao) - 1)
            inicio = memoria.tab_particao[ultimo][1] + memoria.tab_particao[ultimo][2]
            alocacao(inicio, tamanho, pid, memoria) #aloca no final
            
def alocacao(inicio: int, tamanho: int, pid: str, memoria: Memoria):  
    '''
    Função que aloca o processo na memória e atualiza a tabela de partição
    '''
    for i in range(inicio, inicio + tamanho):
        memoria.mem[i] = pid
    memoria.adicionar_particao(pid, inicio, tamanho)
    print(memoria.tab_particao)

def verifica_espaco(memoria: Memoria):
    #tab_part [[pid, inicio, tamanho]]
    #espaco [[inicio, tamanho]]
    espacos = []
    tab_part = memoria.tab_particao
    tab_part.sort(key=lambda x: x[1]) #ordenar pelos inicios para fazer as comparações
    if len(tab_part) > 0:
        if tab_part[0][1] != 0:
            espacos.append([0, tab_part[0][1]])
        for i in range(1, len(memoria.tab_particao)):
            espaco = tab_part[i][1] - (tab_part[i-1][1] + tab_part[i-1][2])
            if espaco != 0:
                espacos.append([(tab_part[i-1][1] + tab_part[i-1][2]), espaco])
    inicio_ultimo = tab_part[len(tab_part) - 1][1] + tab_part[len(tab_part) - 1][2]
    i = inicio_ultimo
    while i < memoria.tam and memoria.mem[i] == -1:
        i += 1
    if i != inicio_ultimo:
        espacos.append([inicio_ultimo, i])
    return espacos

def verifica_libera(pid: str, memoria: Memoria):
    i = 0
    achou = False
    while i < len(memoria.tab_particao) and not achou:
        if pid == memoria.tab_particao[i][0]:
            achou = True
        else:
            i += 1
    if achou:
        first_libera(memoria, i)

def first_libera(memoria: Memoria, posicao: int):
    for i in range (memoria.tab_particao[posicao][1], memoria.tab_particao[posicao][1] + memoria.tab_particao[posicao][2]):
        memoria.mem[i] = -1
    del memoria.tab_particao[posicao]

def worst(operacoes: list, memoria: Memoria):
    for op in operacoes:
        if op[0] == 'aloca':
            worst_aloca(op[1], int(op[2]), memoria)
        elif op[0] == 'acessa': 
            memoria.mmu.traduz(op[1], int(op[2]), memoria)
        else:
            verifica_libera(op[1], memoria)

def worst_aloca(pid: str, tamanho: int, memoria: Memoria):
    if not memoria.tab_particao:
        alocacao(0, tamanho, pid, memoria) #aloca no comeco
    else:
        espacos = verifica_espaco(memoria)
        espacos.sort(key=lambda x: x[1], reverse=True)
        print(espacos)
        if  espacos and tamanho <= espacos[0][1]:
            alocacao(espacos[0][0], tamanho, pid, memoria)
            #entra aqui
        else:
            #final
            ultimo = (len(memoria.tab_particao) - 1)
            inicio = memoria.tab_particao[ultimo][1] + memoria.tab_particao[ultimo][2]
            alocacao(inicio, tamanho, pid, memoria) #aloca no final
    
def best(operacoes: list, memoria: Memoria):
    for op in operacoes:
        if op[0] == 'aloca':
            best_aloca(op[1], int(op[2]), memoria)
        elif op[0] == 'acessa': 
            memoria.mmu.traduz(op[1], int(op[2]), memoria)
        else:
            verifica_libera(op[1], memoria)
    # Aloca no menor espaço disponivel (frag externa)
    pass

def best_aloca(pid: str, tamanho: int, memoria: Memoria):
    if not memoria.tab_particao:
        alocacao(0, tamanho, pid, memoria) #aloca no comeco
    else:
        espacos = verifica_espaco(memoria)
        espacos.sort(key=lambda x: x[1])
        print(espacos)
        if  espacos and tamanho <= espacos[0][1]:
            alocacao(espacos[0][0], tamanho, pid, memoria)
            #entra aqui
        else:
            #final
            ultimo = (len(memoria.tab_particao) - 1)
            inicio = memoria.tab_particao[ultimo][1] + memoria.tab_particao[ultimo][2]
            alocacao(inicio, tamanho, pid, memoria) #aloca no final

def buddy():
    # muita coisa
    pass

def acessa_memoria(memoria: Memoria, MMU: MMU, pid: str, end_virtual: int):
    end_fisico = MMU.traduz(pid, end_virtual)
    if end_fisico is not None:
        conteudo = memoria.memoria[end_fisico]
        print(f"O conteúdo da memória RAM nessa posição é {conteudo}")
    else:
        print("Erro")
        
def saida_arquivo(caminho: str, saida: list):
    '''
    alocacao p01 0 999
    alocacao p02 1000 1999
    alocacao p03 2000 2999
    liberacao p02 1000 1999
    alocacao p04 1000 1499
    acesso p04 0 1000
    '''
    with open(caminho, 'w') as arq:
        for linha in saida:
            arq.write(linha + '\n')
 
def formata_saida(operacao: str, pid: str, inicio: int, fim: int):
    if operacao == 'aloca':
        linha = f"alocacao {pid} {inicio} {fim}"
    elif operacao == 'libera':
        linha = f"liberacao {pid} {inicio} {fim}"
    else:
        linha = f"acesso {pid} {inicio} {fim}"
    return linha
    
def main():    
    caminho_entrada = sys.argv[1]
    estrategia = sys.argv[2]
    caminho_saida = "saida.txt"

    arq = ler_arquivo(caminho_entrada)
    qtd_processos = arq[0]
    pids = arq [1]
    operacoes = arq [2:]
    
    memoria = Memoria(4096)
    logs = []
    
    if estrategia == 'first':
        logs = first(operacoes, memoria)
        print(memoria.mem[:1000])
    elif estrategia == 'worst':
        worst(operacoes, memoria)
        print(memoria.mem[:1000])
    elif estrategia == 'best':
        best(operacoes, memoria)
        print(memoria.mem[:1000])
    elif estrategia == 'buddy':
        pass
    else:
        print('Erro')
    #salvar_saida(linha, tarefas, caminho_saida)

    #arg 1 = estrategia de alocacao
    #arg 2 = caminho do arquivo de entrada
    #Leitura do arquivo de entrada
    #Inicialização da memória RAM, dos processos e da tabela de partição
    #Tratamento de requisições - escrita no arquivo de log de saída
    #Encerramento da simulação' 

    if logs:
        saida_arquivo(caminho_saida, logs)

if __name__ == '__main__':
    main()