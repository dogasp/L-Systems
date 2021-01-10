import sys

constant = ["-", "+", "*"]

def setFileName(args):
    """récupération des emplacements des fichiers si spécifiés 
    sinon le nom est demandé à l'utilisateur"""
    inputFileName = ""
    outputFileName = "resultat.py"

    while len(args) > 1:
        if args[0] == '-i':
            inputFileName = args[1]
        elif args[0] == '-o':
            outputFileName = args[1]
        else:
            print(f"Argument {args[0]} non reconnus")
        args = args[2:]

    return inputFileName, outputFileName

def fileIsValid(data):
    fileValid = ""
    if data.count("axiome") > 1: #vérification de l'existance d'un unique axiome
        fileValid = "Il y a plus d'un axiome dans le fichier en entrée."
    if "angle" not in data:
        fileValid = "L'angle n'as pas été spécifié dans le fichier en entrée."
    if "taille" not in data: #vérification de l'existence de l'angle et de la taille
        fileValid = "La taille n'as pas été spécifié dans le fichier en entrée."
    if "\n " not in data: #vérification de la présence d'au moins une regle
        fileValid = "Aucune règle n'as été spécifiée dans le fichier en entrée."

    if fileValid != "":
        print(fileValid) #affichage de l'erreur
        return False
    return True

def readRule(i, data):
    value = {} #dictionnaire contenant les regles sous la forme : {[lettre, avant, apres]: regle}
    d = 1
    while data[i+d][0] == " ":
        symbole, regle = (data[i+d].split('"')[1]).split("=")
        d += 1
        if len(symbole) == 1:
            value[(symbole, "", "")] = regle
        elif len(symbole) == 3: #si il y a une indication de position
            if symbole[1] == '>': #si on indique une condition
                value[(symbole[0], "", symbole[2])] = regle
            else:
                value[(symbole[2], symbole[0], "")] = regle
        else:
            value[(symbole[2], symbole[0], symbole[4])] = regle

    #vérifier validité des regles
    return value

def readData(inputFileName):
    """Fonction pour lire les données du fichier en entrée 
    et renvois une liste avec touts les paramètres"""
    config = ["", {}, 0, 0, 0] #axiome, regles, angle, taille, niveau
    with open(inputFileName, 'r') as file:
        data = file.read()
        if fileIsValid(data):
            data = data.split("\n")[:-1]
            for i in range(len(data)):
                row = data[i]
                if row[0] != " ":
                    parameter, value = row.replace(" ", "").split("=")

                    if parameter == "regles":
                        config[1] = readRule(i, data)
                    elif parameter == "axiome":
                        config[0] = value.split('"')[1]
                    elif parameter == "angle":
                        config[2] = float(value)
                    elif parameter == "taille":
                        config[3] = float(value)
                    elif parameter == "niveau":
                        config[4] = int(value)
    return config

def checkContext(path, rule):
    """Fonction qui prend en entrée la chaine à vérifier, 
    l'endroit en cours et la regle à tester et renvois vrai 
    si la regle est respectée"""
    pos = []
    if (not (rule[1] == "" and rule[2] == "") and rule[1] != rule[0]) or rule[1] == rule[2] == "": #cas ou il y a un contexte à droite ou à gauche
        match = rule[1]
        reverse = False
        if rule[2] !="": #si on regarde à droite, on inverse la liste, c'est le même algorithme
            path = "".join(path[::-1]).replace("[", "$").replace("]", "[").replace("$", "]")
            match = rule[2][::-1]
            reverse = True
        index = 0
        mem = []
        tmp = [""] *len(match)
        while index < len(path):
            if path[index] not in constant:
                if path[index] == "[":
                    mem.append(tmp.copy())
                elif path[index] == "]":
                    tmp = mem.pop()
                else:
                    if "".join(tmp) == match and path[index] == rule[0]:
                        toappend = len(path) - index - 1 if reverse else index
                        pos.append(toappend)
                    if tmp != []:
                        tmp.pop(0)
                        tmp.append(path[index])
            index += 1
        
    elif rule[1] != "" and rule[2] != "": #cas ou il y a un contexte à droite et à gauche
        pos = list(set(checkContext(path, [rule[0], "", rule[2]])) & set(checkContext(path, [rule[0], rule[1], ""])))
    return pos

def generate(config):
    """Fonction qui permet d'établir 
    l'était du système au niveau demandé"""
    path = config[0]
    for _ in range(config[4]): #pour chaque niveau
        newPath = [""]*len(path)
        for rule in config[1].keys(): #pour chaque regle
            for place in checkContext(path, rule):
                newPath[place] = config[1][rule]

        for i in range(len(newPath)):
            if newPath[i] == "":
                newPath[i] = path[i]
        path = "".join(newPath)

    return path

def translate(processed, config):
    """Fonction permettant de traduire
    l'était du système en instruction turtle"""
    size = config[3]
    angle = config[2]
    equivalent = {'a': f"pd();fd({size});", 
                  'b': f"pu();fd({size});", 
                  '+': f"right({angle});", 
                  '-': f"left({angle});", 
                  '*': "right(180);", 
                  '[': "mem.append((pos(), heading()));", 
                  ']': "pu();tmp=mem.pop();goto(tmp[0]);seth(tmp[1]);"}

    result = "from turtle import *\ncolor('black')\nspeed(0)\nmem=[]\n" #ajout de speed car trop lent sinon

    for letter in processed:
        if letter in equivalent.keys(): #implémentation du Stochastic L-system
            result += equivalent[letter] + "\n"

    result += "exitonclick();"
    return result

def main():
    """Fonction principale qui execute toutes les autres fonctions"""
    args = sys.argv[1:]
    inputFileName, outputFileName = setFileName(args)
    if inputFileName == "":
        print("Aucun fichier n'as été spécifié avec le commutateur -i")
        return False
    config = readData(inputFileName)
    if config[0] == "":
        return False
    processed = generate(config)
    result = translate(processed, config)
    #print(result)

    with open(outputFileName, "w") as file:
        file.write(result)

    exec(result)
    
if __name__=='__main__' : 
    main()