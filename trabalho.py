import sys
import os
import math

class Memoria:
    def __init__(self , tam, arquivo_saida):
        self.tam = tam
        self.mem = [0] * tam
        self.tab_particao = []
        self.mmu = MMU()
        self.arquivo_saida = arquivo_saida

    def adicionar_particao(self, pid: str, base: int, lim: int):
        '''
        '''
        self.tab_particao.append([pid, base, lim])
    
    def remover_particao(self, pid: str):
        '''
        '''
        for i in range(len(self.tab_particao)):
            if self.tab_particao[i][0] == pid:
                self.tab_particao.pop(i)
    
    def buddy_particao():
        pass

class MMU:
    #def __init__(self, memoria, tab_particao, lista_processos):
    #    self.memoria = memoria
    #    self.tab_particao = tab_particao
    #    self.lista_processos = lista_processos
        
    @staticmethod
    #sera que assim nao resolve? pq com o while acho que ia ficar muito maior o codigo
    def traduz(pid: str, end_virtual: int, memoria: Memoria):
        '''
        '''
        for particao in memoria.tab_particao:
            if particao[0] == pid:
                base = particao[1]
                limite = particao[2]
                if end_virtual >= limite:
                    memoria.arquivo_saida.write(f"Segmentation Fault {pid} {end_virtual}" + '\n')
                    return None
                memoria.arquivo_saida.write(f"acesso {pid} {end_virtual} {base + end_virtual}" + '\n')
                return None
        
        
class processo:
    def __init__(self, pid: str, tamanho: int):
        '''
        '''
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
    '''
    '''
    logs = []
    for op in operacoes:
        if op[0] == 'aloca':
            #pid = op[1]
            #tam = int(op[2])
            first_aloca(op[1], int(op[2]), memoria)

            #particao = memoria.tab_particao[-1] #pega a ultima particao
            #inicio = particao[1]
            #fim = inicio + particao[2] - 1
            #logs.append(formata_saida('aloca', pid, inicio, fim))
        elif op[0] == 'acessa': 
            memoria.mmu.traduz(op[1], int(op[2]), memoria)
            #logs.append(formata_saida('acesso', op[1], int(op[2]), int(op[2])))
        else:
            verifica_libera(op[1], memoria)
            #logs.append(formata_saida('libera', op[1], 0, 0))
    #return logs


def first_acessa(pid: str, end_virtual: int, memoria: Memoria):
    '''
    '''
    memoria.mmu.traduz(pid, end_virtual, memoria.trab_particao)

def first_aloca(pid: str, tamanho: int, memoria: Memoria):
    '''
    '''
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
    memoria.arquivo_saida.write(f"alocacao {pid} {inicio} {inicio+tamanho-1}" + '\n')
    #logs.append(formata_saida('aloca', pid, inicio, inicio + tamanho))

def verifica_espaco(memoria: Memoria):
    '''
    '''
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
    termino = tab_part[len(tab_part) - 1][1] + tab_part[len(tab_part) - 1][2]
    tamanho_final = memoria.tam - termino
    espacos.append([termino, tamanho_final])
    return espacos

def verifica_libera(pid: str, memoria: Memoria):
    '''
    '''
    i = 0
    achou = False
    while i < len(memoria.tab_particao) and not achou:
        if pid == memoria.tab_particao[i][0]:
            achou = True
        else:
            i += 1
    if achou:
        libera(memoria, i)

def libera(memoria: Memoria, posicao: int):
    '''
    '''
    for i in range (memoria.tab_particao[posicao][1], memoria.tab_particao[posicao][1] + memoria.tab_particao[posicao][2]):
        memoria.mem[i] = 0
    memoria.arquivo_saida.write(f"liberacao {memoria.tab_particao[posicao][0]} {memoria.tab_particao[posicao][1]} {memoria.tab_particao[posicao][1] + memoria.tab_particao[posicao][2] - 1}" + '\n')
    del memoria.tab_particao[posicao]
    

def worst(operacoes: list, memoria: Memoria):
    '''
    '''
    for op in operacoes:
        if op[0] == 'aloca':
            worst_aloca(op[1], int(op[2]), memoria)
        elif op[0] == 'acessa': 
            memoria.mmu.traduz(op[1], int(op[2]), memoria)
        else:
            verifica_libera(op[1], memoria)

def worst_aloca(pid: str, tamanho: int, memoria: Memoria):
    '''
    '''
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
    '''
    '''
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
    '''
    '''
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
    '''
    '''
    for op in operacoes:
        if op[0] == 'aloca':
            buddy_aloca(op[1], int(op[2]), memoria)
        elif op[0] == 'acessa': 
            memoria.mmu.traduz(op[1], int(op[2]), memoria)
        else:
            buddy_libera(op[1], memoria)
    # muita coisa

def buddy_aloca(pid: str, tamanho: int, memoria: Memoria):
    '''
    '''
    if not memoria.tab_particao:
        # [4096]
        # [2048] [2048]
        # [1024] [1024] [2048]
        # [512][512][1024][2048]
        # 
        
    else:
        espacos = verifica_espaco(memoria)
        espacos.sort(key=lambda x: x[1])
        
        
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
    '''
    '''
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
    
    
    #logs = []
    
    with open(caminho_saida, "a") as arquivo:
        memoria = Memoria(4096, arquivo)
        if estrategia == 'first':
            #first(operacoes, memoria)
        elif estrategia == 'worst':
            worst(operacoes, memoria)
            #print(memoria.mem[:1000])
        elif estrategia == 'best':
            best(operacoes, memoria)
            #print(memoria.mem[:1000])
        elif estrategia == 'buddy':
            #buddy(operacoes, memoria)
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
3
    #if logs:
     #   saida_arquivo(caminho_saida, logs)

if __name__ == '__main__':
    main()

    #for i in range(1, 10):
     #   try:
      #      plotar_linha_temporal(f"entrada{i}.txt", f"log_entrada{i}_{estrategia}.txt")
       # except FileNotFoundError:
        #    print(f"Arquivo cenario{i}.csv não encontrado. Pulando...")

            
#def registrar_log_auxiliar(arquivo_aberto, mensagem):
 #   # A função recebe o arquivo e escreve nele normalmente
  #  arquivo_aberto.write(f"[FUNÇÃO] {mensagem}\n")

# Escopo principal
#with open("meu_log.txt", "w") as arquivo:
 #   for i in range(5):
  #      resultado = i * 2
   #     arquivo.write(f"Iteração {i}: resultado={resultado}\n")
        
        # Chamando a função e passando o arquivo como argumento
    #    if resultado > 4:
     #       registrar_log_auxiliar(arquivo, f"Aviso: resultado {resultado} é maior qu