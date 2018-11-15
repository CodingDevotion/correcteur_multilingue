#######################################################################
##  Programme spellChecker :
##      Programme qui permet de corriger une phrase dans le fichier
##      input.txt à l'aide du dictionnaire contenu dans le fichier
##      dict.txt.
##
##  Par Alexandre Chartrand - 20062025
##  En date du 29-04-2017
##
##  ***** IMPORTANT *****
##      Les mots du dictionnaire doivent être MINUSCULES
##      dans le fichier dict.txt
##
##      Le programme fonctionne pour toutes les langues,
##      tant que les caractères sont en utf-8
##  *********************
##
##  (BONUS 1)
##  La ponctuation est ajoutée comme ci:
##
##  input: "ai"
##  output: [ai]"(air, aim)" <- Les guillemets encadrent les parenthèses
##
#######################################################################
import io

class HashTable():

    def __init__(self, size):
        self.size = size
        self.Table = [[] for i in range(size)]

    # Retourne la longueur du tableau
    def __len__(self):
        return self.size


    # hashFonction : Fonction qui crée une clé numérique
    # à partir d'un string (mot). J'ai utilisé l'algorythme
    # djb2. Source : http://www.cse.yorku.ca/~oz/hash.html
    # Traduit de C en python par moi-même.

    def hashFonction(mot):
        hash = 5381
        for i in mot:
            hash = ((hash << 5) + hash) + ord(i)
        return hash


    # Fonction get : Retourne la valeur dans la hashTable à
    # une clé donnée. Permet de trouver si un mot est dans la
    # hashTable rapidement.
    def __get__(self, mot):

        # On calcule la clé
        indexHashingTable = HashTable.hashFonction(mot) % self.size

        # On cherche, à une clé donnée, si le mot exite
        for i in self.Table[indexHashingTable]:
            if i == mot:
                return i


    # Fonction set : Ajoute un mot dans la hashTable
    def __set__(self, mot):

        # On calcule la cle
        indexHashingTable = HashTable.hashFonction(mot) % self.size

        # Si, à un indice de la hashTable donné, il n'y a aucune
        # valeur, c'est donc qu'il n'y a aucune collision.
        # On ajoute donc le mot automatiquement dans la table.
        if len(self.Table[indexHashingTable]) == 0:
            self.Table[indexHashingTable].append(mot)

        else:

            # Sinon, on ajoute un nouveau mot, dans un tableau
            # (J'utilise la stratégie avec la liste chainée pour
            # traiter les collisions)
            self.Table[indexHashingTable].append(mot)



# Classe qui initialise et execute le correcteur
# Un peu comme une classe main.
# La classe lit les fichiers, initialise une HashTable,
# corrige la phrase et l'affiche
class SpellCHecker:

    def __init__(self):

        # Lecture des fichiers dict et input
        self.input = SpellCHecker.readInput(self)
        self.dict = SpellCHecker.readDictionnary(self)

        # Trouver l'alphabet utilisé dans le dictionnaire
        self.alphabet = SpellCHecker.trouverAlphabet(self)

        # Initialisation d'une hashTable de grandeur
        # 2 X nombre mots dans le dictionnaire
        self.hashTable = HashTable(len(self.dict)*2)

        # On insère tous les mots du dictionnaire dans la hashTable
        self.allWordsInHashTable(self.hashTable)

        # On corrige tous les mots
        self.corrigerMots(self.input)


    # Fonction qui lit le fichier dictionnaire et le retourne
    def readDictionnary(self):
        with io.open('dict.txt', 'r', encoding='utf8') as fichier:
            dictionnary = fichier.readlines()
        return dictionnary


    # Fonction qui lit le fichier input et retourne la phrase
    def readInput(self):
        with io.open('input.txt', 'r', encoding='utf8') as fichier:

            # Seule la premiere ligne du fichier input.txt est lue
            input = fichier.readline()
        return input


    # Fonction qui mémorise l'alphabet du langage contenu dans dict.txt
    def trouverAlphabet(self):

        alphabet = ""

        # Pour tous les caractères dans dictionnaire, si un certain
        # caractère n'est pas dans alphabet, on l'ajoute.
        for i in str(self.dict).rstrip("\n"):
            for j in i:
                if j.lower() not in alphabet:
                    alphabet+=j

        return alphabet


    # Fonction qui place tous les mots contenus dans le dictionnaire
    # dans une hashTable
    def allWordsInHashTable(self, hashTable):
        text = self.dict
        for i in text:
            hashTable.__set__(i.rstrip('\n'))


    # Fonction qui corrige tous les mots contenus dans la phrase.
    # La fonction appelle "corrigerMot", qui corrige un mot dans la phrase

    def corrigerMots(self, sentense):

        # On supprime de la phrase la ponctuation et les \n
        sentense = sentense.rstrip('\n')
        sentense = self.supprimerPonctuation(sentense)

        # On initialise une phrase corrigée
        newSentense = ""

        # On sépare la phrase en mots, et on corrige chacun des mots
        words = sentense.split(' ')
        for i in words:
            newSentense = newSentense + self.corrigerMot(i) + " "

        print(newSentense)


    # Fonction qui supprime la ponctuation et
    # retourne la phrase sans ponctuation
    def supprimerPonctuation(self, sentense):
        uselessChar = [".",",",":",";","!","?","\""]

        for i in sentense:

            # Si la phrase contient une apostrophe,
            # un sépare le mot en 2
            if i == '\'':
                sentense = sentense[:sentense.index(i)] + " " \
                           + sentense[sentense.index(i)+1:]

            # Si la phrase contient un des caractères innutiles,
            # on le supprime
            if i in uselessChar:
                sentense = sentense[:sentense.index(i)] \
                           + sentense[sentense.index(i)+1:]

        return sentense


    # (BONUS 1) Fonction qui remet la ponctuation en place, à la fin
    # d'un mot

    def ajouterPonctuationFin(self, sentense, mot):
        uselessChar = [".", ",", ":", ";", "!", "?", "\"", "\'"]
        sentense = sentense.rstrip('\n')

        for i in sentense:
            if i == '\'' or i == '\"':
                sentense = sentense[:sentense.index(i)+1] + " " \
                           + sentense[sentense.index(i)+1:]

        words = sentense.split(' ')

        # Si la phrase contient un " ou un ' à la fin d'un mot,
        # et que ce mot est identique au mot mis en paramètre on ajoute
        # " ou ' à la fin du mot

        for i in words:
            # Si le mot a 2 pontuations. Ex: "allo"
            if i[0:1] in ["\'", "\""]:
                if i[1:-1] == mot:
                    if i[-1] in uselessChar:
                        return i[-1:]

            # Si le mot a seulement une ponctuation à la fin:
            # Ex : allo.
            else:
                if i[:-1] == mot:
                    if i[-1] in uselessChar:
                        return i[-1:]

        # Sinon, on retourne aucune ponctuation supplémentaire
        return ""


    # (BONUS 1) Fonction qui remet la ponctuation en place, au
    # debut d'un mot
    def ajouterPonctuationDebut(self, sentense, mot):

        sentense = sentense.rstrip('\n')
        words = sentense.split(' ')

        # Si la phrase contient un " ou un ' au debut d'un mot,
        # et que ce mot est identique au mot mis en parametre on
        # ajoute " ou ' au debut du mot
        for i in words:

            # Si le mot a 2 pontuations. Ex: "allo"
            if i[1:-1] == mot:
                if i[0] in ["\'","\""]:
                    return i[0]

            # Si le mot a seulement une ponctuation a la fin:
            # Ex : "allo
            if i[1:] == mot:
                if i[0] in ["\'", "\""]:
                    return i[0]

        # Sinon, on retourne aucune ponctuation supplémentaire
        return ""


    # Fonction qui corrige un mot
    # La fonction encadre un mot qui n'est pas présent dans le
    # dictionnaire et effectue les 5 tests nessessaires si ce mot
    # est erroné.
    def corrigerMot(self, mot):

        if not self.hashTable.__get__(mot.lower()):

            # Si le mot n'est pas dans le dictionnaire, il
            # est encadré
            motEncadre = "["+ mot + "]"

            # Tableau qui contient toutes les corrections possibles
            # d'un mot
            correction = [self.intervertirPaireCaracteres(mot),
                          self.insererLettreAlphabet(mot),
                          self.supprimerChCaractereDuMot(mot),
                          self.remplacerChCaractereDuMot(mot),
                          self.separerEn2Mots(mot)]

            correctionSansrepetition = ""



            for i in correction:
                # On supprime tous les doublons en transformant
                # chaque propositions de correction en set
                i = set(i)

                for j in i:

                    # On supprime les tests qui ont retournés
                    # le mot sans correction
                    if j != mot:

                        # on ajoute une virgule
                        # après chaque propositions.
                        correctionSansrepetition += j+", "

            # On supprime la dernière virgule
            correctionSansrepetition = correctionSansrepetition[:-2]

            # On retourne le mot corrige, on ajoute sa ponctuation, et
            # on ajoute les parenthèses.
            return motEncadre + self.ajouterPonctuationDebut(self.input, mot) \
                              + "(" \
                              + str(correctionSansrepetition) \
                              + ")" \
                              + self.ajouterPonctuationFin(self.input, mot)


        # Sinon, si le mot n'a pas à être corrigé, il est retourné avec
        # sa ponctuation, sans correction
        else:
            return self.ajouterPonctuationDebut(self.input, mot) \
                   + mot + self.ajouterPonctuationFin(self.input, mot)


    # TEST 1 : Intervertir chaque paire de caractères adjacents d'un mot
    def intervertirPaireCaracteres(self, mot):

        # On initialise un tableau qui contient toutes les
        # possibilites de correction
        motsCorriges = []

        for i in range(0, len(mot) - 1):

            # On échange les caractères mot[i] et mot[i+1]
            a = mot[i]
            b = mot[i + 1]
            newMot = mot[:i] + b + a + mot[i + 2:]

            # Si un mot avec une paire intervertie est dans le dictionnaire,
            # on ajoute le mot aux propositions de correction
            if self.hashTable.__get__(newMot.lower()):
                motsCorriges.append(newMot)

        # Si le mot ne contient pas de correction, on ajoute seulement
        # le mot, non corrigé
        if len(motsCorriges) == 0:
            motsCorriges.append(mot)

        return motsCorriges


    # TEST 2 : Insérer chaque lettre de l'alphabet entre chaque paires
    #  de caractères adjacents du mot
    def insererLettreAlphabet(self, mot):

        motsCorriges = []
        for i in self.alphabet:
            for j in range(0, len(mot) + 1):

                # Pour toutes les lettres de l'alphabet,
                # on ajoute la lettre à toutes les
                # positions possibles
                newMot = mot[:j] + i + mot[j:]
                if self.hashTable.__get__(newMot.lower()):
                    motsCorriges.append(newMot)

        if len(motsCorriges) == 0:
            motsCorriges.append(mot)

        return motsCorriges

    # TEST 3 : Supprimer chaque caractère du mot
    def supprimerChCaractereDuMot(self, mot):

        motsCorriges = []
        for i in range(0, len(mot)):

            #Pour toutes les lettres d'un mot, on
            # supprime une lettre à la fois
            newMot = mot[:i] + mot[i+1:]

            if self.hashTable.__get__(newMot.lower()):
                if newMot not in motsCorriges:
                    motsCorriges.append(newMot)

        if len(motsCorriges) == 0:
            motsCorriges.append(mot)

        return motsCorriges


    # TEST 4 : Remplacer chaque caractère du mot par chaque lettre de
    # l'alphabet.
    def remplacerChCaractereDuMot(self, mot):

        motsCorriges = []

        for i in self.alphabet:
            for j in range(0, len(mot)):

                # Pour toutes les lettres du mots,
                # on supprime la lettre a la position j et on
                # ajoute la lettre i a la place
                newMot = mot[:j] + i + mot[j+1:]

                if self.hashTable.__get__(newMot.lower()):
                    motsCorriges.append(newMot)

        if len(motsCorriges) == 0:
            motsCorriges.append(mot)

        return motsCorriges


    # TEST 5: Séparer le mot en paire de mots de toutes
    # les n - 1 façons possibles (
    def separerEn2Mots(self, mot):

        motsCorriges = []

        # Pour toutes les n-1 combinaisons
        # on sépare le mot en 2 mots a et b
        for i in range(1, len(mot)):
            a = mot[:i]
            b = mot[i:]

            # Si a et b sont dans le dictionnaire,
            # on ajoute a + " " + b comme suggestion
            if (    self.hashTable.__get__(a.lower()) and
                    self.hashTable.__get__(b.lower())):

                c = "" + a + " " + b
                motsCorriges.append(c)


        if len(motsCorriges) == 0:
            motsCorriges.append(mot)

        return motsCorriges


if __name__ == "__main__":
    # On lance une instance de SpellCHecker
    SpellCHecker()