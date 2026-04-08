# Exercício C  Minerar um bloco de minério
# Crie um agente modeloC.py que faça o seguinte:
# quando ficar ao lado de um bloco de minério ob e tiver munição, ele deve memorizar a posição desse bloco
# e jogar um bomba.
# Após jogar a bomba, deve fugir por alguns turnos e retornar ao bloco para jogar outra bomba.
# Esse comportamento deve se repetir esse ciclo até jogar 3 bombas, ou até acabar a munição.
# quando não estiver executando esse plano, deve andar aleatoriamente.

#Modelo 5

import random

class Agent:

    def __init__(self):
        self.contador = 0 #inicializa memória
        self.posicao = (-1,-1) #inicializa memória

    def tem_bloqueio(self, game_state, p):
        return not game_state.is_in_bounds(p) or game_state.entity_at(p) in ['sb','ib','b',0,1]

    def next_move(self, game_state, player_state):

        ax, ay = player_state.location

        c = game_state.entity_at((ax, ay + 1))
        d = game_state.entity_at((ax + 1, ay))
        b = game_state.entity_at((ax, ay - 1))
        e = game_state.entity_at((ax - 1, ay))
        
        if c == 'ob' or d == 'ob' or b == 'ob' or e == 'ob':
                self.contador = 10 
                return 'p'

        if c == 'ob':
            self.posicao = (ax, ay + 1)
        
        if d == 'ob':
            self.posicao = (ax + 1, ay)

        if b == 'ob':
            self.posicao = (ax, ay - 1)    

        if e == 'ob':
            self.posicao = (ax - 1, ay)

        px, py = self.posicao

    # FIZ ATÉ AQUI POR QUE NÃO CONSEGUI TERMINAR... IGNORA O RESTO


        dp = abs(ax - px) + abs(ay - py) #distancia até o ponto em memória (px,py)


        
        if self.contador > 0:
            self.contador = self.contador - 1


            #Guarda ações que aumentam a distancia até o ponto (px,py)
            actions = []
            if not self.tem_bloqueio(game_state, (ax, ay+1)): #cima
                d = abs(ax - px) + abs((ay+1) - py)
                if d > dp:
                    actions.append('u')

            if not self.tem_bloqueio(game_state, (ax, ay-1)): #baixo
                d = abs(ax - px) + abs((ay-1) - py)
                if d > dp:
                    actions.append('d')

            if not self.tem_bloqueio(game_state, (ax+1, ay)): #direita
                d = abs((ax+1) - px) + abs(ay - py)
                if d > dp:
                    actions.append('r')

            if not self.tem_bloqueio(game_state, (ax-1, ay)): #esquerda
                d = abs((ax-1) - px) + abs(ay - py)
                if d > dp:
                    actions.append('l')

            #Se tem alguma ação escolhe uma aleatoriamente
            if len(actions) > 0:
                return random.choice(actions)
                
        if self.contador == 1:

        return '' #Fica parado por padrão
