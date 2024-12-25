import numpy as np
import math

class Cubo:
    def __init__(self, LARGURA, ALTURA):
        self.LARGURA = LARGURA
        self.ALTURA = ALTURA
        # Usar numpy array diretamente para armazenar os vértices
        self.vertices = np.array([
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Frente
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]  # Trás
        ])
    
    def get_faces(self):
        return [
            [0, 1, 2, 3],  # Frente
            [4, 5, 6, 7],  # Trás
            [0, 1, 5, 4],  # Inferior
            [2, 3, 7, 6],  # Superior
            [0, 3, 7, 4],  # Esquerda
            [1, 2, 6, 5]   # Direita
        ]
    
    def get_cores_faces(self):
        return [
            (255, 0, 0),    # Vermelho (frente)
            (0, 255, 0),    # Verde (traseira)
            (0, 0, 255),    # Azul (superior)
            (255, 255, 0),  # Amarelo (inferior)
            (255, 165, 0),  # Laranja (esquerda)
            (255, 0, 128)   # Roxo (direita)
        ]
    
    def get_vertice(self):
        return self.vertices
    
    def set_vertice(self, novos_vertices):
        self.vertices = np.array(novos_vertices)

    def get_aresta(self):
        return [
            [0, 1], [1, 2], [2, 3], [3, 0],  # Frente
            [4, 5], [5, 6], [6, 7], [7, 4],  # Traseira
            [0, 4], [1, 5], [2, 6], [3, 7]   # Conectando as faces
        ]
    
    def projetar(self, v, largura, altura, fov=256, viewer_distance=4):
        """Projeta as coordenadas 3D para 2D."""
        x = int(v[0] * fov / (v[2] + viewer_distance) + largura / 2)
        y = int(-v[1] * fov / (v[2] + viewer_distance) + altura / 2)
        return x, y
    
    def rotacionar(self, angulo_x, angulo_y, angulo_z):
        """Rotaciona um ponto 3D em torno dos eixos X, Y e Z."""
        # Matriz de rotação no eixo X
        rot_x = np.array([
        [1, 0, 0],
        [0, np.cos(angulo_x), -np.sin(angulo_x)],
        [0, np.sin(angulo_x), np.cos(angulo_x)]
    ])
    
        # Matriz de rotação no eixo Y
        rot_y = np.array([
        [np.cos(angulo_y), 0, np.sin(angulo_y)],
        [0, 1, 0],
        [-np.sin(angulo_y), 0, np.cos(angulo_y)]
    ])
    
    # Matriz de rotação no eixo Z
        rot_z = np.array([
        [np.cos(angulo_z), -np.sin(angulo_z), 0],
        [np.sin(angulo_z), np.cos(angulo_z), 0],
        [0, 0, 1]
    ])
    
        # Obtendo o vértice atual do objeto
        vertice = self.get_vertice()  # Assumindo que 'get_vertice' é um método que retorna os vértices atuais

        # Aplicando as rotações sucessivas nos 3 eixos (X, Y, Z)
        rotated_vertices = np.dot(vertice, rot_x)  # Rotaciona no eixo X
        rotated_vertices = np.dot(rotated_vertices, rot_y)  # Rotaciona no eixo Y
        rotated_vertices = np.dot(rotated_vertices, rot_z)  # Rotaciona no eixo Z

        return rotated_vertices
    
    def desenhar_cubo(self, tela, vertices_rotacionados, pygame):
        """Desenha as faces e arestas do cubo rotacionado na tela."""
        faces_ordenadas = []

        # Ordenar as faces com base na profundidade (do fundo para a frente)
        for i, face in enumerate(self.get_faces()):
            profundidade = self.calcular_profundidade(vertices_rotacionados, face)
            faces_ordenadas.append((profundidade, i, face))
        
        faces_ordenadas.sort(reverse=True)  # Ordenar pela profundidade (maior profundidade primeiro)

        # Desenhar as faces de trás para frente
        for _, i, face in faces_ordenadas:
            # Obter os vértices da face
            vertices_face = [vertices_rotacionados[v] for v in face]

            # Projeção dos vértices da face
            pontos_face = [self.projetar(v, self.LARGURA, self.ALTURA) for v in vertices_face]

            # Desenhar a face preenchida
            pygame.draw.polygon(tela, self.get_cores_faces()[i], pontos_face)

            # Desenhar as arestas (sobrepondo a face)
            for j in range(len(pontos_face)):
                ponto1 = pontos_face[j]
                ponto2 = pontos_face[(j + 1) % len(pontos_face)]
                pygame.draw.line(tela, (255, 255, 255), ponto1, ponto2, 2)

    def atualizar_angulo_rotacao(self, angulo_x, angulo_y, angulo_z, incremento=0.01):
        """Atualiza os ângulos de rotação."""
        return angulo_x + incremento, angulo_y + incremento, angulo_z + incremento
    
    def calcular_profundidade(self, vertices_rotacionados, face):
        """Calcula a profundidade da face com base na média dos vértices projetados."""
        profundidade = np.mean([vertices_rotacionados[v][2] for v in face])
        return profundidade
    
    def get_centro(self, vertices):
        """Centraliza o cubo, deslocando-o para que o centro fique em (0, 0, 0)."""
        centro = np.mean(vertices, axis=0)
        # Subtrair o centro de cada vértice para centralizar o cubo
        vertices_centralizados = vertices - centro
        return vertices_centralizados
