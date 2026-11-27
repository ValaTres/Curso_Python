import turtle #desenhar a tela - trabalhar com formas
import random 
import time #sabe horario dia e coisas do tipo

tela = turtle.Screen()
tela.title("Jogo da Cobrinha")

pontos = 0

tela.bgcolor("black")
tela.setup(width=600, height=600)

tela.tracer(0)

cobra = turtle.Turtle() #jogador
cobra.speed(0)
cobra.shape("square")
cobra.color("violet")
cobra.penup() #impede traço
cobra.goto(0,0)
cobra.direction = 'stop'

fruta = turtle.Turtle()
fruta.speed(0)
fruta.shape('circle')
fruta.color('green')
fruta.penup()
fruta.goto(0,100)

corpo = []

def cima():
    cobra.direction = 'up'
def baixo():
    cobra.direction = 'down'
def direita():
    cobra.direction = 'right'
def esquerda():
    cobra.direction = 'left'

# comandos do teclado

tela.listen()
tela.onkeypress(cima, 'Up')
tela.onkeypress(baixo, 'Down')
tela.onkeypress(esquerda, 'Left')
tela.onkeypress(direita, 'Right')

while True:
    tela.update()
    
    if cobra.distance(fruta) <20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        fruta.goto(x, y)
        pontos += 10 # Soma de pontos
        
        novo_pedaco = turtle.Turtle() #Aumenta corpo
        novo_pedaco.speed(0)
        novo_pedaco.shape('square')######
        novo_pedaco.color('purple')
        novo_pedaco.color()
        corpo.append(novo_pedaco)
        
        tela.title(f"Pontos: {str(pontos)}")
    time.sleep(0.1)
    
    if cobra.direction == 'left':
        x = cobra.xcor()
        cobra.setx(x - 20)    
    elif cobra.direction == 'right':
        x = cobra.xcor()
        cobra.setx(x + 20)
    elif cobra.direction == 'up':
        y = cobra.ycor()
        cobra.sety(y + 20)
    elif cobra.direction == 'down':
        y = cobra.ycor()
        cobra.sety(y - 20)
        
    for i in range(len(corpo)-1, 0, -1):
#inicio do laço que percorre os pedaços do corpo. Esse -1 começa pelo ultimo pedaço do corpo
#e esse 0 define que o laço FOR vai até o primeiro pedaço, sem incluir ele
#o outro -1 faz o contador diminuir de 1 em 1 de trás pra frente
        x = corpo[i - 1].xcor()
        y = corpo[i - 1].ycor()
        corpo[i].goto(x, y)
        
        if len(corpo) > 0:
            x = cobra.xcor()
            y = cobra.ycor()
            corpo[0].goto(x, y)
        
    if cobra.xcor() > 290 or cobra.xcor() < -290 or cobra.ycor() > 290 or cobra.ycor() < -290:
        tela.title(f'GAME OVER! Pontuação final:{str(pontos)}')
        cobra.goto(0.0)
        cobra.direction = "stop"
        break
tela.mainloop()
    
