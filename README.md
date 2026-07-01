# Simulador de Gestão de Memória - Sistemas Operacionais

* Trabalho prático desenvolvido para a disciplina 12035 - Sistemas Operacionais (DIN/UEM)
* Professor: Dr. Alisson Renan Svaigen 

## Autores

* João Vitor Bidoia Angelo - RA: 139617
* Letícia Akemi Nakahati Vieira - RA: 140535

## Requisitos e Versões

* Linguagem de Programação: Python 3.10

## Como Executar

O sistema deve ser executado via terminal passando o arquivo de entrada como primeiro argumento e a estratégia como segundo

```bash
python Trabalho_SO.py *arquivo_entrada* *estrategia* 
```

As opções válidas para a estratégia são: `first`, `best`, `worst` ou `buddy`

### Exemplos de uso:

```bash
python Trabalho_SO.py entrada001.txt buddy
python Trabalho_SO.py entrada002.txt first
```

## Arquivos de Saída

A execução gera o seguinte arquivo de log:
`log_[arquivo_de_entrada]_[estrategia].txt`
