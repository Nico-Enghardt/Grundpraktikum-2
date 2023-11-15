import numpy as np
import plot

import os

print(os.listdir("."))

messwerte_lampe = np.loadtxt("1-Glühlampe.csv",delimiter=";",skiprows=1)
messwerte_graphit = np.loadtxt("1-Graphitstab.csv",delimiter=";",skiprows=1)
messwerte_widerstand = np.loadtxt("1-Widerstand.csv",delimiter=";",skiprows=1)

# Columns: Spannung U in V; Delta U; empty ;d=100mm;d=80 mm;d=60 mm; emtpy ;d=100mm;d=80 mm;d=60 mm
# U auf Y-Achse
# I^2 auf X-Achse

messwerte_lampe[:,1] *= 1000
#messwerte_lampe[:,3] *= 1000

fluke = lambda werte, digits: 2

def normierung(messwerte):
    
    U = messwerte[:,0]
    I = messwerte[:,1]   
    
    dU = messwerte[:,2]
    dI = messwerte[:,3]
    
    U_max, dU_max = np.max(U), dU[np.argmax(U)]
    I_max, dI_max = np.max(I), dI[np.argmax(I)]
    
    U_pro_Umax = U / np.max(U)
    I_pro_Imax = I / np.max(I)
    
    def squared_rel_error(error, value):
        
      return np.square(np.divide(error,value+0.0001))
    
    dU_pro_Umax = np.divide(U,U_max) * np.sqrt(squared_rel_error(dU,U)+squared_rel_error(dU_max,U_max))
    dI_pro_Imax = np.divide(I,I_max) * np.sqrt(squared_rel_error(dI,I)+squared_rel_error(dI_max,I_max))
    
    #print(dU_pro_Umax, np.divide(dU, U_max)) 
    
    #return I, U, dI, dU
    return I_pro_Imax, U_pro_Umax, dI_pro_Imax, dU_pro_Umax

plot.diagramm(*normierung(messwerte_lampe), description="d=100 mm",color="blue")
plot.diagramm(*normierung(messwerte_widerstand), description="d=80 mm",color="orange")
plot.diagramm(*normierung(messwerte_graphit), description="d=80 mm",color="red")

plot.plt.suptitle("Normierte Strom-Spannungs-Kennlinien",fontsize=22)
plot.plt.title("Glühlampe (blau), Widerstand (orange), Graphitstab (rot)",fontsize=18)

plot.plt.show()