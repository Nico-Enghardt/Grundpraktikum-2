import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)

import openpyxl as pyxl
from pandas import DataFrame
from Rundung import rundung_str

def diagramm(x_series_errors, y_series_errors, legende=None, xlabel=None, ylabel=None, color="black",marker="x"):
    
    # Werte und Fehlerbalken
    
    x_series, x_errors = x_series_errors
    y_series, y_errors = y_series_errors
    
    plt.errorbar(x_series,y_series,xerr=x_errors,yerr=y_errors,color="black",linewidth=0,elinewidth=0.5,capsize=0.4,capthick=0.4)
    plt.scatter(x_series,y_series,marker=marker,label=legende,color=color)
    
    
    xaxis = plt.gca().xaxis
    yaxis = plt.gca().yaxis
    
    
    plt.grid(visible=True, which="major", linewidth=.6)
    plt.grid(visible=True, which="minor", linewidth=.3)

    # Achsenbeschriftungen
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # Diagrammbereich eintragen 
    
    # plt.xlim(-0.1,1.3)
    # plt.ylim(-0.1,1.3)
    
    # xaxis.set_major_locator(MultipleLocator(0.5))
    # #xaxis.set_major_formatter('{x:.f}')
    
    # xaxis.set_minor_locator(MultipleLocator(0.02))
    
    # yaxis.set_major_locator(MultipleLocator(50))
    # #xaxis.set_major_formatter('{x:.0f}')
    # yaxis.set_minor_locator(MultipleLocator(5))
    
    plt.legend()

def logarithmic_axis(values_errors_tuple, basis = 10):
  # Expect values_errors_tuple to contain (np.array, np.array) with same length
  
  values = values_errors_tuple[0]
  errors = values_errors_tuple[1]
  
  ln_values = np.log(values)/np.log(basis)
  
  ln_errors = None
  if errors is not None:
    ln_errors = np.divide(errors,values)/np.log(basis) # The effective errors of ln values are the relative errors of the values
  
  return ln_values, ln_errors
  
def use_log_scale(x_values_errors, y_values_errors, xBasis= None, yBasis= None):
  
  if xBasis != None:
    x_values_errors = logarithmic_axis(x_values_errors, basis = xBasis)
  if yBasis != None:
    y_values_errors = logarithmic_axis(y_values_errors, basis = yBasis)
    #y_values_errors = 20*y_values_errors[0], 20*y_values_errors[1]
  
  return x_values_errors, y_values_errors

def import_file(filename):
  
  if filename.endswith(".xlsx"):
    
    workbook = pyxl.load_workbook(filename, data_only=True)
    df = DataFrame(workbook.get_sheet_by_name('Sheet1').values)
    
    df.drop(index=df.index[0], axis=1,inplace=True)
    
    return np.array(df.to_numpy(),dtype="float64")
    
  if filename.endswith(".csv"):
    
    return np.loadtxt(filename,delimiter=";",skiprows=1)

def squared_rel_error(error, value):
  
      value_nonzero = np.where(value!=0, 1, 0)
        
      return np.square(np.divide(error,value+0.000000000001)*value_nonzero)
    
def save_table(name,*all_value_error_tupel): 
  
  table = ""
  
  num_variables = len(all_value_error_tupel)
  num_datapoints = len(all_value_error_tupel[0][0])
  
  for num_point in range(num_datapoints):
    row = ""
    
    for num_var in range(num_variables):
      
      if len(all_value_error_tupel[num_var]) == 2:
        # Probably fehler given to data
        value = all_value_error_tupel[num_var][0][num_point]
        error = all_value_error_tupel[num_var][1][num_point]
  
        row += f" {rundung_str(value,error)} &"
      else: 
        
        value = all_value_error_tupel[num_var][num_point]
        row += f" {value} &"
      
    table += row[:-1] + " \\\\ \n"  
    
  with open(name,"w") as file:
    
    file.write(table)