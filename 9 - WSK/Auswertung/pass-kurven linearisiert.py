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

def calc_linearisierte_passkurve(f_value_error, UR_pro_U0_value_error, inverse_w=True):
  
  # transfrom (U/U0) as function of (f) --> [(U/U0)^-2 - 1] as function of (f^-2)

  UR_pro_U0, dU_pro_U_0 = UR_pro_U0_value_error 
  
  f, df  = f_value_error
  
  f_squared = np.square(f)
  if inverse_w:
    f_squared = np.divide(1,np.square(f))
  df = np.zeros(f.shape)
  
  UR_pro_U0_inverse_squared = np.divide(1,np.square(UR_pro_U0)) - (1+0.2/8)**2
  d_UR_pro_U0_inverse_squared = df
  
  return (f_squared, df) , (UR_pro_U0_inverse_squared, d_UR_pro_U0_inverse_squared)

#diagramm(*use_log_scale(*load_messwerte(messwerte_bandpass)), legende="Bandpass (R + L + C)",xlabel="log_2(Frequenz)", ylabel="ln(U_R / U_0)", color="blue")
#diagramm(*use_log_scale(*load_messwerte(messwerte_hochpass)), legende="Hochpass (R + L)",xlabel="log_2(Frequenz)", ylabel="ln(U_R / U_0)", color="red")
diagramm(*use_log_scale(*calc_linearisierte_passkurve(*load_messwerte(messwerte_hochpass))), legende="Hochpass (R + C)",xlabel="log_2(Frequenz)", ylabel="ln(U_R / U_0)", color="red")
#diagramm(*calc_linearisierte_passkurve(*load_messwerte(messwerte_hochpass)), legende="Hochpass (R + C)",xlabel="log_2(Frequenz)", ylabel="ln(U_R / U_0)", color="red")
#diagramm(*use_log_scale(*calc_linearisierte_passkurve(*load_messwerte(messwerte_tiefpass),inverse_w=False)), legende="Tiefpass (R + L)",xlabel="log_2(Frequenz)", ylabel="ln(U_R / U_0)", color="green")

def U_pro_U_0_of_w (f, Ri, R= 8, C = None, L = 4.7 * 0.001,):
  
  # w is the angle frequency 
  # L is Inductivity in Henry
  
  C = 3.3 *10**(-6)
  
  w = 2*np.pi*f
  
  if C:
    np.divide(R,np.sqrt((R+Ri+1)**2 + np.divide(1,np.square(w))*C**2)-Ri)
  
  return np.divide(R,np.sqrt((R+Ri+1)**2 + np.square(w)*(L**2))-Ri)

all_f = np.arange(0,20000,step=5)

for Ri in range(0,10):

  all_U_pro_U_0_of_w = U_pro_U_0_of_w(all_f,Ri = (1.4)**Ri)

  #diagramm(*use_log_scale(*calc_linearisierte_passkurve((all_f,None),(all_U_pro_U_0_of_w,None),inverse_w=False)), legende="Tiefpass (R + L)",xlabel="log_2(Frequenz)", ylabel="ln(U_R / U_0)", color="red",marker=".")
  
  #diagramm(*use_log_scale(*calc_linearisierte_passkurve((all_f,None),(all_U_pro_U_0_of_w,None),inverse_w=True)), legende="Tiefpass (R + L)",xlabel="log_2(Frequenz)", ylabel="ln(U_R / U_0)", color="red",marker=".")

plt.suptitle("Normierte Strom-Spannungs-Kennlinien",fontsize=22)
plt.title("Glühlampe (blau), Widerstand (orange), Graphitstab (rot)",fontsize=18)

plt.show()

def save_table(name,kwargs): 
  
  for ind in range(kwargs):
    
    print("f")


save_table("tabelle-bfandpass.tex",)