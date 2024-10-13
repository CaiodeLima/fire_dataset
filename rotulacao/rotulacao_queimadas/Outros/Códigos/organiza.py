import pandas as pd
import corrigeCSV

nomeArquivo = 'D:\CENSIPAM\Codigos\censipam_rotulacao\Outubro\Outubro.csv'

correcao1 = []                          #Variável criada para pegar os endereços das aspas sozinhas nas linhas

with open(nomeArquivo) as arquivo:       #Abre o arquivo como um arquivo de texto
    lines = arquivo.readlines()

for i in range(len(lines)):
    correcao = lines[i].replace(',', ";")
    correcao1.append(correcao)

print(correcao1[1])    

df = pd.DataFrame(correcao1, columns=list("A"))        #Salva as mudanças no .csv
df.to_csv(nomeArquivo, index = False, header = None)

corrigeCSV.correction(nomeArquivo)