import numpy as np
from plot import *

from Rundung import rundung, PosErsSigZif
    
def load_messwerte(messwerte):
    
    f = messwerte[:,0]
    
    # Fehler der Frequenz: +- 1 in 3. signifikanter Stelle der Frequenz
    df = np.power(10.0,-2 - PosErsSigZif(messwerte[:,0]))
    
    U_0 = messwerte[:,1]
    U_R = messwerte[:,2]
    
    dU_0 = messwerte[:,3]
    dU_R = messwerte[:,4]
    
    U_R_pro_U_0 = np.divide(U_R,U_0)
    
    dU_R_pro_U_0 = U_R_pro_U_0 * np.sqrt(squared_rel_error(dU_0,U_0)+squared_rel_error(dU_R,U_R))

    return (f, df), (U_R_pro_U_0, dU_R_pro_U_0)

messwerte_bandpass = import_file("Auswertung/Bandpass.xlsx")
messwerte_hochpass = import_file("Auswertung/Hochpass.xlsx")
messwerte_tiefpass = import_file("Auswertung/Tiefpass.xlsx")

# Drop first value of hochpass

messwerte_hochpass = messwerte_hochpass[1:]

diagramm(*use_log_scale(*load_messwerte(messwerte_bandpass)), legende="Bandpass (R + L + C)",xlabel="log_2(Frequenz)", ylabel="ln(U_R / U_0)", color="blue")
diagramm(*use_log_scale(*load_messwerte(messwerte_hochpass)), legende="Hochpass (R + L)",xlabel="log_2(Frequenz)", ylabel="ln(U_R / U_0)", color="red")

diagramm(*use_log_scale(*load_messwerte(messwerte_tiefpass)), legende="Tiefpass (R + C)",xlabel="log_2(Frequenz)", ylabel="ln(U_R / U_0)", color="green")

plt.suptitle("Normierte Strom-Spannungs-Kennlinien",fontsize=22)
plt.title("Glühlampe (blau), Widerstand (orange), Graphitstab (rot)",fontsize=18)

plt.show()

def save_table(name,kwargs): 
  
  for ind in range(kwargs):
    
    print("f")


save_table("tabelle-bfandpass.tex",)