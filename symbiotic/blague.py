

import time
import random


BLAGUES = (  # '$' is a pause
    "python le poli\n$java   le joli\n\n$C      $l'E. Coli ",
    "Au cinéma, quel est le plan préféré des bioinformaticiens ?\n\n$$$Le plan$-séquence ! ",
    "ASP rentre dans un bar.\n$$Le barman: «une bière ?»\n$ASP: «Non.»\n$«Un alcool fort ?»\n$«Non.»\n$«un jus ?»\n$«Non.»\n$«de l'eau alors ?»\n$«Non.»\n$Le barman, découragé: $«Tu es insastisfiable !»",
    "Qu'est ce qui est petit, dangereux et dans un arbre ?\n\n$$$Une pie avec une mitrailleuse !\n\n$$--le muppet show",
)


def tell(rigolote=False):
    blague = random.choice(BLAGUES)
    for part in blague.split('$'):
        print(part, end='', flush=True)
        time.sleep(1)
    print('\n')

    if rigolote:
        print("\n({} personnes ont aimé cette blague)".format(random.randint(1000, 45000)))
