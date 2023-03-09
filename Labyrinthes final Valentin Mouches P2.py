from tkinter import *                                               
from random import randint ,choice
from time import sleep


tab = []
tab_dico = []
taille = 0
x = 0


root = Tk()                                                         
root.geometry("700x700")
root.minsize(200,200)
root.title("labyrinthe")
root.config(bg = "#000000")
Laby = Canvas(root,width= 600, height=600, bg= "#F6FFB3")
end = Label(text = "Fini", bg = "#999999")
texte = Label(root,text= "entrez le nombre de cases de côté",bg = "#999999")
clique = Label(root,text="clique gauche pour lancer")
nb = Entry(root, bd = 10,relief=FLAT,bg = "#999999" )


def init(x:int) -> None:                                                        
    global tab,tab_dico,taille
    tab , tab_dico = init_laby(x, x)
    taille = init_canvas(x, x)
    clique.pack()
    Laby.pack()
    Laby.config()
    affiche_laby(tab)

    
def get_entry(event) -> int:
    global x
    x = int(nb.get())   
    nb.delete(0,)       
    nb.destroy()         
    texte.destroy()     
    init(x)             
    return x
    
    
def init_laby(x:int,y:int) -> list:
    tab = [[k * x + i for i in range(y)] for k in range(x)]         
    tab_dico = [[ 0 for i in range(x)] for k in range(y)]           
    for i in range(len(tab)):                                       
        for k in range(len(tab[0])):
            tab_dico[i][k] = {"id" : tab[i][k], "D":True, "B" : True, "co":(i,k)}
    return tab , tab_dico


def init_canvas(x:int,y:int) -> int:                                
    l = int(600/x)                         
    taille = l                                                      
    for i in range(0,620,l):    
        Laby.create_line(0,i,600,i)                                                        
        Laby.create_line(i,0,i,600)                                 
    return taille 


def affiche_laby(tab:list) -> None:                                        
    for i in range(len(tab)):
        print(tab[i])

        
def voisin(case:tuple,position:str,taille:int) -> tuple:                                 
    x = case[0]
    y = case[1]
    if position == 'D':                                                                 
        return tab_dico[x+1][y],(x+1)*taille,y*taille,(x+1)*taille,(y+1)*taille        
    elif position == 'B' :                                                              
        return tab_dico[x][y+1],x*taille,(y+1)*taille,(x+1)*taille,(y+1)*taille         

    
def casse_mur(x:int,y:int,position:str,taille:int) -> list:
    global tab, tab_dico                                            
    info = 0
    dico_voisin,pos1,pos2,pos3,pos4 = voisin((x,y), position,taille)

    if dico_voisin["id"] != (tab_dico[x][y])["id"]:                  
        (tab_dico[x][y])[position] = False                         
        id_voisin = dico_voisin["id"]                             
        n_id = (tab_dico[x][y])["id"]                             
        Laby.create_line(pos1,pos2,pos3,pos4,fill = "#F6FFB3")    
        #boucle qui parcour tout le tableau 
        for i in range(len(tab)):                                   
            for k in range(len(tab[0])):
                if (tab_dico[i][k])["id"] == id_voisin:            
                    (tab_dico[i][k])["id"] = n_id                  
                    tab[i][k] = n_id                              
        info = 1
    return tab,tab_dico,info


def genere_laby(event) -> None:
    global x,taille,tab,tab_dico
    clique.destroy()
    tour = int(x**2 -1)                                      
    while tour != 0:                                          
        Laby.update()
        a = randint(0, x-1)                                         
        o = randint(0, x-1)
        
        if o == x-1 and a == x-1 :                                 
            info = 0                                               
        elif o == x-1 :                                            
            position = 'D'                                        
            tab,tabdico,info = casse_mur(a, o, position,taille)   
        elif a == x-1 :                                           
            position = 'B'                                         
            tab,tabdico,info = casse_mur(a, o, position,taille)    
        else:                                                    
            position = choice(['D','B'])                            
            tab,tabdico,info = casse_mur(a, o, position,taille)     
        if info == 1: 
            tour -= 1
        else:
            pass                     
        affiche_laby(tab)
    end.pack()

    
texte.pack()
nb.pack(pady = 10)
print(x)


root.bind('<Return>',get_entry)
Laby.bind("<Button-1>", genere_laby)
root.mainloop()

