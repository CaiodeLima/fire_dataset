from math import atan2, degrees, dist
import pandas as pd
import os

# Função para conseguir a angulação do Ponto 1 ao ponto 2 (escala 0 a 360 graus)
def get_angle(point_1, point_2):
    angle = atan2(point_2[1] - point_1[1], point_2[0] - point_1[0])
    angle = degrees(angle)
    angle = (angle + 360) % 360
    return angle

if __name__ == '__main__':
    # Criação das variáveis auxiliares
    auxDay = 0
    
    # Criação da lista dos 4 quadrantes possíveis
    quadrant1 = []
    quadrant2 = []
    quadrant3 = []
    quadrant4 = []

    # Criação da lista que contas pontos próximos
    proximos1km = []
    proximos3km = []
    
    # Leitura do CSV
    path = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles2/Datasets/classic/predicao.csv'
    df = pd.read_csv(path, sep=';')

    # Transforma as variáveis que utilizamos de Dataframe para lista, visto que é muito mais rápido
    originHora = df['hora'].to_list()
    dia = df['dia'].to_list()
    mes = df['mes'].to_list()
    ano = df['ano'].to_list()
    originLatitude = df['latitude'].to_list()
    originLongitude = df['longitude'].to_list()

    for i in range(len(originLongitude)):        
        # Ponto de origem a ser analizado
        originPoint = [originLatitude[i], originLongitude[i]]
        
        # O motivo dessas variáveis começarem em -1 é porque sempre haverá a checagem de um ponto consigo mesmo, nesta metodologia
        # e por isso, caso não hava pontos próximos
        q1 = -1
        p1km = -1
        p3km = -1

        # Já esses podem começar no 0 normalmente
        q2 = 0
        q3 = 0
        q4 = 0        

        # Checa se o dia passou, para otimizar, ou seja, só atualiza o dataframe temporário quando o dia é passado 
        if auxDay != dia[i]:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Dia atual:', dia[i], '/', mes[i], '/', ano[i])
            analysedDay = df.loc[(df['dia'] == dia[i]) & (df['mes'] == mes[i]) & (df['ano'] == ano[i])]
            auxDay = dia[i]
            
            # Transforma as variáveis que utilizamos de Dataframe para lista, visto que é muito mais rápido
            targetHora = analysedDay['hora'].to_list()
            targetLatitude = analysedDay['latitude'].to_list()
            targetlongitude = analysedDay['longitude'].to_list()

        # Contagem de focos próximos e quais quadrantes eles pertencem caso estejam dentro dos padrões exigidos
        for j in range(len(targetLatitude)):
            targetPoint = [targetLatitude[j], targetlongitude[j]]
            
            distance = dist(originPoint, targetPoint)
            angle = get_angle(originPoint, targetPoint)
            
            # Se a distância for de 1km ou menos e o foco for daquela hora ou horas antes
            if distance <= 0.00898311 and originHora[i] >= targetHora[j]:
                p1km += 1

            # Se a distância for de 3km ou mennos e o foco for daquela hora ou horas antes
            if distance <= 0.02694934 and originHora[i] >= targetHora[j]:
                p3km += 1

            # TUDO ISSO PARA UM RAIO DE 3KM E O FOCO FOR DAQUELA HORA OU HORAS ANTES:
            # Se o ângulo entre a origem e o alvo estiver entre 0 e 90 graus, temos um ponto proximo no Quadrante 1
            if 0 <= angle < 90 and distance <= 0.02694934 and originHora[i] >= targetHora[j]:
                q1 += 1
            
            # Se o ângulo entre a origem e o alvo estiver entre 90 e 180 graus, temos um ponto proximo no Quadrante 2
            elif 90 <= angle < 180 and distance <= 0.02694934 and originHora[i] >= targetHora[j]:
                q2 += 1
            
            # Se o ângulo entre a origem e o alvo estiver entre 180 e 270 graus, temos um ponto proximo no Quadrante 3
            elif 180 <= angle < 270 and distance <= 0.02694934 and originHora[i] >= targetHora[j]:
                q3 += 1
            
            # Se o ângulo entre a origem e o alvo estiver entre 270 e 360 graus, temos um ponto proximo no Quadrante 4
            elif 270 <= angle and distance <= 0.02694934 and originHora[i] >= targetHora[j]:
                q4 += 1
        
        quadrant1.append(q1)
        quadrant2.append(q2)
        quadrant3.append(q3)
        quadrant4.append(q4)
        proximos1km.append(p1km)
        proximos3km.append(p3km)

    # Passa os arrays para o dataframe e os salva
    df['Q1'] = quadrant1
    df['Q2'] = quadrant2
    df['Q3'] = quadrant3
    df['Q4'] = quadrant4
    df['p1km'] = proximos1km
    df['p3km'] = proximos3km

    df.to_csv(path, sep = ';', index = False)