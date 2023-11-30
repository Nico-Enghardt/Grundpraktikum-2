import numpy as np
from plot import *

    
def load_messwerte(messwerte):
    
    angle = messwerte[:,0]
    defrac_angle = 182.01 - angle
    lamb = messwerte[:,1]
    
    d_defrac_angle = np.ones(defrac_angle.shape)*0.1
    d_lamb = np.zeros(defrac_angle.shape)

    return (defrac_angle,d_defrac_angle), (lamb, d_lamb), (angle,d_defrac_angle)

messwerte_mercury = import_file("10 - OPS\Dispersionskurve.xlsx")
defrac_angle, lamb, angle = load_messwerte(messwerte_mercury)


defrac_angle_rad = defrac_angle[0] / 180 * np.pi, defrac_angle[1] / 180 * np.pi

dings = defrac_angle_rad[0]/ 2 + np.pi/6

n = np.sin(dings) / np.sin(np.pi/6) * 1.003
dn = 1/2 * np.cos(dings) / np.sin(np.pi/6)  * defrac_angle_rad[1] * 1.003

diagramm(lamb, (n,dn), legende="dispersion curve",xlabel="wavelength in nm", ylabel="refractive index")

plt.show()

save_table("dispersionskurve.tex",defrac_angle, angle, (n, dn), lamb[0])
