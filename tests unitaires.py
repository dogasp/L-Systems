"""Ce chicher contient tous les tests unitaires de notre programme"""
import unittest
from main import *

class MyTest(unittest.TestCase):
    def test_setFileName(self):                                                 #test de la cfonction de récupération des arguments d'execution
        self.assertEqual(setFileName(['-i', 'Entrée.txt', '-o', 'sortie.txt']), ("Entrée.txt", "sortie.txt"))
    
    def test_fileIsValid(self):                                                 #test de la fonction de vérification de validité du fichier d'entrée (buisson.txt est valide et fougère_sans_taille.txt ne l'est pas)
        with open("tests/buisson.txt", "r") as f:
            self.assertTrue(fileIsValid(f.read()))
        with open("tests/fougère_sans_taille.txt", "r") as f:
            self.assertFalse(fileIsValid(f.read()))

    def test_readData(self):                                                    #test de la lecture des paramètres (avec un L-system classique et un context sensitive L-system)
        self.assertEqual(readData("tests/buisson.txt"), ['--a', {('a', '', ''): 'aa+[+a[+a]-a+a]-[-a-[a]+a]'}, 30.0, 10.0, 4])
        self.assertEqual(readData("tests/context.txt"), ['a[+a]a[-a]a[+a]b', {('a', '', 'b'): 'b'}, 40.0, 10.0, 3])

    def test_generate(self):                                                    #test de la génération à partir d'une configuration classique et une context-sensitive(exemple pris sur Wikipedia)
        config = ['--a', {('a', '', ''): 'aa+[+a[+a]-a+a]-[-a-[a]+a]'}, 30.0, 10.0, 1]
        self.assertEqual(generate(config), "--aa+[+a[+a]-a+a]-[-a-[a]+a]")

        config = ['a[+a]a[-a]a[+a]b', {('a', '', 'b'): 'b'}, 40.0, 10.0, 1]
        self.assertEqual(generate(config), 'a[+a]a[-a]b[+b]b')

    def test_translate(self):                                                   #test de la fonction de conversion de la chaine de caractère vers du code python pour turtle
        config = ['--a', {('a', '', ''): 'aa+[+a[+a]-a+a]-[-a-[a]+a]'}, 30.0, 10.0, 0]
        self.assertEqual(translate("--a", config), "from turtle import *\ncolor('black')\nspeed(0)\nmem=[]\nleft(30.0);\nleft(30.0);\npd();fd(10.0);\nexitonclick();")


if __name__ == "__main__":
    unittest.main()