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
            libera(op[1], memoria)


def busca_first(tamanho: int, memoria: Memoria):
    for i in range(len(memoria.tab_particao)):  
        if memoria.tab_particao[i].pid == -1 and memoria.tab_particao[i].tamanho >= tamanho:
            return i
    return -1

def first_aloca(pid: str, tamanho: int, memoria: Memoria):
    '''
    Função que realiza a alocação da estratégia first fit
    Considera os seguintes casos
    1. Fazer a alocação no início da memória
    2. Fazer a alocação no meio da memória
    3. Fazer a alocação no final da memória

    [-1, 0, 256], [p01, 256, ...]
    '''
    if len(memoria.tab_particao) == 1:
        if memoria.tab_particao[0].pid == -1 and tamanho <= memoria.tam:
            alocacao(0, tamanho, pid, memoria) # aloca no comeco
        else:
            print("erro")
    else:
        posicao = busca_first(tamanho, memoria)
        if posicao == -1:
            print("erro")
        else:
            alocacao(posicao, tamanho, pid, memoria) #aloca no espaco que achou

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


def worst_aloca(pid: str, tamanho: int, memoria: Memoria):
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
        maior_pos = -1
        maior_tam = -1
        for i in range(len(memoria.tab_particao)):
            if memoria.tab_particao[i].pid == -1 and memoria.tab_particao[i].tamanho >= tamanho:
                if memoria.tab_particao[i].tamanho > maior_tam:
                    maior_pos = i
                    maior_tam = memoria.tab_particao[i].tamanho
        if maior_pos != -1:
            alocacao(maior_pos, tamanho, pid, memoria) #aloca no maior espaço
        else:
            print("erro")

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

def best_aloca(pid: str, tamanho: int, memoria: Memoria):
    '''
    Função que realiza a alocação da estratégia first fit
    Considera os seguintes casos
    1. Fazer a alocação no início da memória
    2. Fazer a alocação no meio da memória
    3. Fazer a alocação no final da memória

    [-1, 0, 256], [p01, 256, ...]
    '''
    if len(memoria.tab_particao) == 1:
        if memoria.tab_particao[0].pid == -1 and tamanho <= memoria.tam:
            alocacao(0, tamanho, pid, memoria) # aloca no comeco
        else:
            print("erro")
    else:
        menor_pos = float("inf")
        menor_tam = float("inf")
        for i in range(len(memoria.tab_particao)):
            if memoria.tab_particao[i].pid == -1 and memoria.tab_particao[i].tamanho >= tamanho:
                if memoria.tab_particao[i].tamanho > menor_tam:
                    menor_pos = i
                    menor_tam = memoria.tab_particao[i].tamanho
        if menor_pos != -1:
            alocacao(menor_pos, tamanho, pid, memoria) #aloca no menor espaço
        else:
            print("erro")

def alocacao(posicao: int, tamanho: int, pid: str, memoria: Memoria):  
    '''
    Função que aloca o processo na memória e atualiza a tabela de partição
    '''
    base = memoria.tab_particao[posicao].base  
    
    if tamanho < memoria.tab_particao[posicao].tamanho:
        restante = memoria.tab_particao[posicao].tamanho - tamanho
        memoria.tab_particao.insert(posicao+1, processo(-1, base + tamanho, restante))
    memoria.mem[base:base+tamanho] = [pid] * tamanho
    memoria.tab_particao[posicao] = processo(pid, base, tamanho)
    memoria.arquivo_saida.write(f"alocacao {pid} {base} {base+tamanho-1}" + '\n')

    print(memoria.tab_particao)

def busca_libera(pid: str, memoria: Memoria):
    '''
    Função que busca o processo que será liberado do disco
    '''
    for i in range(len(memoria.tab_particao)):
        if memoria.tab_particao[i].pid == pid:
            return i
    return -1


def libera(pid: int, memoria: Memoria):
    '''
    Funcao que realiza a remoção de determinado processo do disco
    Ela passa um for que zera todas os índices que o processo ocupava
    '''

    posicao = busca_libera(pid, memoria)
    if posicao != -1:
        base = memoria.tab_particao[posicao].base
        tamanho = memoria.tab_particao[posicao].tamanho
        pid = memoria.tab_particao[posicao].pid

        memoria.mem[base:base+tamanho] = [0] * tamanho
        memoria.arquivo_saida.write(f"liberacao {pid} {base} {tamanho - 1}" + '\n')
        memoria.tab_particao[posicao].pid = -1

        antecessor = posicao -1

        if 0 <= antecessor and memoria.tab_particao[antecessor].pid == -1:
            novo_tamanho = memoria.tab_particao[antecessor].tamanho + tamanho
            memoria.tab_particao[antecessor].tamanho = novo_tamanho
            del memoria.tab_particao[posicao]
            
            if memoria.tab_particao[posicao].pid == -1:
                novo_tamanho = memoria.tab_particao[antecessor].tamanho + memoria.tab_particao[posicao].tamanho
                memoria.tab_particao[antecessor].tamanho = novo_tamanho
                del memoria.tab_particao[posicao]
        elif posicao + 1 < len(memoria.tab_particao) and memoria.tab_particao[posicao + 1].pid == -1:
            novo_tamanho = memoria.tab_particao[posicao + 1].tamanho + memoria.tab_particao[posicao].tamanho
            memoria.tab_particao[posicao].tamanho = novo_tamanho
            del memoria.tab_particao[posicao+1]
        print(memoria.tab_particao)
    else:
        print("erro")

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
    '''
    Função recursiva que realiza a junção de buddys após a liberação]
    Se o resto da divisão (base/tamanho) resultar em 1, o buddy junta com o anterior a ele
    Se não, junta com o seguinte
    '''
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
    caminho_saida = f"log_{caminho_entrada}_{estrategia}"

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
            print(memoria.mem)
            pass
        else:
            print('Erro')

if __name__ == '__main__':
    main()
