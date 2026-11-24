#  ________  ________  ___  ___      ___ ___  ________   ___  ___  ________     
# |\   __  \|\   ___ \|\  \|\  \    /  /|\  \|\   ___  \|\  \|\  \|\   __  \    
# \ \  \|\  \ \  \_|\ \ \  \ \  \  /  / | \  \ \  \\ \  \ \  \\\  \ \  \|\  \   
#  \ \   __  \ \  \ \\ \ \  \ \  \/  / / \ \  \ \  \\ \  \ \   __  \ \   __  \  
#   \ \  \ \  \ \  \_\\ \ \  \ \    / /   \ \  \ \  \\ \  \ \  \ \  \ \  \ \  \ 
#    \ \__\ \__\ \_______\ \__\ \__/ /     \ \__\ \__\\ \__\ \__\ \__\ \__\ \__\
#     \|__|\|__|\|_______|\|__|\|__|/       \|__|\|__| \|__|\|__|\|__|\|__|\|__|
#                                                                                                                                                    
#  ________  ________  _____ ______   _______                                   
# |\   ____\|\   __  \|\   _ \  _   \|\  ___ \                                  
# \ \  \___|\ \  \|\  \ \  \\\__\ \  \ \   __/|                                 
#  \ \  \  __\ \   __  \ \  \\|__| \  \ \  \_|/__                               
#   \ \  \|\  \ \  \ \  \ \  \    \ \  \ \  \_|\ \                              
#    \ \_______\ \__\ \__\ \__\    \ \__\ \_______\                             
#     \|_______|\|__|\|__|\|__|     \|__|\|_______|                             
#
#
# AUTOR: Lucas de Sousa Ferreira
# VERSÃO: 1.0
# LICENÇA: OPEN SOURCE
from random import randint

random = randint(1,100)
chute = 0
chances = 10

while chute != random :
    chute = input('Chute um número de 0 a 100: ')
    if chute.isnumeric() :
        chute = int(chute)
        chances = chances - 1
        if chute == random :
            print('')
            print('Parabéns! Você venceu! O número era {} e você ainda tinha {} chances'.format(random,chances))
            print('')
            break
        else :
            print('')
            if  chute > random :
                print('Voce errou! Dica: É um número menor.')
            else :
                print('Voce errou! Dica: É um número maior.')
            print('Você ainda possui {} chances.'.format(chances))
            print('')
        if chances == 0 :
            print('')
            print('Suas chances acabaram, você perdeu! O número era {}'.format(random))
            print('')
            break
print('Game Over')