import sys

def setFileName(args):
    """récupération des emplacements des fichiers si spécifiés 
    sinon le nom est demandé à l'utilisateur"""
    inputFileName = ""
    outputFileName = "resultat.py"                                             #valeur par défaut du fichier de sortie

    while len(args) > 1:                                                       #tant qu'il y a des arguments à lire, on traite les areguments (ils viennent par paire: le comutateur et la valeur)
        if args[0] == '-i':                                                    #si c'est le comutateur du fichier d'entrée, on atribue la valeur à la variable
            inputFileName = args[1]
        elif args[0] == '-o':                                                  #si le nom du fichier de sortie est spécifié, la variable est modifiée
            outputFileName = args[1]
        else:
            print(f"Argument {args[0]} non reconnus")                          #si l'argument n'est pas reconnus, un message est envoyé à l'utilisateur
        args = args[2:]

    return inputFileName, outputFileName

def fileIsValid(data):
    """Fonction qui prend les données d'un fichier d'entrée en paremètre
    et qui renvois True si le fichier est valide"""
    fileValid = ""
    if data.count("axiome") > 1:                                               #vérification de l'existance d'un unique axiome
        fileValid = "Il y a plus d'un axiome dans le fichier en entrée."
    if "angle" not in data:                                                    #vérification de l'existence de l'angle et de la taille
        fileValid = "L'angle n'as pas été spécifié dans le fichier en entrée."
    if "taille" not in data:
        fileValid = "La taille n'as pas été spécifié dans le fichier en entrée."
    if "\n " not in data:                                                      #vérification de la présence d'au moins une regle
        fileValid = "Aucune règle n'as été spécifiée dans le fichier en entrée."

    if fileValid != "":
        print(fileValid)                                                       #Si la variable fileVazlid a été changée, c'est qu'il y a une erreur et elle est affichée
        return False
    return True

def readRule(i, data):
    value = {}                                                                 #dictionnaire contenant les regles sous la forme : {[lettre, avant, apres]: regle}
    d = 1                                                                      #d correspond à l'offset, il est définis à 1 car l'index transmis est celui de la ligne précédente
    while data[i+d][0] == " ":                                                 #tant qu'on se trouve sur une ligne contenant des règles
        symbole, regle = (data[i+d].split('"')[1]).split("=")                  #extraction de la chaine de caractère et séparation du symbole et de la valeur
        if len(symbole) == 1:                                                  #si le symbole a un longeur de 1, c'est qu'il n'y a pas de contexte, et la regle est faite
            value[(symbole, "", "")] = regle
        elif len(symbole) == 3:                                                #si il y a UNE indication de position
            if symbole[1] == '>':                                              #et que c'est une indication à droite, on attribue la règle en conséquence, même chose à gauche
                value[(symbole[0], "", symbole[2])] = regle
            else:
                value[(symbole[2], symbole[0], "")] = regle
        else:
            value[(symbole[2], symbole[0], symbole[4])] = regle                #Sinon c'est que c'est une règle multidirectionnelle
        d += 1
    return value

def readData(inputFileName):
    """Fonction pour lire les données du fichier en entrée 
    et renvois une liste avec touts les paramètres"""
    config = ["", {}, 0, 0, 0, []]                                                 #variable contenant la configuration (axiome, regles, angle, taille, niveau, constantes)
    with open(inputFileName, 'r') as file:                                     #lecture du fichier en entrée
        data = file.read()
        if fileIsValid(data):                                                  #vérification de la validité du fichier en entrée
            data = data.split("\n")                                            #séparation de chaques lignes
            for i in range(len(data)):
                row = data[i]
                if len(row) > 0 and row[0] != " ":                             #pour chaque ligne, on regarde si elle n'est pas vide et si elle ne contient pas d'espace (sinon c'est une règle)
                    parameter, value = row.replace(" ", "").split("=")         #séparation de la ligne entre le paramètre et la valeur avec le symbole =

                    if parameter.replace("è", "e") == "regles":                #si c'est une règle, execution de la fonction de récupération des règles
                        config[1] = readRule(i, data)
                    elif parameter == "axiome":
                        config[0] = value.split('"')[1]                        #extraction de l'axiome des guillemets
                    elif parameter == "angle":
                        config[2] = float(value)                               #le reste est juste une conversion vers int ou float
                    elif parameter == "taille":
                        config[3] = float(value)
                    elif parameter == "niveau":
                        config[4] = int(value)
                    elif parameter == "constantes":                            #récupération des constantes
                        config[5] = value
    return config

def checkContext(path, rule, constant):
    """Fonction qui prend en entrée la chaine à vérifier
    et la regle à tester et renvois les emplacements où la regle est vérifiée"""
    pos = []
    if not (rule[1] != "" and rule[2] != ""):                                  #cas ou il y a un contexte à droite ou à gauche (porte xor)
        match = rule[1]                                                        #match correspond à la chaine à retrouver avant le symbole en question
        reverse = False                                                        #booléen qui mémorise si on va vers la droite (True) ou vers la gauche (False)
        if rule[2] !="":                                                       #si on regarde à droite, on inverse la liste, c'est le même algorithme
            path = "".join(path[::-1]).replace("[", "¤").replace("]", "[").replace("¤", "]") #inversion de l'axiome et inversion des crochets (on a utilisé ¤ car il a très peu de chances d'être utilisé comme symbole)
            match = rule[2][::-1]                                              #[::-1] permet d'inverser une chaîne de caractère
            reverse = True
        index = 0                                                              #index permet de parcourir path
        mem = []                                                               #mem permet de garder tmp en mémoire quand le programme explore une branche sous forme de pile
        tmp = [""] *len(match)                                                 #correspond aux len(match) derniers caractères parcourus
        while index < len(path):
            if "".join(tmp) == match and path[index] == rule[0]:               #pour les autres lettres, si on obtient la séquence de match, et que le symbole est le bon, c'est qu'on a trouvé un emplacement
                toappend = len(path) - index - 1 if reverse else index         #inversion de l'index si on travaille à l'envers (à droite)
                pos.append(toappend)                                           #ajout de la position dans la liste des positions
            if path[index] not in constant:                                    #si la lettre parcourue n'est pas dans les constantes (voir ligne 3)
                if path[index] == "[":                                         #si on rencontre une branche, on sauvegarde le tmp (l'historique) dans la pile
                    mem.append(tmp.copy())
                elif path[index] == "]":                                       #récupération de l'élément en haut de la pile
                    tmp = mem.pop()
                elif tmp != []:                                                #si tmp n'est pas nul, on retire le dernier élément et on ajoute celui actuel (tmp est une file)
                    tmp.pop(0)
                    tmp.append(path[index])
            index += 1
    else:                                                                      #cas ou il y a un contexte à droite et à gauche, on fait l'union du contexte seulement à droite et le contexte seulement à gauche
        pos = list(set(checkContext(path, [rule[0], "", rule[2]], constant)) & set(checkContext(path, [rule[0], rule[1], ""], constant)))
    return pos

def generate(config):
    """Fonction qui permet d'établir 
    l'était du système au niveau demandé"""
    path = config[0]                                                           #path correspond à l'axiome
    for _ in range(config[4]):                                                 #pour chaque niveau
        newPath = [""]*len(path)                                               #création d'une nouvelle variable qui contiendra le résultat
        for rule in config[1].keys():                                          #boucle pour chaque règle
            for place in checkContext(path, rule, config[5]):                             #récupération des positions qui correspondent à la règle
                newPath[place] = config[1][rule]                               #à chaque position, la valeur est attribuée
        for i in range(len(newPath)):                                          #pour chaque emplacement où newPath est vide, c'est qu'il n'y a pas de règle valide, le symbole est recopié
            if newPath[i] == "":
                newPath[i] = path[i]
        path = "".join(newPath)                                                #modification de la variable path
    return path

def translate(processed, config):
    """Fonction permettant de traduire
    l'était du système en instruction turtle"""
    size = config[3]                                                           #attribution des valeurs suivant la configuration
    angle = config[2]
    equivalent = {'a': f"pd();fd({size});",                                    #equivalent est un dictionnaire servant à traduire les caractères en code python pour turtle
                  'b': f"pu();fd({size});", 
                  '+': f"right({angle});", 
                  '-': f"left({angle});", 
                  '*': "right(180);", 
                  '[': "mem.append((pos(), heading()));", 
                  ']': "pu();tmp=mem.pop();goto(tmp[0]);seth(tmp[1]);",
                  'l': "pensize(6);",
                  'm': "pensize(3);",
                  's': "pensize(1);",
                  'r': "pencolor('#FF0000');",
                  'g': "pencolor('#00FF00');",
                  'b': "pencolor('#0000FF');"}

    result = "from turtle import *\ncolor('black')\nspeed(0)\nmem=[]\n"        #code par défaut dans tous les fichiers résultat

    for letter in processed:                                                   #pour chaque lettre, on regarde son équivalent, si il n'en a pas, rien ne se passera. Un retour à la ligne est ajouté pour plus de lisibilité
        if letter in equivalent.keys():
            result += equivalent[letter] + "\n"

    result += "exitonclick();"                                                 #ajout de la dernière ligne permettant de quitter le programme une fois le tracé finis
    return result

def main():
    """Fonction principale qui execute toutes les autres fonctions"""
    args = sys.argv[1:]                                                        #récupération des arguments passés lors de l'execution du programme, on n'as pas besoins du premier (nom du fichier executé)
    inputFileName, outputFileName = setFileName(args)                          #récupération du fichier d'entrée et de sortie
    if inputFileName == "":                                                    #arrêt du programme aucun fichier n'as été spécifié en entrée
        print("Aucun fichier n'as été spécifié avec le commutateur -i")
        return False
    config = readData(inputFileName)                                           #création de la variable des paramètres
    if config[0] == "":                                                        #si le ficher est invalide ou qu'il y a des règles incopmpatibles, le programme est quitté
        return False
    processed = generate(config)                                               #génération de la chaine de caractère au niveau demandé
    result = translate(processed, config)                                      #conversion de la chaine en code turtle
    print(result)

    with open(outputFileName, "w") as file:                                    #sauvegarde du résultat
        file.write(result)

    exec(result)                                                               #execution du résultat
    
if __name__=='__main__' : 
    main()