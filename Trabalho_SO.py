import sys
import math

class Memoria:
    def __init__(self , tam, arquivo_saida):
        '''
        Inicialização da memória, em que todas os objetos estão armazenados
        '''
        self.tam = tam
        self.mem = [0] * tam
        self.tab_particao = [Particao(-1, 0, tam)]
        self.mmu = MMU()
        self.arquivo_saida = arquivo_saida
        self.particao = Particao

class MMU:
        
    @staticmethod
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
                    memoria.arquivo_saida.write(f"acesso {pid} {end_virtual} violacao\n")
                    return None
                memoria.arquivo_saida.write(f"acesso {pid} {end_virtual} {base + end_virtual}\n")
                return None
        
class Particao:
    def __init__(self, pid: str, base: int, tamanho: int):
        '''
        Inicialização de um particao, que vai ser adicionado posteriormente na tabela de partição
        '''
        self.pid = pid
        self.base = base
        self.tamanho = tamanho

def ler_arquivo(caminho: str):
    '''
    Realiza a leitura do arquivo de entrada e retorna uma lista com as informações nele
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
            libera(op[1], memoria)

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
            libera(op[1], memoria)

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
            libera(op[1], memoria)
            
def busca_first(tamanho: int, memoria: Memoria):
    '''
    Busca o primeiro espaço disponível para alocação
    Se não tiver, retorna -1
    '''
    for i in range(len(memoria.tab_particao)):  
        if memoria.tab_particao[i].pid == -1 and memoria.tab_particao[i].tamanho >= tamanho:
            return i
    return -1

def first_aloca(pid: str, tamanho: int, memoria: Memoria):
    '''
    Realiza a alocação da estratégia first fit
    '''
    posicao = busca_first(tamanho, memoria)
    if posicao == -1:
        erro_aloca(pid, memoria)
    else:
        alocacao(posicao, tamanho, pid, memoria) #aloca no espaco que achou


def worst_aloca(pid: str, tamanho: int, memoria: Memoria):
    '''
    Realiza a alocação da estratégia worst fit
    '''
    maior_pos = -1
    maior_tam = -1
    for i in range(len(memoria.tab_particao)):
        if memoria.tab_particao[i].pid == -1 and memoria.tab_particao[i].tamanho >= tamanho:
            if memoria.tab_particao[i].tamanho > maior_tam:
                maior_pos = i
                maior_tam = memoria.tab_particao[i].tamanho
    if maior_pos != -1:
        alocacao(maior_pos, tamanho, pid, memoria)
    else:
        erro_aloca(pid, memoria)

def best_aloca(pid: str, tamanho: int, memoria: Memoria):
    '''
    Realiza a alocação da estratégia best fit
    '''
    menor_pos = float("inf")
    menor_tam = float("inf")
    for i in range(len(memoria.tab_particao)):
        if memoria.tab_particao[i].pid == -1 and memoria.tab_particao[i].tamanho >= tamanho:
            if memoria.tab_particao[i].tamanho < menor_tam:
                menor_pos = i
                menor_tam = memoria.tab_particao[i].tamanho
    if menor_pos != float("inf"):
        alocacao(menor_pos, tamanho, pid, memoria) #aloca no menor espaço
    else:
        erro_aloca(pid, memoria)

def alocacao(posicao: int, tamanho: int, pid: str, memoria: Memoria):  
    '''
    Aloca o particao na memória e atualiza a tabela de partição
    '''
    tab_part = memoria.tab_particao
    base = tab_part[posicao].base  
    
    if tamanho < tab_part[posicao].tamanho:
        restante = tab_part[posicao].tamanho - tamanho
        tab_part.insert(posicao+1, Particao(-1, base + tamanho, restante))
    memoria.mem[base:base+tamanho] = [pid] * tamanho
    tab_part[posicao] = Particao(pid, base, tamanho)
    memoria.arquivo_saida.write(f'alocacao {pid} {base} {base+tamanho-1}\n')

def erro_aloca(pid: str, memoria: Memoria):
    memoria.arquivo_saida.write(f'alocacao {pid} erro!\n')

def busca_libera(pid: str, memoria: Memoria):
    '''
    Busca o particao que será liberado do disco
    '''
    for i in range(len(memoria.tab_particao)):
        if memoria.tab_particao[i].pid == pid:
            return i
    return -1


def libera(pid: int, memoria: Memoria):
    '''
    Funcao que realiza a remoção de determinado particao do disco
    Ela passa um for que zera todas os índices que o particao ocupava
    '''

    posicao = busca_libera(pid, memoria)
    if posicao != -1:
        base = memoria.tab_particao[posicao].base
        tamanho = memoria.tab_particao[posicao].tamanho
        pid = memoria.tab_particao[posicao].pid

        memoria.mem[base:base+tamanho] = [0] * tamanho
        memoria.arquivo_saida.write(f'liberacao {pid} {base} {base + tamanho - 1}\n')
        memoria.tab_particao[posicao].pid = -1
        junta_particao(posicao, tamanho, memoria)
    else:
        memoria.arquivo_saida.write(f"{pid} não encontrado\n")

def junta_particao(posicao: int, tamanho: int, memoria: Memoria):
    '''
    Função que agrupa as partições que estão ao lado
    Verifica se o antecessor tem pid = -1. Se houver, junta o atual com o antecessor,
    e depois repete de forma análoga no sucessor
    '''
    antecessor = posicao -1
    sucessor = posicao + 1

    if 0 <= antecessor and memoria.tab_particao[antecessor].pid == -1:
        novo_tamanho = memoria.tab_particao[antecessor].tamanho + tamanho
        memoria.tab_particao[antecessor].tamanho = novo_tamanho
        del memoria.tab_particao[posicao]   
    if sucessor < len(memoria.tab_particao) and memoria.tab_particao[sucessor].pid == -1:
        novo_tamanho = memoria.tab_particao[sucessor].tamanho + memoria.tab_particao[posicao].tamanho
        memoria.tab_particao[posicao].tamanho = novo_tamanho
        del memoria.tab_particao[sucessor]


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

def busca_buddy_aloca(tamanho_particao: int, memoria: Memoria):
    '''
    Busca a posicao do menor espaço disponivel para realizar a alocação
    Se não houver, retorna -1
    '''
    posicao = -1
    menor = float('inf') 

    for i in range(len(memoria.tab_particao)):
        if memoria.tab_particao[i].pid == -1 and memoria.tab_particao[i].tamanho >= tamanho_particao:
            if memoria.tab_particao[i].tamanho < menor:
                menor = memoria.tab_particao[i].tamanho
                posicao = i
    return posicao, menor
    
def buddy_aloca(pid: str, tamanho: int, memoria: Memoria):   
    '''
    Realiza a alocação da estratégia buddy
    '''
    tamanho_particao = int(2 ** math.ceil(math.log2(tamanho)))
    posicao, menor = busca_buddy_aloca(tamanho_particao, memoria)

    if posicao != -1:
        base = memoria.tab_particao[posicao].base
        memoria.arquivo_saida.write(f'alocacao {pid} {base} {base + tamanho_particao - 1}\n')

        while tamanho_particao < menor:
            menor = int(memoria.tab_particao[posicao].tamanho / 2)
            memoria.tab_particao[posicao] = Particao(-1, base, menor)
            nova_base = base + menor
            memoria.tab_particao.insert(posicao + 1, Particao(-1, nova_base, menor))
        memoria.tab_particao[posicao].pid = pid
        memoria.mem[base:base+tamanho_particao] = [pid] * tamanho
    else:
        erro_aloca(pid, memoria)


def buddy_busca_pid(pid: str, tab_particao: list[Particao]):
    '''
    Busca a posição do pid na tabela partição,
    se não houver, retorna -1
    '''
    for i in range(len(tab_particao)):
        if tab_particao[i].pid == pid:
            return i
    return -1


def buddy_libera(pid: str, memoria: Memoria):
    '''
    Realiza a remoção de um buddy que foi liberado
    '''
    posicao = buddy_busca_pid(pid, memoria.tab_particao)
    if posicao == -1:
        memoria.arquivo_saida.write(f"{pid} não encontrado\n")
    else:
        base = memoria.tab_particao[posicao].base
        tamanho = memoria.tab_particao[posicao].tamanho

        memoria.tab_particao[posicao].pid = -1
        
        memoria.mem[base:base+tamanho] = [0] * tamanho
        memoria.arquivo_saida.write(f"liberacao {pid} {base} {base + tamanho - 1}" + '\n') 
        junta_buddy(posicao, memoria)
        
        
def junta_buddy(posicao: int, memoria: Memoria):
    '''
    Função recursiva que realiza a junção de buddys após a liberação
    Se o resto da divisão (base/tamanho) resultar em 1, o buddy junta com o anterior a ele
    Se não, junta com o seguinte
    '''
    base = memoria.tab_particao[posicao].base
    tamanho = memoria.tab_particao[posicao].tamanho
    posicao_amigo = (base // tamanho) % 2
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
    caminho_saida = f"log_{caminho_entrada[:len(caminho_entrada)-4]}_{estrategia}.txt"

    arq = ler_arquivo(caminho_entrada)
    operacoes = arq [2:]
    
    with open(caminho_saida, "a") as arquivo:
        memoria = Memoria(4096, arquivo)
 
        if estrategia == 'first':
             first(operacoes, memoria)
        elif estrategia == 'worst':
             worst(operacoes, memoria)
        elif estrategia == 'best':
             best(operacoes, memoria)
        elif estrategia == 'buddy':
             buddy(operacoes, memoria)
        else:
             print('Erro')
    
if __name__ == '__main__':
    main()
