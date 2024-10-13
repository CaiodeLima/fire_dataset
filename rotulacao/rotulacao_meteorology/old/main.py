# Para fins de comparação, eu utilizava o site:
# https://psl.noaa.gov/cgi-bin/DataAccess.pl?DB_dataset=NCEP+Reanalysis+Daily+Averages&DB_variable=Relative+humidity&DB_statistic=Mean&DB_tid=95779&DB_did=198&DB_vid=4983
# Os resultados não batiam + as casas decimais nas coordenadas não estão influenciamento no resultado :/
# Se conseguir rodar esse código, vai ser muito mais rápido que a API

import netCDF4 # No Anaconda, usar o comando: pip install netCDF4

HumFile = 'rhum.sig995.2020.nc'
OpenHumFile = netCDF4.Dataset(HumFile)
print(OpenHumFile)

print('--------------------------------------------------------------------------------------------------------------------------')
print('--------------------------------------------------------------------------------------------------------------------------')

print(OpenHumFile)
print('--------------------------------------------------------------------------------------------------------------------------')
print('--------------------------------------------------------------------------------------------------------------------------')
hum = OpenHumFile['rhum']
print(hum)
print('--------------------------------------------------------------------------------------------------------------------------')
print('--------------------------------------------------------------------------------------------------------------------------')
memata = hum[280, 15.728809192907828, -47.669845482528125] # Quase ctz que é dia, long e lat. Ao meu ver, o dia vai de 0 a 365
                                                            # já que ele não aceita valores maiores ou menores que esses

print (memata)