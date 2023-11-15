import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)

def diagramm(x_series, y_series, x_errors=None, y_errors=None, description=None,color="black",):
    
    xaxis = plt.gca().xaxis
    yaxis = plt.gca().yaxis

    #xaxis.set_major_locator(MultipleLocator(.2))
    ##xaxis.set_major_formatter('{:.1f}')
    #
    #xaxis.set_minor_locator(MultipleLocator(.02))
    #
    #yaxis.set_major_locator(MultipleLocator(10))
    ##yaxis.set_major_formatter('{:.0f}')
    #yaxis.set_minor_locator(MultipleLocator(1))

    # Add axis labels
    
    plt.xlabel("Spannungsteilerskale")
    plt.ylabel("U/U_0")
    

    plt.errorbar(x_series,y_series,xerr=x_errors,yerr=y_errors,color="black",linewidth=0,elinewidth=0.5,capsize=0.4,capthick=0.4)
    plt.scatter(x_series,y_series,marker="x",color=color)
    plt.grid(visible=True, which="major", linewidth=.5)
    plt.grid(visible=True, which="minor", linewidth=.3)
    
    #plt.xlim(-0.1,1.3)
    #plt.ylim(-0.1,1.3)