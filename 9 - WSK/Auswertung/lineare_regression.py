import numpy as np
import matplotlib.pyplot as plt
from Rundung import *

def support(xwerte,ywerte,yfehler):              #Funktionsdefinition
    """Berechnet die Summen über x, x^2, y, xy und 1, jeweils durch den Fehler^2."""
    
    x2=0                                         #Summe über (x^2)/(sigma^2)
    for i in range(len(xwerte)):                 #gehe über alle Werte
        x2 += (xwerte[i]**2) / (yfehler[i]**2)   #und addiere die einzelnen Summenteile auf
    x=0                                          #Summe über (x)/(sigma^2)
    for i in range(len(xwerte)):
        x += xwerte[i] / (yfehler[i]**2)
    y=0                                          #Summe über (y)/(sigma^2)
    for i in range(len(ywerte)):
        y += ywerte[i] / (yfehler[i]**2)
    xy=0                                         #Summe über (x*y)/(sigma^2)
    for i in range(len(xwerte)):
        xy += (xwerte[i]*ywerte[i]) / (yfehler[i]**2)
    eins=0                                       #Summe über (1)/(sigma^2)
    for i in range(len(xwerte)):
        eins += 1 / (yfehler[i]**2)
        
    #return x,x2,y,xy,eins                        #gebe alle Werte zurück
    return x, x2, y, xy, eins #Ausgabe der Werte mit Rundung

def bestimmt(xwerte,ywerte,yfehler,a,b):
    yquer = support(xwerte,ywerte,yfehler)[2]/support(xwerte,ywerte,yfehler)[4]   #Berechnung von yquer
    zähler=0                                                                      #Zähler von R
    for i in range(len(ywerte)):                                                  #Summe über die
        zähler += ((ywerte[i]-a-b*xwerte[i])/(yfehler[i]))**2                     #Abweichungen von der Ausgleichsgeraden
    nenner=0                                                                      #Nenner von R
    for i in range(len(ywerte)):                                                  #Summe über die
        nenner += ((ywerte[i]-yquer)/(yfehler[i]))**2                             #Abweichungen vom Mittelwert yquer
    
    #return (1-zähler/nenner),zähler/(len(xwerte)-2)                               #R und (chi^2)/(n-2)
    return rundung((1-zähler/nenner)*100,zwischen=False), rundung(zähler/(len(xwerte)-2),zwischen=False)

def kern(xwerte,ywerte,yfehler):
    """Berechnet a, b, Delta a und Delta b."""
    
    (x,x2,y,xy,eins)=support(xwerte,ywerte,yfehler)  #erhält Hilfssummen aus support
    S = eins*x2-x**2                                 #Determinante der Koeffizientenmatrix S
    a=(x2*y-x*xy)/S                                  #y-Achsenabschnitt
    b=(eins*xy-x*y)/S                                #Steigung
    da=np.sqrt(x2/S)                                 #Fehler des y-Achsenabschnitts
    db=np.sqrt(eins/S)                               #Fehler der Steigung
    
    #return (a,da),(b,db)
    return (a,da), (b,db)

def regression(xwerte,ywerte,yfehler):
    (a,da),(b,db)=kern(xwerte,ywerte,yfehler)         #y-Achsenabschnitt, Steigung und ihre Fehler erhalten
    R2,s2=bestimmt(xwerte,ywerte,yfehler,a,b)     #Bestimmtheitsmaß und Varianz erhalten

    return (a,da), (b,db), R2, s2

"""
xkoords=np.linspace(xwerte[0],xwerte[-1],100) #x-Wertliste für das Diagramm
plt.plot(xkoords,a+b*xkoords,color="blue",label="Ausgleichsgerade")     #Ausgleichsgerade
plt.plot(xkoords,a+da+(b-db)*xkoords,color="red")                       #obere Grenzgerade
plt.plot(xkoords,a-da+(b+db)*xkoords,color="red",label="Grenzgeraden")
"""

"""
print("Der y-Achsenabschnitt beträgt",a,"\u00B1",da,".")
print("Die Geradensteigung beträgt",b,"\u00B1",db,".")
print("Das Bestimmtheitsmaß R^2 beträgt",R2,"%.")
print("Die Varianz beträgt",s2,".")
"""