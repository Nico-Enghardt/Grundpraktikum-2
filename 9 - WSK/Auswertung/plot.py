import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)

import openpyxl as pyxl
from pandas import DataFrame

def diagramm(x_series_errors, y_series_errors, legende=None, xlabel=None, ylabel=None, color="black",marker="x"):
    
    # Werte und Fehlerbalken
    
    x_series, x_errors = x_series_errors
    y_series, y_errors = y_series_errors
    
    plt.errorbar(x_series,y_series,xerr=x_errors,yerr=y_errors,color="black",linewidth=0,elinewidth=0.5,capsize=0.4,capthick=0.4)
    plt.scatter(x_series,y_series,marker=marker,label=legende,color=color)
    
    
    xaxis = plt.gca().xaxis
    yaxis = plt.gca().yaxis
    
    
    plt.grid(visible=True, which="major", linewidth=.5)

    # Achsenbeschriftungen
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # Diagrammbereich eintragen 
    
    # plt.xlim(-0.1,1.3)
    # plt.ylim(-0.1,1.3)
    
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
  
def use_log_scale(x_values_errors, y_values_errors, x= True, y= True):
  
  if x:
    x_values_errors = logarithmic_axis(x_values_errors,basis=2)
  if y:
    y_values_errors = logarithmic_axis(y_values_errors)
  
  return x_values_errors, y_values_errors

def import_file(filename):
  
  if filename.endswith(".xlsx"):
    
    workbook = pyxl.load_workbook(filename, data_only=True)
    df = DataFrame(workbook.get_sheet_by_name('Tabelle1').values)
    
    df.drop(index=df.index[0], axis=1,inplace=True)
    
    return np.array(df.to_numpy(),dtype="float64")
    
  if filename.endswith(".csv"):
    
    return np.loadtxt(filename,delimiter=";",skiprows=1)

def squared_rel_error(error, value):
  
      value_nonzero = np.where(value!=0, 1, 0)
        
      return np.square(np.divide(error,value+0.000000000001)*value_nonzero)