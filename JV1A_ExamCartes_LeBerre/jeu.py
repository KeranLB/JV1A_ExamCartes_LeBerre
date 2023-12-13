### Import ###

######

### Class ###
class Carte:

    def __init__(self, cout_mana, nom, description):
        self.__nom = nom
        self.__description = description
        self.__cout_mana = cout_mana

    def affiche_description(self):
        print(self.__description)

    def get_nom(self):
        return self.__nom
    
    def get_cout_mana(self):
        return self.__cout_mana
    
    def est_joue(self):
        """
        Place la carte sur la zone de jeu du joueur,
        et lui coûte le prix de mana de la carte.

        mana -> entier
        """
        return self.__cout_mana
    
class Mage:

    def __init__(self, nom, pv, mana_max):
        self.__nom = nom
        self.__pv = pv
        self.__mana_max = mana_max
        self.__mana_actuel = mana_max
        self.__main = {}
        self.__defausse = {}
        self.__zone_jeu = {}

    def ad_carte_main(self, carte):
        """
        Ajoute une carte dans la main du mage.

        carte -> objet
        """
        self.__main[carte.get_nom()] = carte

    def retire_carte(dico, carte_nom):
        """
        Retire du dictionnaire la carte entrée en paramètre.

        dico -> dictionnaire
        carte_nom -> chaine de caractères
        """
        tmp = {}
        for keys in dico:
            if keys != carte_nom:
                tmp[keys] = dico[keys]
        return tmp

    def joue_carte(self, carte):
        """
        Transfert la carte joué de la main à la zone de jeu,
        en payant en mana, le cout de mana de la carte.

        carte -> objet
        """
        self.__zone_jeu[carte.get_nom()] = carte
        self.__main = self.retire_carte(self.__main, carte.get_nom())
        self.__mana_actuel -= carte.est_joue()

    def carte_meurt(self, carte):
        """
        Transfert la carte morte de la zone de jeu à la défausse.

        carte -> objet
        """
        if carte.meurt():
            self.__defausse[carte.get_nom()] = carte
            self.__zone_jeu = self.retire_carte(self.__zone_jeu, carte.get_nom())

    def recup_mana(self):
        """
        Récupère le mana une fois que le Mage adverse fini son tour.
        """
        self.__mana_actuel = self.__mana_max

    def attaque(self, cible, carte):
        """
        Attaque Mage/créature avec une des cartes présentent dans la zone de jeu.

        cible -> objet
        carte -> objet
        """
        carte.attaque(cible)

    def augmente_man_max(self, valeur):
        """
        Augmente le mana max du mage

        valeur -> entier
        """
        self.__mana_max += valeur

    def perd_pv(self, degats):
        """
        Fait perdre de la vie au Mage en fonction des dégâts subis
        """
        self.__pv -= degats
    
    def get_attaque(self):
        """
        Cette méthode est utilisé lors des ripostes or le mage ne riposte pas
        quand il subis une attaque, il renvoi donc un score d'attaque égale à 0.
        """
        return 0

class Cristal(Carte):

    def __init__(self, valeur, cout_mana, nom, description):
        Carte.__init__(cout_mana, nom, description)
        self.__valeur = valeur

    def augmente_man_max(self, mage):
        """
        La quantité de mana max du mage qui a joué le cristal
        se voit augmenter son mana de la valeur du crystal.

        mage -> objet
        """
        mage.augmente_mana_max(self.__valeur)

    
class Creature(Carte):

    def __init__(self, pv, score_attaque, cout_mana, nom, description):
        Carte.__init__(cout_mana, nom, description)
        self.__pv = pv
        self.__score_attaque = score_attaque

    def perd_pv(self, degats):
        """
        Fait perdre de la vie à la créature en fonction des dégâts subis
        et retourn une attaque par la suite.

        degats -> entier
        cible -> objet
        """
        self.__pv -= degats
    
    def attaque(self, cible):
        """
        Attaque Mage/Créature.

        cible -> objet
        """
        cible.perd_pv(self.__score_attaque)
        self.perd_pv(cible.get_attaque())

    def meurt(self):
        """
        Si la créature n'a plus de pv alors elle va dans la défausse.
        """
        return self.__pv < 1 

    def get_attaque(self):
        return self.__score_attaque
    

class Blast(Carte):

    def __init__(self, valeur, cout_mana, nom, description):
        Carte.__init__(cout_mana, nom, description)
        self.__valeur = valeur

    def attaque(self, cible):
        """
        Attaque Mage/Créature et ses dégâts correspondent à sa valeur.
        Il est ensuite défausser.

        cible -> objet
        """
        cible.perd_pv(self.__valeur)
    
    def meurt(self):
        """
        Blast meurt après avoir attaquer donc renvoie par défaut True.
        """
        return True
######  
### carte ###
fireball = Blast(30, 4, "Fireball", "Lance une boulle de feu sur une carte dans la zone de jeu adversaire, ou attaque directement le mage adverse.")
goblin = Creature(25, 5, 3, "Goblin", "Petit goblin pouvan attaquer avec sa petite épée les créature ou le mage adverse.")
chevalier = Creature(50, 15, 4, "Chevalier", "Chevalier possède beaucoup de vie et tape plus fort que la moyen car il est entrainé.")
cristal = Cristal(2, 0, "Cristal", "Permet d'augmenter de tour en tour votre quantité de mana max.")

nom_joueur_A = input("entrer votre nom joueur 1 : ")
joueur_A = Mage(nom_joueur_A, 150, 10)
nom_joueur_B = input("entrer votre nom joueur 2 : ")
joueur_B = Mage(nom_joueur_B, 150, 10)

joueur_A.ad_carte_main(fireball)
joueur_A.ad_carte_main(goblin)
joueur_A.ad_carte_main(chevalier)
joueur_A.ad_carte_main(cristal)

joueur_B.ad_carte_main(fireball)
joueur_B.ad_carte_main(goblin)
joueur_B.ad_carte_main(chevalier)
joueur_B.ad_carte_main(cristal)
######
### MAIN ###

######