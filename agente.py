import random

class Agent:
    def __init__(self):
        pass

    def next_move(self, game_state, player_state):
        print("Pensando...")
        actions = ['u', 'd', 'l', 'r',]
        action = random.choice(actions)

        #Num de turnos :
        print("Ação:", action)

        #Posição dos tesouros :
        print ("Tesouros:", game_state.treasure)

        #Detectando oponente
        oponentes = game_state.opponents(player_state.id)
        print("Oponentes:", oponentes)

        hx, hy = oponentes[0]
        print("Primeiro oponente:", hx, hy)

        #Mostrar coordenadas da bomba no mapa
        bombas = game_state.bombs
        print("Lista de coordenadas das bombas no mapa : ", bombas)

        #Printar posição do agente, hp, ammo
        ax, ay = player_state.location
        print("Posição do agente:", ax, ay)

        vidas = player_state.hp
        print("Vidas:", vidas)

        ammo = player_state.ammo
        print("Munição:", ammo)

        #Distância do Inimigo
        d = abs(ax-hx) + abs(ay-hy)
        print("Distância do inimigo", d)

        if d == 1:
            action  = 'p'
        return action