import numpy as np
import math
from model_3d import Model_3D

class Cubo(Model_3D):
    def __init__(self, pygame, largura_tela, altura_tela):
        super().__init__(pygame=pygame, largura_tela=largura_tela, altura_tela=altura_tela)
        # Usar numpy array diretamente para armazenar os vértices
        self._vertices = np.array([
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Frente
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]  # Trás
        ])

        self._faces = [
            [0, 1, 2, 3],  # Frente
            [4, 5, 6, 7],  # Trás
            [0, 1, 5, 4],  # Inferior
            [2, 3, 7, 6],  # Superior
            [0, 3, 7, 4],  # Esquerda
            [1, 2, 6, 5]   # Direita
        ]
        self.arestas =  [
            [0, 1], [1, 2], [2, 3], [3, 0],  # Frente
            [4, 5], [5, 6], [6, 7], [7, 4],  # Traseira
            [0, 4], [1, 5], [2, 6], [3, 7]   # Conectando as faces
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
    
    def set_vertice(self, novos_vertices):
        self._vertices = np.array(novos_vertices)
    
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
    
        # Aplicando as rotações sucessivas nos 3 eixos (X, Y, Z)
        rotated_vertices = np.dot(self._vertices, rot_x)  # Rotaciona no eixo X
        rotated_vertices = np.dot(rotated_vertices, rot_y)  # Rotaciona no eixo Y
        rotated_vertices = np.dot(rotated_vertices, rot_z)  # Rotaciona no eixo Z

        return rotated_vertices
    

    def atualizar_angulo_rotacao(self, angulo_x, angulo_y, angulo_z, incremento=0.01):
        """Atualiza os ângulos de rotação."""
        return angulo_x + incremento, angulo_y + incremento, angulo_z + incremento
    

