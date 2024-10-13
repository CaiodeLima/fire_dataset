from math import atan2, degrees

def get_angle(point_1, point_2): #These can also be four parameters instead of two arrays
    angle = atan2(point_2[1] - point_1[1], point_2[0] - point_1[0])
    angle = degrees(angle)
    angle = (angle + 360) % 360
    return round(angle)

ponto1 = [10,10]
ponto2 = [10,10]

print(get_angle(ponto1, ponto2))