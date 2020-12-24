import sys

def setFileName():
    """récupération des emplacements des fichiers si spécifiés 
    sinon le nom est demandé à l'utilisateur"""
    inputFileName = ""
    outputFileName = "resultat.py"
    args = sys.argv[1:]
    while len(args) > 1:
        if args[0] == '-i':
            inputFileName = args[1]
        elif args[0] == '-o':
            outputFileName = args[1]
        else:
            print(f"Argument {args[0]} non reconnus")
        args = args[2:]

    if inputFileName == "":
        inputFileName = input("Entrez le nom du fichier: ")

    return inputFileName, outputFileName

def readData(inputFileName):
    config = ["", {}, 0, 0, 0] #axiome, regles, angle, taille, niveau
    with open(inputFileName, 'r') as file:
        data = file.read().split("\n")[:-1]
        for i in range(len(data)):
            row = data[i]
            if row[0] != " ":
                parameter, value = row.replace(" ", "").split("=")
                if parameter == "regles":
                    value = {}
                    d = 1
                    while data[i+d][0] == " ":
                        symbole, regle = (data[i+d].split('"')[1]).split("=")
                        d += 1
                        value[symbole] = regle
                    config[1] = value

                if parameter == "axiome":
                    config[0] = value.split('"')[1]
                elif parameter == "angle":
                    config[2] = float(value)
                elif parameter == "taille":
                    config[3] = float(value)
                elif parameter == "niveau":
                    config[4] = int(value)
    return config

def generate(config):
    path = config[0]
    for _ in range(config[4]): #pour chaque niveau
        newPath = ""
        for letter in path: #pour chaque lettre du chemin
            if letter in config[1].keys():
                newPath += config[1][letter]
            else:
                newPath += letter
        path = newPath
    return path

def translate(processed, config):
    size = config[3]
    angle = config[2]
    equivalent = {'a': f"pd();fd({size});", 'b': f"pu();fd({size});", '+': f"right({angle});", '-': f"left({angle});", '*': "right(180);", '[': "mem.append((pos(), heading()));", ']': "pu();tmp=mem.pop();goto(tmp[0]);seth(tmp[1]);"}
    end = "exitonclick();"
    result = "from turtle import *\ncolor('black')\nspeed(0)\nmem=[]\n" #ajout de speed car trop lent sinon

    for letter in processed:
        if letter in equivalent.keys(): #implémentation du Stochastic L-system
            result += equivalent[letter] + "\n"
    result += end
    return result

def saveResult(result, outputFileName):
    with open(outputFileName, "w") as file:
        file.write(result)

def main():
    inputFileName, outputFileName = setFileName()
    config = readData(inputFileName)
    processed = generate(config)
    result = translate(processed, config)
    print(result)
    saveResult(result, outputFileName)
    

if __name__=='__main__' : 
    main()