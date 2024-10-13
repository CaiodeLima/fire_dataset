import numpy as np
import pandas as pd
import BurnCheck
import pathlib

month = 10

class Labels:
    def __init__(self):
        self._dataset = pd.read_csv('D:\\CENSIPAM\\Codigos\\censipam_rotulacao\\Outubro\\teste.csv', delimiter=";", decimal=",")
        self._columns_to_add = [ ('queimada', 'check_burn') ]
        self.adding_columns()
        self.adding_values()
        self.save_dataset()

    def adding_columns(self):
        pass
        # for key in self._columns_to_add:
        #     self._dataset[key[0]] = ""
        
    def adding_values(self):
        for function in self._columns_to_add:
            self._dataset[function[0]] = eval("self."+function[1])(self._dataset)        

    def check_burn(self, row):
        lat = row['latitude'].astype(float)
        long = row['longitude'].astype(float)
        print(type(long))
        #burned = BurnCheck.burned_check(long, lat, month)
        return 1

    def save_dataset(self):
        self._dataset.to_csv("./Outubro_Rotulado.csv")
        
Labels()