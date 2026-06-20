# Trabalho-SO

4 estratégias de alocamento
- First - Fit
- Best - Fit
- Worst - Fit
- Buddy

Memória principal
    Vai tá lá
Lista de processos
    Arquivo que a gente recebe
Unidade de Gerenciamento de Memória - MMU
    checagem de segurança
        Segmentation fault
    calculo da tradução
        Endereço fisico -> Endereço logico + o endereço base
    Ela busca o dado e entrega pro processador
Tabela de partição
    Delimitar um limite pra onde começam as alterações
    Base e o fim do arquivo
    Endereço Base e Endereço limite do processo

Aloca: coloca pn com tamanho (x) na memória
Libera: Remove pn com tamanho (x) na memória
Acessa: pn 

Arquivo de entrada:
4 - Quant de processos
p01;p02;p03;p04 - PID dos processos
aloca p01 1000 
aloca p02 1000  
aloca p03 1000
libera p02
aloca p04 500
acessa p04 0

Arquivo de Saída

alocacao p01 0 999
alocacao p02 1000 1999
alocacao p03 2000 2999
liberacao p02 1000 1999
alocacao p04 1000 1499
acesso p04 0 1000

Fluxo de operação
Leitura do arquivo de entrada
Inicialização da memória RAM, dos processos e da tabela de partição
Tratamento de requisições
Encerramento da simulação
