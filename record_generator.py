from pyunitreport import HTMLTestRunner
from selenium import webdriver
import re
import time
import threading
import pandas as pd


def get_name():
    """ Función para obtener nombres del meeting.
    Output
        list_of_names : list of string
            Lista de nombres 
    """
    names = driver.find_elements_by_xpath('//*[@class="participants-ul"]/li//span[@class="participants-item__display-name"]')
    list_of_names = [x.text for x in names]
    return list_of_names


def num_of_members():
    """ Retorna la cantidad total de participantes
    Output
        my_number : int
            El numero de participantes
    """
    my_number = driver.find_element_by_xpath('//*[@id="wc-container-right"]/div/div[1]/div[1]/div[2]/span')
    my_number  = str(my_number.text)
    my_number = re.search("[0-9]+", my_number)[0]
    my_number= int(my_number)
    return my_number

def add_data_dic(my_dic,number_of_members,list_of_names,now,bit):
    """ Agregar registros en la tabla de registro """
    my_dic["number_of_members"].append(number_of_members)
    my_dic["list_of_names"].append(list_of_names)
    my_dic["now"].append(now)
    my_dic["bit"].append(bit)

def register(seconds):
    """ Es la función que me permite obtener todos los datos de la llamada de zoom.

    Input
        seconds : int
            Representa cada cuantos segundos toma el registro
    Output
        df : pandas dataframe 
            Es la tabla donde se muestran todos los registros
            number_of_members : int
                Representa la cantidad de personas en un momento determinado
            list_of_names : int
                Lista de nombres de las personas conectadas en un momento determinado
            now : datetime
                Fecha y hora del registro
            bit : int
                0 Si no hay cambio
                1 Si al menos una persona se retiro
                2 Si al menos una persona entro
    """
    my_dic = {"number_of_members": [], "list_of_names": [], "now":[], "bit":[]}
    #df = pd.DataFrame(columns=["Numero conectados", "Lista de nombres", "now", "salio"])
    pivot=2
    list_of_names = get_names()
    while True:
        bit=0
        try:
            number= num_of_members()
            if number > pivot:
                print("Entro alguien")
                list_of_names = get_names()
                pivot = number
                bit=2
        
            elif number < pivot:
                print("Salio alguien")
                list_of_names = get_names() 
                pivot = number
                bit=1
            print(list_of_names)
            print(number)
            now= time.strftime("%I:%M:%S")
            add_data_dic(my_dic, number, list_of_names, now, bit)
            #df = guardar_pandas(df, number, list_of_names, now, salio)
            time.sleep(seconds)
        except:
            print("Error en ejecucion de agregar registro")
            df = pd.DataFrame(my_dic) 
            return df

if __name__ == "__main__":
    """ Empieza el programa a correr.
        Falta hacer: algo que agarre como argumento el link y los segundos """
    link_meeting=input("Inserta el link del meeting: ")
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(executable_path=r"./chromedriver.exe", options=options)
    driver.get(link_meeting)
    register(30)

""" def guardar_pandas(df, numero, lista, now, salio):
    df=df.append(pd.DataFrame([(numero,lista, now, salio)], columns=["Numero conectados", "Lista de nombres", "now","salio"]), ignore_index=True)
    return df """

