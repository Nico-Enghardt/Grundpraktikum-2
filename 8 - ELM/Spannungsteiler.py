import numpy as np
import plot

import os

print(os.listdir("."))

messwerte_unbelastet = np.loadtxt("2-unbelastet.csv",delimiter=";",skiprows=1,max_rows=11)
messwerte_belastet = np.loadtxt("2-belastet.csv",delimiter=";",skiprows=1,max_rows=11)

# Columns: Spannung U in V; Delta U; empty ;d=100mm;d=80 mm;d=60 mm; emtpy ;d=100mm;d=80 mm;d=60 mm
# U auf Y-Achse
# I^2 auf X-Achse

def process_data(messwerte):

    U_pro_U_max = messwerte[:,3]
    dU_pro_U_max = messwerte[:,4]
    S = messwerte[:,1]
    dS = np.ones(messwerte.shape[0])*0.02

    return S, U_pro_U_max, dS, dU_pro_U_max

plot.diagramm(*process_data(messwerte_unbelastet),color="blue")
plot.diagramm(*process_data(messwerte_belastet),color="red")


S, U_pro_U_max_unbelastet, dS, dU_pro_U_max_unbelastet = process_data(messwerte_unbelastet)
S, U_pro_U_max_belastet, dS, dU_pro_U_max_belastet = process_data(messwerte_belastet)


print("s in 1 & $U/U_{max} (unbelastet) & $U/U_{max} (belastet mit 220 \Omega)")
for ind, s in enumerate(S):
    
    print(f"${s}\pm{0.02}$ & ${U_pro_U_max_unbelastet[ind]:.3f}\pm{dU_pro_U_max_unbelastet[ind]:.3f}$ & ${U_pro_U_max_belastet[ind]:.3f}\pm{dU_pro_U_max_belastet[ind]:.3f}$ \\\\")


space = np.arange(0,10,0.04)
R_0 = 48.7
R_L = 220 

def spannungsteiler_function(s, s_0, R_0, R_L):
    
    s_over_s_0 = s/s_0
    
    R_0_over_R_L = R_0/R_L
    
    
    return (s_over_s_0 / (1 + s_over_s_0*(1-s_over_s_0)*R_0_over_R_L))

theoriewerte_spannung = [spannungsteiler_function(s,10,R_0, R_L) for s in space]

plot.plt.plot(space,theoriewerte_spannung,linewidth=0.3,color="red")

theoriewerte_spannung = [s/10 for s in space]
plot.plt.plot(space,theoriewerte_spannung,linewidth=0.3,color="blue")
plot.plt.legend(["unbelastet","belastet"])
plot.plt.show()

S_list, U_pro_U_max, dS, dU_pro_U_max = process_data(messwerte_belastet)
theoriewerte_spannung = [spannungsteiler_function(s,10,R_0, R_L) for s in S_list]

varianz = np.sum(np.power(U_pro_U_max - np.array(theoriewerte_spannung),2))/len(S_list)
print("Varianz: ",varianz,"Standardabweichung: ", np.sqrt(varianz))


plot.diagramm(S_list,U_pro_U_max - theoriewerte_spannung)
plot.plt.ylabel("Differenz in U/U_0 zwischen Experiment und Theorie")


plot.plt.title("",fontsize=18)


plot.plt.show()