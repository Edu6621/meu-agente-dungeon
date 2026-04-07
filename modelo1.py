#Modelo 1
class Agent:

    def __init__(self):
        self.direcao = 'r' #inicializa memória 

    #Função booleana auxiliar para verificar se uma posição p está bloqueada.
    #Retorna True se p está fora do mapa ou se estiver ocupada por parede/bomba/agente 
    def tem_bloqueio(self, game_state, p):
        return not game_state.is_in_bounds(p) or game_state.entity_at(p) in ['sb','ib','ob','b',0,1]

    def next_move(self, game_state, player_state):
        ax, ay = player_state.location

        if self.direcao == 'r':
            if self.tem_bloqueio(game_state, (ax+1, ay)):
                self.direcao = 'l' #atualiza memória
        else:
            if self.tem_bloqueio(game_state, (ax-1, ay)):
                self.direcao = 'r' #atualiza memória

        return self.direcao 
