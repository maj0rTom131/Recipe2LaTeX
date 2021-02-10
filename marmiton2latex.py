from bs4 import BeautifulSoup
import sys
import urllib.request
import re

def main():
    if (len(sys.argv) < 2):
        print("Bitte Link mit angeben!")
        return
    else:
        url = sys.argv[1]
    document = get(url)
    elements = parse(document)
    createTex(elements)
    return

def createTex(recipe):
    with open(recipe['title'].replace(' ', '_') + ".tex", "w") as recipefile:  # opens file with recipe title as name
            recipefile.write("\\franz\n\\begin{recipe}\n[%\n")
            recipefile.write("\tpreparationtime = {\\unit[" + str(recipe['preparationTime']) + "]{min}}")
            recipefile.write(",\n\tbakingtime = {\\unit[" + str(recipe['cookingTime']) + "]{min}}")

            recipefile.write(",\n\tportion = " + str(recipe['servings']) + " Personnes\n")

            recipefile.write("]\n{" + str(recipe['title']) + "}\n\n")


            recipefile.write("\\ingredients{\n")

            ingredients = recipe['ingredients']
            for i in ingredients:
                if ingredients[i] != None: # if amount not given, use another notation
                    recipefile.write("\t\\unit[" + ingredients[i] + "]{} & " + i + " \\\\\n")
                else:
                    recipefile.write("\t\\unit[]{" + ingredients[i] + "} & " + i + " \\\\\n")
            recipefile.write("}\n\n")
            recipefile.write("\\preparation{\n")
            recipefile.write("\\\\\n")
            recipefile.write("\\\\\n")
            instructions = recipe['steps'] # normalizing instructions text
            for step in instructions:
                recipefile.write("\t\\step " + step + "\\\\\n\n")

            recipefile.write("}\n\\end{recipe}\n\\newpage")
            return


def get(url):
    site = urllib.request.urlopen(url)
    return BeautifulSoup(site, features="lxml")


def parse(document):
    elements = dict()
    ingredients = dict()
    steps = []
    elements['title'] = re.search('[^\s][\w\s\']+[^\s]', document.find("h1", class_='main-title').decode_contents()).group()
    elements['preparationTime'] = document.find("div", class_='recipe-infos__timmings__preparation').decode_contents().split('</strong> ')[1].replace('\t', '').split(' ')[0]
    elements['cookingTime'] = document.find("span", class_='recipe-infos__timmings__value').decode_contents().replace('\t', '').replace('\n', '').split(' ')[0]
    elements['servings'] = document.find("span", class_='title-2 recipe-infos__quantity__value').decode_contents()
    for item in document.find("ul", class_='recipe-ingredients__list').findAll("li", class_='recipe-ingredients__list__item'):  # search for each list item in ingredient list
        qty = item.find("span", class_='recipe-ingredient-qt').decode_contents()
        ingredients[item.find("span", class_='ingredient').decode_contents()] = qty
    elements['ingredients'] = ingredients
    for step in document.find("ol", class_='recipe-preparation__list').findAll("li", class_='recipe-preparation__list__item'):  # search for each list item in instructions list
        steps.append(step.decode_contents().replace('\n', '').replace('\t', ''))
    elements['steps'] = steps
    print(elements)
    return elements


main()
