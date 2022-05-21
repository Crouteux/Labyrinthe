from tkinter import*
from random import choice,randint





def laby(length:int, height:int) -> list:
    '''Initialise le labyrinthe'''
    lab = [[0]*length for k in range(height)]
    coords = [[0]*length for k in range(height)]
    a = 0
    for n in range(height):
        for i in range(length):
            coords[n][i] = {"id": a, "D": True, "B": True, "coords": (n, i)}
            lab[n][i] = coords[n][i]["id"]
            a += 1
    return coords




def trace_wall(tile:dict) -> None:
    '''Trace les contours du labyrinthe'''
    if tile["D"] == True:
        x1 = tile["coords"][1]*TILE_SIZE+TILE_SIZE
        y1 = tile["coords"][0]*TILE_SIZE
        can.create_line(x1, y1, x1, y1+TILE_SIZE, fill=LINE_COLOR)
    if tile["B"] == True:
        x1 = tile["coords"][1]*TILE_SIZE+TILE_SIZE
        y1 = tile["coords"][0]*TILE_SIZE
        can.create_line(x1, y1+TILE_SIZE, x1-TILE_SIZE,
                        y1+TILE_SIZE, fill=LINE_COLOR)




def show_perimeter() -> None:
    '''Trace les contours du labyrinthe'''
    can.create_line(2, 2, 2, Y, fill=LINE_COLOR)
    can.create_line(X, 2, X, Y, fill=LINE_COLOR)
    can.create_line(2, 2, X, 2, fill=LINE_COLOR)
    can.create_line(2, Y, X, Y, fill=LINE_COLOR)




def trace_laby() -> None:
    '''Crée les nombres qui s'afficheront'''
    can.create_rectangle(0, 0, X, Y, fill=BACKGROUND_COLOR)
    for ligne in coords:
        for tile in ligne:
            trace_wall(tile)
            can.create_text(tile["coords"][1]*TILE_SIZE+TILE_SIZE//2, tile["coords"][0]
                            * TILE_SIZE + TILE_SIZE//2, text=tile["id"], fill=LINE_COLOR, font=("18"))
    show_perimeter()




def adjacent(tile:dict, position:str) -> dict:
    '''Renvoie la case voisine et ses coordonnés en fonction de la case précédente '''
    if position == "G":
        return coords[tile["coords"][0]][tile["coords"][1]-1]
    elif position == "D":
        return coords[tile["coords"][0]][tile["coords"][1]+1]
    elif position == "H":
        return coords[tile["coords"][0]-1][tile["coords"][1]]
    elif position == "B":
        return coords[tile["coords"][0]+1][tile["coords"][1]]




def wall_break(tile:dict, position:str) -> None:
    '''Vérifie que les coordonnés de la case voisine à celle passé en parametre sont différents de celle-ci et permet de casser les murs'''
    global NUMBER_TURNS
    adjacent2 = adjacent(tile, position)
    if tile["id"] != adjacent2["id"]:
        if tile["id"] < adjacent2["id"]:
            m = tile["id"]
            remplissage = adjacent2["id"]
            adjacent2["id"] = m
            NUMBER_TURNS += 1
            for ligne in coords:
                for tiles in ligne:
                    if tiles["id"] == remplissage or tiles["id"] == tile["id"]:
                        tiles["id"] = m
        else:
            m = adjacent2["id"]
            remplissage = tile["id"]
            tile["id"] = m
            NUMBER_TURNS += 1
            for ligne in coords:
                for tiles in ligne:
                    if tiles["id"] == remplissage or tiles["id"] == adjacent2["id"]:
                        tiles["id"] = m
        if position == "B":
            coords[tile["coords"][0]][tile["coords"][1]]["B"] = False
        elif position == "D":
            coords[tile["coords"][0]][tile["coords"][1]]["D"] = False




def test() -> None:
    '''Teste la fonction wall_break'''
    for ligne in coords:
        for tile in ligne:
            if coords[0][0]["id"] != tile["id"]:
                return False
    return True


def genere_laby() -> None:
    '''Génère le labyrinthe'''
    trace_laby()
    temps = 1000
    while NUMBER_TURNS != LENGTH*HEIGHT-1:
        i = randint(0, HEIGHT-1)
        j = randint(0, LENGTH-1)
        if i == HEIGHT-1 and j != LENGTH-1:
            if coords[i][j]["D"] == True:
                wall_break(coords[i][j], "D")
        elif j == LENGTH-1 and i != HEIGHT-1:
            if coords[i][j]["B"] == True:
                wall_break(coords[i][j], "B")
        elif i == HEIGHT-1 and j == LENGTH-1:
            pass
        else:
            pos = choice(["B", "D"])
            if coords[i][j][pos] == True:
                wall_break(coords[i][j], pos)
        fen.after(temps, trace_laby)
        temps = temps + 500



LENGTH = 5
HEIGHT = 4
TILE_SIZE = 100
Y = HEIGHT * TILE_SIZE
X = LENGTH * TILE_SIZE
BACKGROUND_COLOR = "light yellow"
LINE_COLOR = "black"
NUMBER_TURNS = 0
dim = f"{X*2}x{Y*2}"
fen = Tk()
fen.geometry(dim)
fen.title("Labyrinthe")
fen.configure(bg='black')
can = Canvas(fen, width=X, height=Y, bg=BACKGROUND_COLOR)
can.pack()
coords = laby(LENGTH, HEIGHT)




genere_laby()
fen.mainloop()
