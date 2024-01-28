import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
from tabulate import tabulate 
from uncertainties import ufloat, unumpy
import sympy as sp
import math

def main():
    #left term und right term noch vertauscht
    table , units= read_from_csv('Brennweiten Testtabelle')
    #setup equations
    equations = []
    equations.append(equation('1/(1/(g)+1/b)','f', 'g', 'b', 'f'))
    equations[0].add_unit_right_term('g','mm')

    print(calculate_total_error(equations[0].term_left(), table,"g","b"))
    print_latex_error_calculation(equations[0],table,units,"g", "b") ##
    #funktionen berechnen
    #res = calculate_total_error(equations[0],table)
        
#scipyoptimised
runden_auf_n_stellen=4
class equation:
    def __init__(self, term_left = str, term_right = str, *symbols) -> None:
        self.term_right_ = term_right
        self.term_left_ = term_left
        self.symbols_ = symbols
        self.unit_right_term_ ={}
    # def get_symbols(self):
    #     symbols =[]
    #     for i in (term_left+term_right):
    #         if 
    def add_unit_right_term(self,symbol=str, unit_right_term=str):
        try:
            self.symbols_[symbol]
            self.unit_right_term_[symbol]=unit_right_term
            return True
        except:
            return None
        

    def term_right(self):
        return(self.term_right_)
    
    def term_left(self):
        return(self.term_left_)

    def symbols(self):
        return(self.symbols)  
    
    def unit_right_term (self, symbol=str):
        return(self.unit_right_term_[symbol])
    
    def unit_term(self):
        if(len(self.unit_right_term_) == 1):
            return(self.unit_right_term_.item()[1])
    
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


j = 0 # j für j verschiedene Messwerte
def print_latex_error_calculation(eq=equation, table = dict, units = dict,*var):
    global runden_auf_n_stellen
    #for loop over every entry of the table.
    for table_index in range(len(table[list(table.keys())[0]])):
        latex_deriv=''
        latex_deriv_with_numbers=''
        #for loop for every symbol that shou by 
        for var_ in  range(0,len(var)):
            latex_deriv += f'\\Delta {var[var_]}_\u007b{table_index}\u007d \cdot {sp.latex(sp.diff(eq.term_left(),var[var_]))}'#Ableitung ohne Wert, ok

            #Ableitung mit Zahlen            
            latex_deriv_with_numbers += f'+ {sp.latex( insert_numbers(sp.diff(eq.term_left(),var[var_]),table, table_index, runde_array(list(table.items())[table_index], runden_auf_n_stellen) ))} \cdot {units[var[var_]]}'

            #Das  was hier für eine Variable gemacht wird soll für alle gemacht werden. (das Folgende ist die alte Version)
            #latex_deriv_with_numbers += f'+ {sp.latex(((sp.diff(eq.term_left(),var[var_])).subs({var[var_]: runde((table[var[var_]][j]), runden_auf_n_stellen)})))} \cdot {units[var[var_]]}
            
            
            #Ableitung mit Zahlen, ok'''






        '''latex_error_calculation = f'\\begin\u007bequation\u007d \\Delta {eq.term_left()}_\u007b{j}\u007d = {latex_deriv}={latex_deriv_with_numbers} = {runde(calculate_total_error(eq.term_left, table, *var))} eq_term_right_unit\\end\u007bequation\u007d\\\\' '''

        #Müsste das nicht so?   {eq.term_right()}
        latex_error_calculation = f'\\begin\u007bequation\u007d \\label\u007b\u007d \\Delta {eq.term_right()}_\u007b{j}\u007d = {latex_deriv} ={latex_deriv_with_numbers}{eq.unit_term()} = {runde(calculate_total_error(eq.term_left(), table, *var)[j],runden_auf_n_stellen)} {eq.unit_term()}\\end\u007bequation\u007d\\\\' 
        '''latex_error_calculation = f'\\begin\u007bequation\u007d \\label\u007b\u007d \\Delta {eq.term_right()}_\u007b{j}\u007d = {latex_deriv} ={latex_deriv_with_numbers}{eq.unit_term()} = {runde(calculate_total_error(eq.term_left(), table {hier nur die Zeile j}, *var))} {eq.unit_right_term()}\\end\u007bequation\u007d\\\\' '''
        
        print(latex_error_calculation)
        j += 1
    return(latex_error_calculation)

def insert_numbers(term = str, table = {}, table_row = int,  *var):
    eq_with_numbers = sp.simplify(term)   #indez für verschiedene Messwerte
    for j in range(0,len(var)):   #Anzahl Zahlen
        eq_with_numbers=eq_with_numbers.subs({var[j]: table[var[j]][table_row]}) #Ersetzt alle variablem mit Wert j
        pass
    return(eq_with_numbers)

'''def calculate_value_and_unit():
    value=insert_numbers(eq.term_left(),table,j, *var)
    unit= eq.term_left()
    return(value, unit)'''


def calculate_total_error(term = str, table ={}, *var): #var_number durch schlüssel ersetzen
    eq_left_total_error=0
    for var_ in var:
        var_error=[]
        par_derivative = sp.diff(term, var_)
        for i in range(0,len(table[var_])):
            subtable = {key: value[i] for key, value in table.items()}
            var_error.append(par_derivative.subs(subtable)* table[var_ + '+'][i])
        #wird der Betrag verwendet?

        #var_error=calculate_error(term, var_, table[var_], table[var_ + "+"])  #nimmt nur den ersten return wert
        eq_left_total_error=np.add(eq_left_total_error, var_error)      #var_error Liste der Fehler der Variable zum Messwert j 
    return(eq_left_total_error)

def runde(zahl = float, runden_auf_n_stellen = int):
    # runde auf insgesammt n stellen
    if zahl == 0:
        return 0
    elif abs(zahl) < 1:
        potenz = 10 ** (runden_auf_n_stellen - len(str(int(abs(zahl)))))
        return round(zahl * potenz) / potenz
    else:
        return round(zahl, runden_auf_n_stellen - len(str(int(abs(zahl)))))
    
def runde_array(var = list[int], runden_auf_n_stellen = int):
    # runde auf insgesammt n stellen
    return_ = y[]
    for i in var:
        if i == 0:
            return_.append(0)
        elif abs(i) < 1:
            potenz = 10 ** (runden_auf_n_stellen - len(str(int(abs(i)))))
            return_.append(round(i * potenz) / potenz)
        else:
            return_.append(round(i, runden_auf_n_stellen - len(str(int(abs(i))))))
    return(return_)

if __name__ == "__main__":
    skript_verzeichnis = os.path.dirname(os.path.abspath(__file__)) #Aktuelles Skript-Verzeichnis als Arbeitsverzeichnis setzen
    os.chdir(skript_verzeichnis)    #print("Aktuelles Arbeitsverzeichnis:", os.getcwd()) #Aktuelles Arbeitsverzeichnis ausgeben, um sicherzustellen, dass es geändert wurde  
    main()