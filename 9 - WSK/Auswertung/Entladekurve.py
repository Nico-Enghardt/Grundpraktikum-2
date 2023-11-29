import numpy as np
from plot import *
from lineare_regression import *
from Rundung import rundung, PosErsSigZif

def load_messwerte(messwerte):
    
    t = messwerte[:,0]
    dt = 0.1*np.ones_like(t)
    
    U = messwerte[:,1]
    dU = 0.1*np.ones_like(U)
    #normiere
    dU= dU/U[0]
    U = U/U[0]

    return (t, dt), (U, dU)

messwerte_entladung = import_file("Entladekurve.xlsx")

(x, dx), (y, dy) = use_log_scale(*load_messwerte(messwerte_entladung),xBasis=None,yBasis=np.exp(1))

#lineare regression
(a,da), (b,db), R2, s2 = regression(x,y,dy)

xkoords=np.linspace(x[0],x[-1],100)
plt.plot(xkoords,a+b*xkoords,color="Blue", label="Ausgleichsgerade")
plt.plot(xkoords,a+da+(b-db)*xkoords,color="CornflowerBlue", label="Grenzgerade")
plt.plot(xkoords,a-da+(b+db)*xkoords,color="CornflowerBlue")

diagramm((x, dx), (y, dy), legende="Entladekurve",xlabel="zeit", ylabel="ln(U/ U_max)", color="blue")

print("Der y-Achsenabschnitt beträgt",a,"\u00B1",da,".")
print("Die Geradensteigung beträgt",b,"\u00B1",db,".")
print("Das Bestimmtheitsmaß R^2 beträgt",R2,"%.")
print("Die Varianz beträgt",s2,".")

save_table("Entladekurve.tex",*load_messwerte(messwerte_entladung), (y, dy))

plt.show()