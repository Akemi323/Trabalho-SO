import sys
import os
import math

class Memoria:
    def __init__(self , tam, arquivo_saida):
        '''
        Inicialização da memória, em que todas os objetos estão armazenados
        '''
        self.tam = tam
        self.mem = [0] * tam
        self.tab_particao = [processo(-1, 0, tam)]
        self.mmu = MMU()
        self.arquivo_saida = arquivo_saida
        self.processo = processo

    def adicionar_particao(self, pid: str, base: int, lim: int):
        '''
        Método que adiciona o processo na tabela de partição, ela recebe os elementos diretamente do arquivo
        e cria um objeto processo, que é adicionado na lista de partições
        '''
        processo = self.processo(pid, base, lim)
        self.tab_particao.append(processo)
    
    def remover_particao(self, pid: str):
        '''
        Método que remove o processo da tabela de partição, ela recebe o pid do processo e remove o objeto
        '''
        for i in range(len(self.tab_particao)):
            if self.tab_particao[i].pid == pid:
                self.tab_particao.pop(i)

class MMU:
        
    @staticmethod
    #sera que assim nao resolve? pq com o while acho que ia ficar muito maior o codigo
    def traduz(pid: str, end_virtual: int, memoria: Memoria):
        '''
        Método que realiza a tradução de um endereço virtual em um endereço lógico,
        fazendo a soma da base
        Ela faz também uma verificação: Se o endereço que vai ser alocado for maior do que o espaço disponível,
        retorna um erro de segmentação
        '''
        for particao in memoria.tab_particao:
            if particao.pid == pid:
                base = particao.base
                limite = particao.tamanho
                if end_virtual >= limite:
                    memoria.arquivo_saida.write(f"Segmentation Fault {pid} {end_virtual}" + '\n')
                    return None
                memoria.arquivo_saida.write(f"acesso {pid} {end_virtual} {base + end_virtual}" + '\n')
                return None
        
class processo:
    def __init__(self, pid: str, base: int, tamanho: int):
        '''
        Inicialização de um processo, que vai ser adicionado posteriormente na tabela de partição
        '''
        self.pid = pid
        self.base = base
        self.tamanho = tamanho

    def __repr__(self):
        return f"{{Pid: {self.pid}, Base: {self.base}, Tam: {self.tamanho}}}"

def ler_arquivo(caminho: str):
    '''
    Função que lê o arquivo de entrada e retorna uma lista com as informações nele
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
    Função que organiza o método de alocação first, fazendo a chamada de função de cada
    uma das operações a serem realizadas: Acesso, Alocação e Liberação 
    '''
    for op in operacoes:
        if op[0] == 'aloca':
            first_aloca(op[1], int(op[2]), memoria)
        elif op[0] == 'acessa': 
            memoria.mmu.traduz(op[1], int(op[2]), memoria)
        else:
            busca_libera(op[1], memoria)

def first_aloca(pid: str, tamanho: int, memoria: Memoria):
    '''
    Função que realiza a alocação da estratégia first fit
    Considera os seguintes casos
    1. Fazer a alocação no início da memória
    2. Fazer a alocação no meio da memória
    3. Fazer a alocação no final da memória
    '''
    if len(memoria.tab_particao) == 1:
        if memoria.tab_particao[0].pid == -1 and tamanho <= memoria.tam:
            alocacao(0, tamanho, pid, memoria) # aloca no comeco
        else:
            print("erro")
    else:
        espacos = verifica_espaco(memoria)
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

def worst(operacoes: list, memoria: Memoria):
    '''
    Função que organiza o método de alocação worst, fazendo a chamada de função de cada
    uma das operações a serem realizadas: Acesso, Alocação e Liberação 
    '''
    for op in operacoes:
        if op[0] == 'aloca':
            worst_aloca(op[1], int(op[2]), memoria)
        elif op[0] == 'acessa': 
            memoria.mmu.traduz(op[1], int(op[2]), memoria)
        else:
            busca_libera(op[1], memoria)

def worst_aloca(pid: str, tamanho: int, memoria: Memoria):
    '''
    Função que realiza a alocação da estratégia worst fit
    Considera os seguintes casos
    1. Fazer a alocação no início da memória
    2. Fazer a alocação no meio da memória
    3. Fazer a alocação no final da memória
    '''
    if len(memoria.tab_particao) == 1:
        if memoria.tab_particao[0].pid == -1 and tamanho <= memoria.tam:
            alocacao(0, tamanho, pid, memoria) # aloca no comeco
        else:
            print("erro")
    else:
        espacos = verifica_espaco(memoria)
        espacos.sort(key=lambda x: x[1], reverse=True)
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
    Função que organiza o método de alocação best, fazendo a chamada de função de cada
    uma das operações a serem realizadas: Acesso, Alocação e Liberação 
    '''
    for op in operacoes:
        if op[0] == 'aloca':
            best_aloca(op[1], int(op[2]), memoria)
        elif op[0] == 'acessa': 
            memoria.mmu.traduz(op[1], int(op[2]), memoria)
        else:
            busca_libera(op[1], memoria)
    # Aloca no menor espaço disponivel (frag externa)
    pass

def best_aloca(pid: str, tamanho: int, memoria: Memoria):
    '''
    Função que realiza a alocação da estratégia best fit
    Considera os seguintes casos
    1. Fazer a alocação no início da memória
    2. Fazer a alocação no meio da memória
    3. Fazer a alocação no final da memória
    '''
    if len(memoria.tab_particao) == 1:
        if memoria.tab_particao[0].pid == -1 and tamanho <= memoria.tam:
            alocacao(0, tamanho, pid, memoria) # aloca no comeco
        else:
            print("erro")
    else:
        espacos = verifica_espaco(memoria)
        espacos.sort(key=lambda x: x[1])
        if  espacos and tamanho <= espacos[0][1]:
            alocacao(espacos[0][0], tamanho, pid, memoria)
            #entra aqui
        else:
            #final
            ultimo = (len(memoria.tab_particao) - 1)
            inicio = memoria.tab_particao[ultimo][1] + memoria.tab_particao[ultimo][2]
            alocacao(inicio, tamanho, pid, memoria) #aloca no final


def alocacao(inicio: int, tamanho: int, pid: str, memoria: Memoria):  
    '''
    Função que aloca o processo na memória e atualiza a tabela de partição
    '''
    # 
    memoria.mem[inicio:inicio+tamanho] = [pid] * tamanho
    memoria.adicionar_particao(pid, inicio, tamanho)
    memoria.arquivo_saida.write(f"alocacao {pid} {inicio} {inicio+tamanho-1}" + '\n')

    


def verifica_espaco(memoria: Memoria):
    '''
    Função que gera uma lista com os espaços disponíveis para a alocação
    '''
    espacos = []
    tab_part = memoria.tab_particao
    tab_part.sort(key=lambda x: x.base) #ordenar pelos inicios para fazer as comparações
    if len(tab_part) > 0: #se tiver algo na tabela de particão
        if tab_part[0].base != 0: 
            espacos.append([0, tab_part[0].base])
        for i in range(1, len(memoria.tab_particao)):
            espaco = tab_part[i].base - (tab_part[i-1].base + tab_part[i-1].tamanho)
            if espaco != 0:
                espacos.append([(tab_part[i-1].base + tab_part[i-1].tamanho), espaco])
    termino = tab_part[len(tab_part) - 1].base + tab_part[len(tab_part) - 1].tamanho
    tamanho_final = memoria.tam - termino
    espacos.append([termino, tamanho_final])
    return espacos

def busca_libera(pid: str, memoria: Memoria):
    '''
    Função que busca o processo que será liberado do disco
    '''
    i = 0
    achou = False
    while i < len(memoria.tab_particao) and not achou:
        if pid == memoria.tab_particao[i].pid:
            achou = True
        else:
            i += 1
    if achou:
        libera(memoria, i)

def libera(memoria: Memoria, pos: int):
    '''
    Funcao que realiza a remoção de determinado processo do disco
    Ela passa um for que zera todas os índices que o processo ocupava
    '''
    tab_particao = memoria.tab_particao
    tab_part_rem = tab_particao.pop(pos)
    pid = tab_part_rem.pid
    base = tab_part_rem.base
    tam = tab_part_rem.base + tab_part_rem.tamanho
    
    memoria.mem[base:base+tam] = [0] * tam
    memoria.arquivo_saida.write(f"liberacao {pid} {base} {tam - 1}" + '\n')

def buddy(operacoes: list, memoria: Memoria):
    '''
    Função que organiza o método de alocação buddy, fazendo a chamada de função de cada
    uma das operações a serem realizadas: Acesso, Alocação e Liberação 
    '''
    for op in operacoes:
        if op[0] == 'aloca':
            buddy_aloca(op[1], int(op[2]), memoria)
        elif op[0] == 'acessa': 
            memoria.mmu.traduz(op[1], int(op[2]), memoria)
        elif op[0] == 'libera':
            buddy_libera(op[1], memoria)
        print(memoria.tab_particao)
    # muita coisa

def buddy_aloca(pid: str, tamanho: int, memoria: Memoria):
    '''
    Função que realiza a alocação de um buddy
    '''
    tamanho_particao = int(2 ** math.ceil(math.log2(tamanho)))

    posicao = -1
    menor = float('inf') 

    for i in range(len(memoria.tab_particao)):
        if memoria.tab_particao[i].pid == -1 and memoria.tab_particao[i].tamanho >= tamanho_particao:
            if memoria.tab_particao[i].tamanho < menor:
                menor = memoria.tab_particao[i].tamanho
                posicao = i

    if posicao == -1:
        print(f"Erro: Não há espaço em memória utilizando o sistema Buddy para o processo {pid}.")
        return

    while tamanho_particao < menor:
        menor = int(memoria.tab_particao[posicao].tamanho / 2)
        memoria.tab_particao[posicao] = processo(-1, memoria.tab_particao[posicao].base, menor)
        nova_base = memoria.tab_particao[posicao].base + menor
        memoria.tab_particao.insert(posicao + 1, processo(-1, nova_base, menor))

    memoria.tab_particao[posicao].pid = pid
    base = memoria.tab_particao[posicao].base
    memoria.mem[base:base+tamanho_particao] = [pid] * tamanho
    print(f'aloca {pid} {tamanho}')
    print(memoria.tab_particao)


def buddy_busca_pid(pid, tab_particao):
    for i in range(len(tab_particao)):
        if tab_particao[i].pid == pid:
            return i
    return -1


def buddy_libera(pid, memoria):
    posicao = buddy_busca_pid(pid, memoria.tab_particao)
    if posicao == -1:
        print("erro")
    else:
        base = memoria.tab_particao[posicao].base
        tamanho = memoria.tab_particao[posicao].tamanho

        memoria.tab_particao[posicao].pid = -1
        
        memoria.mem[base:base+tamanho] = [0] * tamanho
        memoria.arquivo_saida.write(f"liberacao {pid} {base} {tamanho - 1}" + '\n') 
        junta_buddy(posicao, memoria)
        
        
def junta_buddy(posicao, memoria):
    base = memoria.tab_particao[posicao].base
    tamanho = memoria.tab_particao[posicao].tamanho
    posicao_amigo = (base // tamanho) % 2
    print(memoria.tab_particao)
    if posicao_amigo == 1:
        if memoria.tab_particao[posicao-1].pid == -1 and memoria.tab_particao[posicao-1].tamanho == tamanho:
            memoria.tab_particao[posicao-1].tamanho = tamanho * 2
            memoria.tab_particao.pop(posicao) 
            junta_buddy(posicao-1, memoria)  
    elif posicao_amigo == 0 and posicao + 1 < len(memoria.tab_particao):
        if memoria.tab_particao[posicao+1].pid == -1 and memoria.tab_particao[posicao+1].tamanho == tamanho: 
            memoria.tab_particao[posicao].tamanho = tamanho * 2
            memoria.tab_particao.pop(posicao+1)
            junta_buddy(posicao, memoria)

def main():    
    caminho_entrada = sys.argv[1]
    estrategia = sys.argv[2]
    caminho_saida = "saida.txt"

    arq = ler_arquivo(caminho_entrada)
    qtd_processos = arq[0]
    pids = arq [1]
    operacoes = arq [2:]
    
    with open(caminho_saida, "a") as arquivo:
        memoria = Memoria(4096, arquivo)

        if estrategia == 'first':
            first(operacoes, memoria)
        elif estrategia == 'worst':
            worst(operacoes, memoria)
            #print(memoria.mem[:1000])
        elif estrategia == 'best':
            best(operacoes, memoria)
            #print(memoria.mem[:1000])
        elif estrategia == 'buddy':
            buddy(operacoes, memoria)
            print(memoria.mem)
            #print(memoria.mem[:1000])
            pass
        else:
            print('Erro')

if __name__ == '__main__':
    main()
