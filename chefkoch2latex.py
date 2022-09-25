import urllib.request
import json
import sys
import math

def main():
    recipe = json.loads(get())
    print("Rezept: " + recipe['title'])
    yn = input("Fortfahren? [Y|N]: ")
    if (yn == "Y" or yn == "y"):
        with open(recipe['title'].replace(' ', '_') + ".tex", "w") as recipefile: # opens file with recipe title as name
            recipefile.write("\\deutsch\n\\begin{recipe}\n[%\n")
            if(recipe['preparationTime']):
                recipefile.write("\tpreparationtime = {\\unit[" + str(recipe['preparationTime']) + "]{min}}")

            if(recipe['cookingTime']):
                recipefile.write(",\n\tbakingtime = {\\unit[" + str(recipe['cookingTime']) + "]{min}}")

            if(recipe['servings']):
                recipefile.write(",\n\tportion = " + str(recipe['servings']) + " Portionen\n")

            recipefile.write("]\n{" + str(recipe['title']) + "}\n\n")


            recipefile.write("\\ingredients{\n")

            ingredients = recipe['ingredientGroups'][0]['ingredients']
            for i in ingredients:
                if i['amount'] != 0.0: # if amount not given, use another notation
                    if math.modf(i['amount'])[0] == 0.0:
                        recipefile.write("\t\\unit[" + str(int(i['amount'])) + "]{" + i['unit'] + "} & " + i['name'] + i['usageInfo'] + " \\\\\n")
                    else:
                        recipefile.write("\t\\unit[" + str(i['amount']) + "]{" + i['unit'] + "} & " + i['name'] + i['usageInfo'] + " \\\\\n")
                else:
                    recipefile.write("\t\\unit[]{" + i['unit'] + "} & " + i['name'] + " \\\\\n")
            recipefile.write("}\n\n")
            recipefile.write("\\preparation{\n")
            recipefile.write("\n")
            instructions = recipe['instructions'].replace('\r','').replace('\n\n','\n').split('\n') # normalizing instructions text
            for step in instructions:
                recipefile.write("\t\\step " + step + "\\\\\n\n")

            recipefile.write("}\n\\end{recipe}\n\\pagebreak")
            return
    else:
        return

def get():
    if len(sys.argv) != 2:
        print("Bitte nur exakt eine URL angeben")
        return
    else:
        id = str(sys.argv[1]).split('www.chefkoch.de/rezepte/')[1].split('/')[0]
        contents = urllib.request.urlopen("https://api.chefkoch.de/v2/recipes/" + id).read()
        return(contents)


main()
