import numpy as np
from plot import *

    
def load_messwerte(messwerte):
    
    defrac_angle = messwerte[:,1]
    lamb = messwerte[:,2]
    
    d_defrac_angle = np.ones(defrac_angle.shape)*0.1
    d_lamb = np.zeros(defrac_angle.shape)

    return (defrac_angle,d_defrac_angle), (lamb,d_lamb)

messwerte_mercury = import_file("Quecksilber-Kalibrierungskurve.csv")
defrac_angle, lamb = load_messwerte(messwerte_mercury)


unknown_lamp_angles = 182.01 -  np.array([133.89,133.79,133.15,132.21,132.80,131.74,131.26])

helium_wavelengths = [447.1, 471.1, 492.2, 501.6, 587.6]

# Drop first value of hochpass

diagramm(defrac_angle,lamb, legende="calibration curve (mercury)",xlabel="defraction angle in °", ylabel="wavelenght in nm",color="black")

for angle in unknown_lamp_angles:
    
    plt.axvline(x=angle, color="orange",label="angles of unknown lamp")

for wavlength in helium_wavelengths:
    
    plt.axhline(y=wavlength, color="red",linewidth=0.5)

plt.show()