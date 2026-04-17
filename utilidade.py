#Agente baseado em Utilidade

import random


class Agent:

    #Construtor da classe: serve para inicializar variáveis de estado interno
    def __init__(self):
        pass

    #Função booleana auxiliar para verificar se uma posição p está bloqueada.
    #Retorna True se p está fora do mapa ou se estiver ocupada por parede/bomba/agente
    def tem_bloqueio(self, game_state, p):
        return not game_state.is_in_bounds(p) or game_state.entity_at(p) in ['sb','ib','ob','b',0,1]

    #Retorna a distância de Manhattan entre os pontos p1 e p2. 
    def distancia(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    #Retorna uma tupla (d,tx,ty) sendo a distancia do tesouro mais próximo e suas coordenadas.
    #Retorna 1000 na distância caso não existam tesouros.
    def tesouro_proximo(self, ax, ay, game_state):
        d = 1000 #começa com um valor "infinito" 
        tx = -1
        ty = -1

        for tesouro_x, tesouro_y in game_state.treasure:
            dist = self.distancia((ax,ay),(tesouro_x, tesouro_y)) #distancia do tesouro até o agente
            if dist < d:
               d = dist
               tx = tesouro_x
               ty = tesouro_y

        return d, tx, ty

    #Retorna uma tupla (d,mx,my) sendo a distancia da municao mais próxima e suas coordenadas.
    #Retorna 1000 na distância caso não existam munições.
    def municao_proxima(self, ax, ay, game_state):
        d = 1000 #começa com um valor "infinito" 
        mx = -1
        my = -1

        for municao_x, municao_y in game_state.ammo:
            dist = self.distancia((ax,ay),(municao_x, municao_y)) #distancia da municao até o agente
            if dist < d:
               d = dist
               mx = municao_x
               my = municao_y

        return d, mx, my

    #Retorna uma tupla (d,tx,ty) sendo a distancia da bomba mais próxima e suas posição.
    #Retorna 1000 na distância caso não existam bombas.
    def bomba_proxima(self, ax, ay, game_state):
        d = 1000 #começa com um valor "infinito" 
        bx = -1
        by = -1

        for bomba_x, bomba_y in game_state.bombs:
            dist = self.distancia((ax,ay),(bomba_x, bomba_y)) #distancia da bomba até o agente
            if dist < d:
               d = dist
               bx = bomba_x
               by = bomba_y

        return d, bx, by

    #Retorna verdadeiro se o ponto (x,y) é uma posição livre no mapa.
    #Para ser considerada livre a posição deve estar dentro dos limites
    #do mapa e não deve conter nenhum objeto indicado na lista "ocupados"
    #Por padrão, ocupados são apenas blocos de madeira, minério e indestrutível
    def posicao_livre(self, x, y, game_state, ocupados = ['sb','ob','ib','b']):
        b = game_state.is_in_bounds((x, y))
        e = game_state.entity_at((x,y)) 
        return (b and e not in ocupados)

    #Retorna uma lista com as posicões livres adjacentes a (ex,ey)     
    def vizinhanca_livre(self, ex, ey, game_state, ocupados = ['sb','ob','ib','b']):
        vizinhos = []
        #Coordenadas de   cima,      baixo,   esquerda,   direita
        posicoes = [(ex, ey-1), (ex, ey+1), (ex-1, ey), (ex+1, ey)]
        for px, py in posicoes:
            if self.posicao_livre(px, py, game_state, ocupados):
               vizinhos.append((px,py))
        return vizinhos
   
    #Função principal do jogo: deve retornar uma das ações abaixo:
    # 'u' = Andar para cima     
    # 'r' = Andar para direita  
    # 'd' = Andar para baixo    
    # 'l' = Andar para esquerda 
    # 'p' = Jogar bomba         
    # ''  = Ficar parado           
    def next_move(self, game_state, player_state):

        # SENSORES ========================================================
        ax, ay = player_state.location
        hx, hy = game_state.opponents(player_state.id)[0]
        vida = player_state.hp
        municao = player_state.ammo
        distancia_humano = self.distancia((ax, ay), (hx, hy)) 
        distancia_bomba, bx, by = self.bomba_proxima(ax, ay, game_state)
        distancia_tesouro, tx, ty = self.tesouro_proximo(ax, ay, game_state)
        distancia_municao, mx, my = self.municao_proxima(ax, ay, game_state)
        saidas = len(self.vizinhanca_livre(ax, ay, game_state))

        print("Sensores atuais:")
        print("agente:", (ax, ay), "oponente:", (hx, hy))
        print("vida:", vida, "municao:", municao)
        print("distancia_humano:", distancia_humano)
        print("distancia_bomba:", distancia_bomba, "bomba:", (bx, by))
        print("distancia_tesouro:", distancia_tesouro, "tesouro:", (tx, ty))
        print("distancia_municao:", distancia_municao, "municao_pos:", (mx, my))
        print("saidas:", saidas)


        # AVALIAÇÃO DAS AÇÕES ============================================
        avaliacoes = []
        adjacentes = {'u': (ax,ay+1), 'r': (ax+1,ay), 'd': (ax,ay-1), 'l':(ax-1,ay), '':(ax,ay)}

        for action, p in adjacentes.items():
           px, py = p

           if action != '' and self.tem_bloqueio(game_state, (px, py)):
               u = -1000
               print("acao:", action, "bloqueada", "u:", u)
               avaliacoes.append((u, action))
               continue

           b, bx, by = self.bomba_proxima(px, py, game_state)
           t, tx, ty = self.tesouro_proximo(px, py, game_state)
           m, mx, my = self.municao_proxima(px, py, game_state)
           h = self.distancia((px, py), (hx, hy))
           s = len(self.vizinhanca_livre(px, py, game_state))

           u = b - t #ALTERE AQUI

           print("acao:", action, "b:", b, "t:", t, "m:", m, "h:", h, "s:", s, "u:", u)
           avaliacoes.append((u, action))


        # ESCOLHA DA AÇÃO ================================================
        melhor_u = max(u for u, action in avaliacoes)
        melhores = [action for u, action in avaliacoes if u == melhor_u]
        if len(melhores) == 0:
            return ''
        return random.choice(melhores)
