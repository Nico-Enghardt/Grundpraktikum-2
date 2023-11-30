import numpy as np
from plot import *

    
def load_messwerte(messwerte):
    
    angle = messwerte[:,0]
    defrac_angle = messwerte[:,1]
    lamb = messwerte[:,2]
    
    d_defrac_angle = np.ones(defrac_angle.shape)*0.1
    d_lamb = np.zeros(defrac_angle.shape)

    return (defrac_angle,d_defrac_angle), (lamb,d_lamb), (angle,d_defrac_angle)

messwerte_mercury = import_file("10 - OPS\Quecksilber-Kalibrierungskurve.csv")
defrac_angle, lamb, angle = load_messwerte(messwerte_mercury)

save_table("calibration_curve.txt", angle, defrac_angle,lamb[0])

unknown_lamp_angles = np.array([133.89,
                                          133.79,
                                          133.15,
                                          132.21,
                                          132.80, # vermutlich ein Ablesefehler
                                          131.74,
                                          131.26])


defraction_angles = 182.01 -  unknown_lamp_angles
d_angles = np.ones(defraction_angles.shape)*0.1

save_table("unknown_lamp_angles.txt", (unknown_lamp_angles,d_angles), (defraction_angles,d_angles))

helium_wavelengths = [447.1, 471.1, 492.2, 501.6, 587.6]

# Drop first value of hochpass

diagramm(defrac_angle, lamb, legende="calibration curve (mercury)",xlabel="defraction angle in °", ylabel="wavelenght in nm",color="black")

for angle in defraction_angles:
    
    plt.axvline(x=angle, color="orange",label="angles of unknown lamp")

for wavlength in helium_wavelengths:
    
    plt.axhline(y=wavlength, color="red",linewidth=0.5)

plt.show()

