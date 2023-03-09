from tkinter import *                                               
from random import randint ,choice
from time import sleep




#initialisation des variables
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



#initialise le jeu
def init(x:int) -> None:                                                        
    global tab,tab_dico,taille
    tab , tab_dico = init_laby(x, x)
    taille = init_canvas(x, x)
    clique.pack()
    Laby.pack()
    Laby.config()
    affiche_laby(tab)
#prend en argument le nombre de cases de côté
#on peut le tester avec plusieur entrée x




#evenement qui va initialiser tout le canvas
#après avoir reçu l'information du nombre de cases de côté
#return le nombre de cases de longueur du tableau
def get_entry(event) -> int:
    global x
    x = int(nb.get())   #recupère le texte du entry
    nb.delete(0,)       #supprime le texte du entry
    nb.destroy()        #supprime le widget 
    texte.destroy()     #detruit le label
    init(x)             #lance le canvas
    return x
    
#prend en argument les abscisses et les ordonnés 
#creer le tableau tab qui contient les id de chaque case
#creer le tableau de dictionnaire tab_dico qui contient les informations des cases 
#return nos tableaux 
def init_laby(x:int,y:int) -> list:
    tab = [[k * x + i for i in range(y)] for k in range(x)]         #creation de tab
    tab_dico = [[ 0 for i in range(x)] for k in range(y)]           #creation de tab_dico
    for i in range(len(tab)):                                       #boucle pour integrer les dicos au tab_dico
        for k in range(len(tab[0])):
            tab_dico[i][k] = {"id" : tab[i][k], "D":True, "B" : True, "co":(i,k)}
    return tab , tab_dico


#prend en argument les abscisses et les ordonnés 
#creer le tableau dans le canvas Laby
#return la taille en abscisse et en ordonné des cases

def init_canvas(x:int,y:int) -> int:                                #dessine notre grille en fonction de notre entrer initial
    l = int(600/x)                         
    taille = l                                                      #taille definie la longueur et la largeure d'une case
    for i in range(0,620,l):    
        Laby.create_line(0,i,600,i)                                 #dessine les ligneshorizontale                       
        Laby.create_line(i,0,i,600)                                 #dessine les ligne verticale
    return taille 



def affiche_laby(tab:list) -> None:                                        
    for i in range(len(tab)):
        print(tab[i])


def voisin(case:tuple,position:str,taille:int) -> tuple:                                 #retransmet le dico de la case voisin et les coo du mur entre les deux cases
    x = case[0]
    y = case[1]
    if position == 'D':                                                                 #en fonction de si le voisin est a droite
        return tab_dico[x+1][y],(x+1)*taille,y*taille,(x+1)*taille,(y+1)*taille         #return le dico du voisin et les coordonnés du mur commun
    elif position == 'B' :                                                              #en fonction de si le voisin est en bas 
        return tab_dico[x][y+1],x*taille,(y+1)*taille,(x+1)*taille,(y+1)*taille         #return le dico du voisin et les coordonnés du mur commun
#peut se tester avec un choix de case 
# une erreur se creer si les case ne sont pas verifier. On obtien alors des out of range
#le probleme est compenser dans genere_laby


    
def casse_mur(x:int,y:int,position:str,taille:int) -> list:
    global tab, tab_dico                                            #appel des tab
    info = 0
    dico_voisin,pos1,pos2,pos3,pos4 = voisin((x,y), position,taille)#appel voisin et les coo du mur

    if dico_voisin["id"] != (tab_dico[x][y])["id"]:                  #regarde leurs id
        (tab_dico[x][y])[position] = False                          #on change la valeur du dico
        id_voisin = dico_voisin["id"]                               #on recupère l'id du voisin
        n_id = (tab_dico[x][y])["id"]                               #on recupère l'id de la case
        Laby.create_line(pos1,pos2,pos3,pos4,fill = "#F6FFB3")      #on efface le mur
        #boucle qui parcour tout le tableau 
        for i in range(len(tab)):                                   
            for k in range(len(tab[0])):
                if (tab_dico[i][k])["id"] == id_voisin:             #si l'id de la case et le meme que celui de la case voisine initial
                    (tab_dico[i][k])["id"] = n_id                   #alors son id change pour celui de la case initial
                    tab[i][k] = n_id                                #et dans tab aussi
        info = 1
    return tab,tab_dico,info
#on peut le tester sur toutes les cases


def genere_laby(event) -> None:
    global x,taille,tab,tab_dico
    clique.destroy()
    tour = int(x**2 -1)                                       #appel de la dimension du tableau
    while tour != 0:                                          #boucle 
        Laby.update()
        a = randint(0, x-1)                                         # genère une case d'abscise a et d'ordonné o
        o = randint(0, x-1)
        
        if o == x-1 and a == x-1 :                                  # si notre case est en bas a droite 
            info = 0                                                # info = 0 veut dire que la verification est bonne et que rien n'a été cassé
        elif o == x-1 :                                             # si notre case est en bas
            position = 'D'                                          #on casse a droite
            tab,tabdico,info = casse_mur(a, o, position,taille)     #on fait casser le mur
        elif a == x-1 :                                             #si le notre case est à droite
            position = 'B'                                          # on casse en bas
            tab,tabdico,info = casse_mur(a, o, position,taille)     #on fait casser le mur
        else:                                                       # si notre case est ailleurs
            position = choice(['D','B'])                            #on laisse le hasard choisir
            tab,tabdico,info = casse_mur(a, o, position,taille)     #on case le mur

        #si une modification a été apporté alors on reduit tour de 1
        if info == 1: 
            tour -= 1
        else:
            pass                     
        affiche_laby(tab)
    end.pack()
#on peut le tester avec 


#affichage des widjets
texte.pack()
nb.pack(pady = 10)
print(x)


#lancement de la fenetre et ajout de l'event Button-1 et entrer 
root.bind('<Return>',get_entry)
Laby.bind("<Button-1>", genere_laby)
root.mainloop()

'''desciption de l'execution

#notre fenetre s'affiche :label texte, entry
changement de l'affichage : label, can, bind
lancement : can
fin : can, label, id dans le shell
'''
