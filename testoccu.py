import numpy as np
motd = "mains"
mots = "maiss"
couleurId = ["red", "yellow", "blue"]
egalite = np.array(list(mots)) ==  np.array(list(motd))
couleur = [i for i in range(len(motd))]
posFaux = []
devin = []
for i in range(len(egalite)):
    if egalite[i] == True:
        couleur[i] = 0 #red = 1
    else:
        posFaux = posFaux + [i]
        devin = devin + [motd[i]]
for j in posFaux:
    if mots[j] in devin:
        couleur[j] = 1 # yellow = 2
        iter = 0
        while mots[j] != devin[iter]:
            iter=iter+1
        del devin[iter]
    else:
        couleur[j] = 2# blue =3

for k in range(len(mots)):
    couleurId[couleur[k]]
