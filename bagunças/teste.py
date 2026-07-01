import math
particao = []
tamanho = 4096
espacos = [[-1, 0, 4096]]

tamanho_arquivo = 500
tamanho_particao = int(2 ** math.ceil(math.log2(tamanho_arquivo)))

i = 0 
while i < len(espacos) and espacos[i][0] != -1:#aqui eu acho o primeiro espaço disponivel
    i += 1
posicao = i
menor = espacos[i][2]

for i in range(i, len(espacos)): #aqui eu busco o menor espaço disponivel
    if espacos[i][0] != -1 and espacos[i][2] < menor and espacos[i][2] >= tamanho_particao: 
        menor = espacos[i][2]
        posicao = i

#esse while daria pra colocar dentro da class memoria com os parametros (tam_particao, menor, posicao)
while tamanho_particao < menor: #aqui ta fazendo a divisao do menor espaço ate achar um que seja do menor tamanho da particao necessaria
    menor = int((espacos[posicao][2])/2)
    espacos[posicao] = [-1, espacos[posicao][1], menor]
    espacos.insert(posicao+1, [-1, espacos[posicao][1] + espacos[posicao][2], menor])

espacos[posicao][0] = "p03" #aqui seria a alocacao
#tab_particao = [pid, base, tamanho]
print(espacos)

# Se o Endereço Atual / Tamanho do Bloco for par, o parceiro está na direita (teria que ver o +1)
# O parceiro esta na esquerda, caso contrário (teria que ver o -1)
# 0/512 -> direita
# 512/512 = 1 -> esquerda

#falta retornar erro sempre que o tamanho do arquivo passa o tamanho da memoria disponivel !!!!