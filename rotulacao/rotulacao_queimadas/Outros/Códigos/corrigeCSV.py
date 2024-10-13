import pandas as pd

def correction(NomeArquivo):
    AspasIndex = []                          #Variável criada para pegar os endereços das aspas sozinhas nas linhas
    ArraySemAspas = []                       #Array responsável para receber as linhas sem as aspas
    ArrayCorrigido = []                      #Último array, que não terá as quebras de linha

    with open(NomeArquivo) as arquivo:       #Abre o arquivo como um arquivo de texto
        lines = arquivo.readlines()

    for i in range(len(lines)):              #Captura o endereço de cada linha com aspas e quebra de linha
        if (lines[i] == '"\n') or (lines[i] == '""\n') or ((lines[i] == '"""\n')):
            AspasIndex.append(i)

    AspasIndex.sort(reverse = True)          #Coloca a lista em ordem decrescente

    for i in AspasIndex:                     #Remove as aspas em linhas sozinhas
        lines.pop(i)

    for i in range(len(lines)):              #Função para remover o resto das aspas na lista
        correcao = lines[i].replace('"', "")
        ArraySemAspas.append(correcao)

    for i in range(len(ArraySemAspas)):      #Remove as quebras de linha para formatar o array de forma correta
        correcao = ArraySemAspas[i].replace('\n', "")
        correcao = correcao.replace('"', "")
        ArrayCorrigido.append(correcao)

    df = pd.DataFrame(ArrayCorrigido, columns=list("A"))        #Salva as mudanças no .csv
    df.to_csv(NomeArquivo, index = False, header = None)   