#Modelo 4

import random

class Agent:

    def __init__(self):
        self.posicao = (-1,-1) #inicializa memória 

    #Função booleana auxiliar para verificar se uma posição p está bloqueada.
    #Retorna True se p está fora do mapa ou se estiver ocupada por parede/bomba/agente
    def tem_bloqueio(self, game_state, p):
        return not game_state.is_in_bounds(p) or game_state.entity_at(p) in ['sb','ib','ob','b',0,1]

    def next_move(self, game_state, player_state):

        #Posição do agente
        ax, ay = player_state.location

        #Posição do oponente
        oponentes = game_state.opponents(player_state.id)
        hx, hy = oponentes[0] #Obtém a posição do oponente
        
        #Compara a posição do humano com a posição em memória
        if (hx, hy) == self.posicao:
            return '' #fica parado

        self.posicao = (hx, hy) #Atualiza memória

        #Preenche a lista actions com ações possíveis ao redor do agente
        actions = [] 
        if not self.tem_bloqueio(game_state, (ax, ay+1)): #cima
            actions.append('u')
        if not self.tem_bloqueio(game_state, (ax, ay-1)): #baixo
            actions.append('d')
        if not self.tem_bloqueio(game_state, (ax+1, ay)): #direita
            actions.append('r')
        if not self.tem_bloqueio(game_state, (ax-1, ay)): #esquerda
            actions.append('l')

        if len(actions)==0:
            return '' #fica parado

        return random.choice(actions) #Retorna um movimento aleatório entre os possíveis
        
