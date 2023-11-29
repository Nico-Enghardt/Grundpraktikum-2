import numpy as np
from plot import *
from lineare_regression import *

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

messwerte_bandpass = import_file("Bandpass.xlsx")
messwerte_hochpass = import_file("Hochpass.xlsx")
messwerte_tiefpass = import_file("Tiefpass.xlsx")

# Drop first value of hochpass

messwerte_hochpass = messwerte_hochpass[1:]

(bandX, DbandX), (bandY, DbandY) = use_log_scale(*load_messwerte(messwerte_bandpass), xBasis = 2, yBasis = 10)
(hochX, DhochX), (hochY, DhochY) = use_log_scale(*load_messwerte(messwerte_hochpass), xBasis = 2, yBasis = 10)
(tiefX, DtiefX), (tiefY, DtiefY) = use_log_scale(*load_messwerte(messwerte_tiefpass), xBasis = 2, yBasis = 10)

(bandX, DbandX), (bandY, DbandY) = (bandX, DbandX), (20*bandY, 20*DbandY)
(hochX, DhochX), (hochY, DhochY) = (hochX, DhochX), (20*hochY, 20*DhochY)
(tiefX, DtiefX), (tiefY, DtiefY) = (tiefX, DtiefX), (20*tiefY, 20*DtiefY)

#lineare Regression durchführen
auswahl=np.empty_like(hochX,dtype=bool,subok=False) #erstelle Array mit selber Länge wie Messreihe voller "true" werte
for i in range(len(auswahl)):
    auswahl[i]=True
#setzte indizes auf false, die ignoriert werden sollen
for i in range(5):
    auswahl[len(hochX)-i-1]=False

(aHoch,daHoch), (bHoch,dbHoch), R2Hoch, s2Hoch = regression(hochX[auswahl],hochY[auswahl],DhochY[auswahl])
xkoords=np.linspace(hochX[auswahl][0],hochX[auswahl][-1],100)
plt.plot(xkoords,aHoch+bHoch*xkoords,color="red")
plt.plot(xkoords,aHoch+daHoch+(bHoch-dbHoch)*xkoords,color="orange")
plt.plot(xkoords,aHoch-daHoch+(bHoch+dbHoch)*xkoords,color="orange") 

auswahl=np.empty_like(tiefX,dtype=bool,subok=False) #erstelle Array mit selber Länge wie Messreihe voller "true" werte
for i in range(len(auswahl)):
    auswahl[i]=True
#setzte indizes auf false, die ignoriert werden sollen
for i in range(8):
    auswahl[i]=False
(aTief,daTief), (bTief,dbTief), R2Tief, s2Tief = regression(tiefX[auswahl],tiefY[auswahl],DtiefY[auswahl])

xkoords=np.linspace(tiefX[auswahl][0],tiefX[auswahl][-1],100)
plt.plot(xkoords,aTief+bTief*xkoords,color="green")
plt.plot(xkoords,aTief+daTief+(bTief-dbTief)*xkoords,color="lime")
plt.plot(xkoords,aTief-daTief+(bTief+dbTief)*xkoords,color="lime")

xkoords=np.linspace(bandX[0],bandX[-1],100)
plt.plot(xkoords,-10*np.log(2)/(np.log(10))+0*xkoords,color="grey",label="Eckfrequenz")

diagramm((bandX, DbandX), (bandY, DbandY), legende="Bandpass (RLC)",xlabel="log_2(Frequenz)", ylabel="ln(U_R / U_0)", color="blue")
diagramm((hochX, DhochX), (hochY, DhochY), legende="Hochpass (RC)",xlabel="log_2(Frequenz)", ylabel="ln(U_R / U_0)", color="red")
diagramm((tiefX, DtiefX), (tiefY, DtiefY), legende="Tiefpass (RL)",xlabel="log_2(Frequenz)", ylabel="ln(U_R / U_0)", color="green")

#plt.suptitle("Normierte Strom-Spannungs-Kennlinien",fontsize=22)
plt.title("Frequenzgänge",fontsize=18)

plt.show()

save_table("bandpass.tex",(messwerte_bandpass[:,1],messwerte_bandpass[:,3]), (messwerte_bandpass[:,2],messwerte_bandpass[:,4]),*load_messwerte(messwerte_bandpass), (bandX, DbandX), (bandY, DbandY))
save_table("hochpass.tex",(messwerte_hochpass[:,1],messwerte_hochpass[:,3]), (messwerte_hochpass[:,2],messwerte_hochpass[:,4]),*load_messwerte(messwerte_hochpass), (hochX, DhochX), (hochY, DhochY))
save_table("tiefpass.tex",(messwerte_tiefpass[:,1],messwerte_tiefpass[:,3]), (messwerte_tiefpass[:,2],messwerte_tiefpass[:,4]),*load_messwerte(messwerte_tiefpass), (tiefX, DtiefX), (tiefY, DtiefY))