from main import setFileName, readData, generate

def translateWithColor(processed, config):
    size = config[3]
    angle = config[2]
    equivalent = {'a': f"pd();fd({size});couleur=(couleur+1)%len(colorData);pencolor(colorData[couleur]);", 'b': f"pu();fd({size});", '+': f"right({angle});", '-': f"left({angle});", '*': "right(180);", '[': "mem.append((pos(), heading()));", ']': "pu();tmp=mem.pop();goto(tmp[0]);seth(tmp[1]);"}
    end = "exitonclick();"
    result = "from turtle import *\ncolor('black')\nspeed(0)\nmem=[]\ncouleur=0\ncolorData=['#FFFFCC','#FFFF99','#FFFF66','#FFFF33','#FFFF00','#FFCC66','#FFCC99','#FFCC33','#FFCC00','#FF9966','#FF9933','#FF9900','#FF6666','#FF6633','#FF6600','#CC6666','#CC3333','#CC3300','#FF3333','#FF3300','#FF0033','#FF0000','#CC0033','#CC0000','#993333','#993300','#990033','#990000','#990066','#993366','#CC3366','#CC0066','#FF3366','#FF0066','#FF3399','#FF0099','#FFCCCC','#CC9999','#FF9999','#FF6699','#FF99CC','#FF66CC','#FFCCFF','#FF99FF','#FF66FF','#FF33FF','#FF00FF','#FF33CC','#CC99CC','#CC66CC','#CC6699','#CC3399','#CC0099','#FF00CC','#CC99FF','#CC66FF','#CC33FF','#CC00FF','#CC00CC','#CC33CC','#9966CC','#996699','#9933CC','#9900CC','#993399','#990099','#9999FF','#9966FF','#9933FF','#9900FF','#660099','#663399','#CCFFCC','#CCFF99','#99FF99','#CCFF66','#CCFF33','#CCFF00','#99FFCC','#66FFCC','#33FFCC','#00FFCC','#33FF99','#00FF99','#CCCC99','#CCCC66','#CCCC33','#CCCC00','#99FF33','#99FF00','#66FF99','#66FF66','#66FF33','#66FF00','#33FF66','#33FF33','#99FF66','#00FF66','#00FF33','#00FF00','#33FF00','#33EE33','#99CC66','#99CC33','#99CC00','#66CC66','#66CC33','#66CC00','#00CC33','#00CC00','#33CC33','#33CC00','#00CC66','#33CC66','#00CC99','#669900','#009933','#009900','#339933','#339900','#33CC99','#66CC99','#99CC99','#009966','#339966','#669966','#999966','#999933','#999900','#669933','#666633','#666600','#336633','#336600','#006633','#006600','#006666','#336666','#CCFFFF','#99FFFF','#66FFFF','#33FFFF','#00FFFF','#99CCCC','#33CCCC','#00CCCC','#669999','#339999','#009999','#0099CC','#CCCCFF','#99CCFF','#66CCFF','#33CCFF','#00CCFF','#3399CC','#6699FF','#3399FF','#0099FF','#9999CC','#6666CC','#6699CC','#666699','#6666FF','#3366FF','#0066FF','#0033FF','#6633FF','#0000FF','#6600FF','#3333FF','#3300FF','#3300CC','#0000CC','#3366CC','#336699','#006699','#0066CC','#3333CC','#0033CC','#330099','#000099','#003399','#333399','#6600CC','#6633CC','#333366','#003366','#000066','#330066','#660066','#663366','#CC9966','#CC6633','#CC6600','#CC9933','#CC9900','#996666','#996633','#996600','#663333','#663300','#660033','#660000','#FFFFFF','#EEEEEE','#E9E9E9','#E5E5E5','#DDDDDD','#CCCCCC','#BBBBBB','#AAAAAA','#999999','#888888','#777777','#666666','#555555','#444444','#333333','#222222','#111111','#333300','#003333','#330033','#330000','#003300','#000033','#000000']\n" #ajout de speed car trop lent sinon

    for letter in processed:
        if letter in equivalent.keys():
            result += equivalent[letter] + "\n"
    result += end
    return result

def mainColor():
    inputFileName, outputFileName = setFileName()
    config = readData(inputFileName)
    processed = generate(config)
    result = translateWithColor(processed, config)
    print(result)
    with open(outputFileName, "w") as file:
        file.write(result)
    exec(result)
    

if __name__=='__main__' : 
    mainColor()