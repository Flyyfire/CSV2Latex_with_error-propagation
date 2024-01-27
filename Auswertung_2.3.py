import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
from tabulate import tabulate 
from uncertainties import ufloat, unumpy
import sympy as sp
import math


formel_einheit



#scipyoptimised
runden_auf_n_stellen=4
class equation:
    def __init__(self, term_left = str, term_right = str, *symbols) -> None:
        self.term_right_ = term_right
        self.term_left_ = term_left
        self.symbols_ = symbols
    # def get_symbols(self):
    #     symbols =[]
    #     for i in (term_left+term_right):
    #         if 

    def term_right(self):
        return(self.term_right_)
    
    def term_left(self):
        return(self.term_left_)

    def symbols(self):
        return(self.symbols)    
    
partial_derivative=[[],[]]  # Gleichung, Variable
a_error_operator=[]

def read_from_csv(filename, delimiter = ";"):
    table = {}
    with open(filename+'.csv', mode='r') as file:    #Öffnen der CSV-Datei im lese-Modus
        reader = csv.reader(file, delimiter=delimiter)
        first_line = next(reader)
        second_line = next(reader)
        units={}
        reading_table = []
        for item in first_line:
            if item == '':
                item = "NC"
                reading_table.append("NC")
            else:
                table[item] = []
                reading_table.append(item)

        for i in range(0,len(first_line)):
            units[reading_table[i]] = second_line[i]

        for line in reader:
            for i in range(0, len(line)):
                if not reading_table[i] == "NC":
                    table[reading_table[i]].append(float(line[i]))
    return (table,units)

j = 0
def print_latex_error_calculation(eq=equation, table = {}, units = {},*var):
    global j
    for j in range(len(table[list(table.keys())[0]])):
        latex_deriv=''
        latex_deriv_with_numbers=''
        for var_ in  range(1,len(var)):
            latex_deriv += f'\\Delta {var[var_]}_\u007b{j}\u007d \cdot {sp.latex(sp.diff(eq.term_left(),var[var_]))}'#Ableitung ohne Wert, ok
            latex_deriv_with_numbers += f'+ {sp.latex((sp.diff(eq.term_left(),var[var_]).subs({var[var_]: table[var[var_]][j]})))}'#Ableitung mit Zahlen, ok

        latex_error_calculation = f'\\begin\u007bequation\u007d \\Delta {eq.term_left()}_\u007b{j}\u007d = {latex_deriv}={latex_deriv_with_numbers} = {runde(calculate_total_error(eq.term_left, table, *var))} formel_einheit\\end\u007bequation\u007d\\\\' 

        #Müsste das nicht so?   {eq.term_right()}
        latex_error_calculation = f'\\begin\u007bequation\u007d \\label\u007b\u007d \\Delta {eq.term_right()}_\u007b{j}\u007d = {latex_deriv} ={latex_deriv_with_numbers} = {runde(calculate_total_error(eq.term_left, table, *var))} {formel_einheit}\\end\u007bequation\u007d\\\\' 

        print(latex_error_calculation)
        j += 1
    return(latex_error_calculation)

def insert_numbers(term = str, table = {},table_row = int,  *var):
    eq_with_numbers = sp.simplify(term)   #indez für verschiedene Messwerte
    for j in range(0,len(var)):   #Anzahl Zahlen
        eq_with_numbers=eq_with_numbers.subs({var[j]: table[var[j]][table_row]}) #Ersetzt alle variablem mit Wert j
        pass
    return(eq_with_numbers)

def calculate_value_and_unit():
    value=insert_numbers(eq.term_left(),table,j, *var)
    unit= eq.term_left()
    return(value, unit)


def calculate_total_error(term = str, table ={}, *var): #var_number durch schlüssel ersetzen
    eq_left_total_error=0
    for var_ in var:
        var_error=[]
        par_derivative = sp.diff(term, var_)
        for i in range(0,len(table[var_])):
            subtable = {key: value[i] for key, value in table.items()}
            var_error.append(par_derivative.subs(subtable)* table[var_ + "+"][i])
        wird der Betrag verwendet?

        #var_error=calculate_error(term, var_, table[var_], table[var_ + "+"])  #nimmt nur den ersten return wert
        eq_left_total_error=np.add(eq_left_total_error, var_error)      #var_error Liste der Fehler der Variable zum Messwert j 
    return(eq_left_total_error)

def runde(zahl,runden_auf_n_stellen):
    # runde auf insgesammt 4 stellen
    if zahl == 0:
        return 0
    elif abs(zahl) < 1:
        potenz = 10 ** (runden_auf_n_stellen - len(str(int(abs(zahl)))))
        return round(zahl * potenz) / potenz
    else:
        return round(zahl, runden_auf_n_stellen - len(str(int(abs(zahl)))))

def main():
    table = read_from_csv('Brennweitenbestimmung mit der Linsenformel')[0]
    #setup equations
    equations = []
    equations.append(equation("1/(1/(g)+1/b)","z"))

    print(calculate_total_error(equations[0].term_left(),table,"g","b"))
    print_latex_error_calculation(equations[0],table,units,"g", "b") ##
    #funktionen berechnen
    #res = calculate_total_error(equations[0],table)

if __name__ == "__main__":
    skript_verzeichnis = os.path.dirname(os.path.abspath(__file__)) #Aktuelles Skript-Verzeichnis als Arbeitsverzeichnis setzen
    os.chdir(skript_verzeichnis)    #print("Aktuelles Arbeitsverzeichnis:", os.getcwd()) #Aktuelles Arbeitsverzeichnis ausgeben, um sicherzustellen, dass es geändert wurde  
    main()