# Simulador de Gestão de Memória - Sistemas Operacionais

Trabalho prático desenvolvido para a disciplina 12035 - Sistemas Operacionais (DIN/UEM) .
Professor: Dr. Alisson Renan Svaigen 

## Autores

* João Vitor Bidoia Angelo - RA: 139617
* Letícia Akemi Nakahati Vieira - RA: 140535

## Requisitos e Versões

* Linguagem de Programação: Python 3.10

## Como Executar

O sistema deve ser executado via terminal passando a estratégia de alocação como primeiro argumento e o caminho do arquivo de entrada como segundo argumento :

```bash
python Trabalho_SO.py <estrategia> <caminho_arquivo_entrada>
```

As opções válidas para a estratégia são: `first`, `best`, `worst` ou `buddy` .

### Exemplos de uso:

```bash
python Trabalho_SO.py buddy ./entradas/entrada01.txt
python Trabalho_SO.py first ./entradas/entrada01.txt
```

## Arquivos de Saída

A execução gera um arquivo de log na raiz do projeto com o seguinte padrão de nomenclatura :
`log_[arquivo_de_entrada]_[estrategia].txt`