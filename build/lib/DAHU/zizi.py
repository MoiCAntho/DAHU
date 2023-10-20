from DAHU.maths import Matrice, matriceel

a = matriceel([[5,9,3],[1,7,4],[9,2,3]])
b = a.inverse()
print((a*b).round())

import re

def convert_to_latex(expression):
    # Remplacement des fonctions mathématiques par leur équivalent LaTeX
    expression = re.sub(r"sin", r"\\sin", expression)
    expression = re.sub(r"cos", r"\\cos", expression)
    expression = re.sub(r"tan", r"\\tan", expression)
    expression = re.sub(r"log", r"\\log", expression)
    expression = re.sub(r"sqrt", r"\\sqrt", expression)

    # Remplacement des opérateurs mathématiques
    expression = re.sub(r"\*\*", r"^", expression)
    expression = re.sub(r"\*", r"\\cdot", expression)
    expression = re.sub(r"/", r"\\frac", expression)

    # Ajout des délimiteurs pour les fonctions et les exposants
    expression = re.sub(r"(\w+)\^(\{.*?\}|\w+)", r"\1^{\2}", expression)
    expression = re.sub(r"(\w+)\((.*?)\)", r"\1\left(\2\right)", expression)

    return expression

# Exemple d'utilisation
math_expression = "cos(5x+9)*e**((2x^2)/(log(x**3)))"
latex_command = convert_to_latex(math_expression)
print(latex_command)
