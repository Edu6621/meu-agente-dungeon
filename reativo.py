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



import random

class Agent:
    def __init__(self):
        pass

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



        #atv 4 Se tiver bomba adjacente, sair
        if c == 'b' or d == 'b' or b == 'b' or e == 'b':
            if c == 'b' or b == 'b':
                return random.choice(['l', 'r'])
            if e == 'b' or d == 'b':
                return random.choice(['u', 'd'])

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
