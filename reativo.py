# 1 ) Ele fica congelado, porque o actions está no final do código
# e ele fica num loop apertando 'p' sem parar

#2) Fica melhor, porque isso evita loops desnecessários
# agora ele só se mexe pra um lado aleatório se estiver sem bombas

#3 ) Ele joga uma bomba do lado da madeira e dá um comando pra se mover
# pra qualquer lado

# 4 ) do jeito que eu fiz se a bomba estiver em cima ou em baixo
# ele se move pra esquerda ou direita, e vice-versa,
# ainda dá pra melhorar mas é melhor do que se fosse
# aleatório

#5 ) Sim, ele escapa porém se tiver parede ou obstáculo no caminho
# ele fica preso na parede

#6 ) essa fuga é melhor em partes, pois na que eu tinha feito
# ela não ficava congelado depois de correr da bomba, nesse
# novo ele fica congelado, mas foge de mais possiveis bombas
# e ele n considera os obstáculos
        
        # if c == 'b' or d == 'b' or b == 'b' or e == 'b':
        #     if c == 'b' or b == 'b':
        #         return random.choice(['l', 'r'])
        #     if e == 'b' or d == 'b':
        #         return random.choice(['u', 'd'])


import random

class Agent:
    def __init__(self):
        pass

    def run_bomb(self, game_state, ax, ay):
        for bomba in game_state.bombs:
            bx = bomba[0]
            by = bomba[1]
            db = abs(ax - bx) + abs(ay - by)

            if db <= 3:
                if bx > ax:
                    if game_state.entity_at((ax-1, ay)) == 'sb' or game_state.entity_at((ax-1, ay)) == 'ob' or game_state.entity_at((ax-1, ay)) == 'ib':
                        return random.choice(['u', 'd'])
                    else: return 'l'     
                if bx < ax:
                    if game_state.entity_at((ax+1, ay)) == 'sb' or game_state.entity_at((ax+1, ay)) == 'ob' or game_state.entity_at((ax+1, ay)) == 'ib':
                        return random.choice(['u', 'd'])
                    else: return 'r'     
                if by > ay:
                    if game_state.entity_at((ax, ay-1)) == 'sb' or game_state.entity_at((ax, ay-1)) == 'ob' or game_state.entity_at((ax, ay-1)) == 'ib':
                        return random.choice(['l', 'r'])
                    else: return 'd'     
                if by < ay:
                    if game_state.entity_at((ax, ay+1)) == 'sb' or game_state.entity_at((ax, ay+1)) == 'ob' or game_state.entity_at((ax, ay+1)) == 'ib':
                        return random.choice(['l', 'r'])
                    else: return 'u' 
        else: return None    

    def no_ammo_run(self, game_state, ax, ay, hx, hy, d, ammo):
        if (d < 4) and ammo == 0:
            if (hx == ax+1 or hx == ax+2 or hx == ax+3):
                return 'l'
            if (hx == ax-1 or hx == ax-2 or hx == ax-3):
                return 'r'
            if (hy == ay+1 or hy == ay+2 or hy == ay+3):
                return 'd'
            if (hy == ay-1 or hy == ay-2 or hy == ay-3):
                return 'u'
        else: return None    

    def next_move(self, game_state, player_state):

        ammo = player_state.ammo
        bombas = game_state.bombs

        # Obtém informações do sensor de posição do agente
        ax, ay = player_state.location

        # Obtém informações de sensores de posições adjacentes ao agente
        c = game_state.entity_at((ax, ay + 1)) # cima
        d = game_state.entity_at((ax + 1, ay)) # direita
        b = game_state.entity_at((ax, ay - 1)) # baixo
        e = game_state.entity_at((ax - 1, ay)) # esquerda

        oponentes = game_state.opponents(player_state.id)
        hx, hy = oponentes[0]
        d = abs(ax - hx) + abs(ay - hy)

        # Regra 1: se oponente adjacente então jogar bomba
        # 1 é player
        if (c == 1 or d == 1 or b == 1 or e == 1) and ammo > 0:
            if player_state.location in bombas:
                return random.choice(['u', 'd', 'l', 'r'])
            print("Estou jogando bomba")
            return 'p'

        #Se houver pelo menos um bloco de madeira adjacente e o agente tiver munição, então jogar
        #bomba para explodir.
        if (c == 'sb' or d == 'sb' or b == 'sb' or e == 'sb') and ammo > 0:
            if player_state.location in bombas:
                return random.choice(['u', 'd', 'l', 'r'])
            print("Explodir madeira")
            return 'p'
        #atv 4/6 Se tiver bomba adjacente, sair 
        correr_bomba = self.run_bomb(game_state, ax, ay) 
        if correr_bomba:
            return correr_bomba
        
        #atv 5 Se tiver sem bomba, fugir do inimigo
        #correr_sem_ammo = self.no_ammo_run(self, game_state, ax, ay, hx, hy, d, ammo)
        #if correr_sem_ammo:
        #    return correr_sem_ammo



        # Regra 2: se houver tesouro adjacente então coletar
        if c == 't' or d == 't' or b == 't' or e == 't':
            print("Estou coletando um tesouro")
            if c == 't': return 'u'
            if d == 't': return 'r'
            if b == 't': return 'd'
            if e == 't': return 'l'

        # Regra 3: se houver munição adjacente então aproximar
        if c == 'a' or d == 'a' or b == 'a' or e == 'a':
            print("Estou coletando munição")
            if c == 'a': return 'u'
            if d == 'a': return 'r'
            if b == 'a': return 'd'
            if e == 'a': return 'l'

        # Regra padrão: mover aleatoriamente

        return random.choice(['u', 'd', 'l', 'r'])
