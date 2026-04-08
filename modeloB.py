import random

class Agent:

    def __init__(self):
        self.contador = 0
        self.posicao = (-1,-1)

    def tem_bloqueio(self, game_state, p):
        return not game_state.is_in_bounds(p) or game_state.entity_at(p) in ['sb','ib','ob','b',0,1]

    def next_move(self, game_state, player_state):
        ax, ay = player_state.location
        
        c = game_state.entity_at((ax, ay + 1))
        d = game_state.entity_at((ax + 1, ay))
        b = game_state.entity_at((ax, ay - 1))
        e = game_state.entity_at((ax - 1, ay))
        p = game_state.entity_at((ax, ay))
        
        if c == 'b' or d == 'b' or b == 'b' or e == 'b' or p == 'b': 
            if game_state.bombs:
                self.posicao = game_state.bombs[0] 
                self.contador = 10 

        if self.contador > 0:
            self.contador = self.contador - 1 

            actions = []
            if not self.tem_bloqueio(game_state, (ax, ay+1)): 
                dist = abs(ax - self.posicao[0]) + abs((ay+1) - self.posicao[1])
                actions.append('u')

            if not self.tem_bloqueio(game_state, (ax, ay-1)): 
                dist = abs(ax - self.posicao[0]) + abs((ay-1) - self.posicao[1])
                actions.append('d')

            if not self.tem_bloqueio(game_state, (ax+1, ay)): 
                dist = abs((ax+1) - self.posicao[0]) + abs(ay - self.posicao[1])
                actions.append('r')

            if not self.tem_bloqueio(game_state, (ax-1, ay)): 
                dist = abs((ax-1) - self.posicao[0]) + abs(ay - self.posicao[1])
                actions.append('l')

            if len(actions) > 0:
                return random.choice(actions)

        return random.choice(['u', 'd', 'l', 'r'])