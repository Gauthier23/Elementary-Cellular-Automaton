# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 10:31:33 2022

@author: Gauthier Guyaz, Lycée Blaise-Cendrars, 3H

Github : https://github.com/Gauthier23
"""

from tkinter import*

###---Fonction créant une ligne composée de carré sur l'axe X---###
def ligne():                
    x = 0
    while x < side:
        can.create_rectangle(x, y*c, x + c, y*c + c, outline = "black", fill="")  #fill = "" ==> transparent
        dico[x/c,y] = 0
        x += c
   
###---Fonction positionant la premier carré noir au centre de la première ligne---###
def etape1():
    x = round((side/2)/c)       #entier le plus proche
    can.create_rectangle(c*x, 0, c*x + c, c, outline = "black", fill="black")
    dico[x, 0] = 1 
 
    
###---Fonction remplissant les carrés noirs selon les indications de la liste temporaire---###
def draw():
    ligne()
    for x in range(0, int(side/c)):
            if temp[x,y] == 1: 
                can.create_rectangle(c*x, c*y, c*x + c, c*y + c, fill="black")
    dico.update(temp)
  
            
###---Fonction recensant l'état des 3 cellules limitrophes supérieures à la cellule concernée---###
def sup(x,y):
    list_sup = [] 
    
    #-cellule au dessus à gauche-#
    if dico.get((x-1, y-1), 0)== 1:     
        list_sup.append(1)
        
    if dico.get((x-1, y-1), 0)== 0:
        list_sup.append(0)
        
    #-cellule au dessus-#    
    if dico.get((x, y-1), 0)== 1:       
        list_sup.append(1)
    
    if dico.get((x, y-1), 0)== 0:
        list_sup.append(0)
        
    #-cellule au dessus à droite-#    
    if dico.get((x+1, y-1), 0)== 1:     
        list_sup.append(1)
        
    if dico.get((x+1, y-1), 0)== 0:
        list_sup.append(0)
        
    return list_sup                     #on retourne la liste contenant les trois états   


###---Fonction qui créer le nouveau dictionnaire pour la création d'une nouvelle génération---###
def calculer():
    global temp, y
    y = y + 1                           #on passe à la rangé en dessous
    for x in range(0, int(side/c)):     #on passe sur toutes les cases avec la coordonnée x (axe x) 
        list_sup = sup(x,y)             #on appelle la fonction listant l'état des voisins supérieurs
            
        if list_sup == [1,1,1]:         #cas : noir, noir, noir
            temp[x,y] = lst[0]          #on attribue à notre dictionnaire temporaire l'état qui correspond à l'élément en position 0 de notre liste
            
        if list_sup == [1,1,0]:         #cas : noir, noir, blanc
            temp[x,y] = lst[1]          #idem, élément positon 1
            
        if list_sup == [1,0,1]:         #cas : noir, blanc, noir
            temp[x,y] = lst[2]          #idem, élément position 2
                
        if list_sup == [1,0,0]:         #cas : noir, blanc, blanc
            temp[x,y] = lst[3]          #idem, élément position 3
            
        if list_sup == [0,1,1]:         #cas : blanc, noir, noir
            temp[x,y] = lst[4]          #idem, élément position 4

        if list_sup == [0,1,0]:         #cas : blanc, noir, blanc
            temp[x,y] = lst[5]          #idem, élément position 5
            
        if list_sup == [0,0,1]:         #cas : blanc, blanc, noir
            temp[x,y] = lst[6]          #idem, élément position 6
                
        if list_sup == [0,0,0]:         #cas : blanc, blanc, blanc
            temp[x,y] = lst[7]          #idem, élément position 7
                
    draw()                              #dessin de la nouvelle colonne

###---Fonction gérant la répétition des générations selon le temps---###
def withtime():
    global flag
    flag = 1
    update_calculs()
        
def update_calculs():
    global flag
    calculer()
    if flag == 1:
            fen.after(100, update_calculs)
        
def stop():
    global flag
    flag = 0

     
#####-----Variables et Constantes-----#####

y = 0
c = 10                          #nombre de pixel pour le côté d'une cellule            
side = 1000                     #taille du côté du canvas carré dans lequel l'automate se développe
backgroud_color = "white"       #couleur de fond du canvas principal "#D4E6F1"
flag = 0                        #gérer la regénération automatique (système de drapeau)
dico = {}                       #dictionaire principal contenant comme clé la position (x,y) et comme valeur son état (0 ou 1)
temp = {}                       #idem mais temporaire afin de gérer la transition vers un nouveau dictionaire principal
lst = []                        #liste qui contient la règle en format bianaire

#####-----Gestionnaire du graphisme Tkinter-----#####    
  
fen = Tk()
Title = Label(text ='ELEMENTARY CELLULAR AUTOMATON',font = ("Helvetica", 10))
Title.pack(padx=7, pady=12)
b1 = Button(fen, text='Lancer une étape', command = calculer)
b2 = Button(fen, text='Lancer', command = withtime )
b3 = Button(fen, text='Stop', command = stop)
can = Canvas(fen, width = side, heigh = side, bg = backgroud_color) 
b1.pack(side = TOP, padx=5, pady=5)
b2.pack(side = TOP, padx=5, pady=5)
b3.pack(side = TOP, padx=5, pady=5)
can.pack(side=TOP, padx=20, pady=10)

#####-----Choisir la règle et la passer en binaire-----#####

rule_number = int(input("Entrer la règle (0-256): "))
binaire = format(rule_number , "b")         #on utilise la règle "b" de la méthode "format"
lst = []
for i in binaire:                           #on passe chaque chiffre du binaire
    lst.append(int(i)) 
while len(lst) < 8:
    lst.insert(0,0)                         #dans la position 0, le chiffre 0  

#####-----Préparation interface de base-----#####

ligne()
etape1()
fen.mainloop()