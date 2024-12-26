import numpy as np
import math
from controle_3d_abs import Controle_3D_Abs

class Cubo(Controle_3D_Abs):
    def __init__(self, pygame):
        super().__init__(pygame=pygame)
        # Usar numpy array diretamente para armazenar os vértices
        self.objeto_3d.vertices = np.array([
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Frente
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]  # Trás
        ])

        self.objeto_3d.faces = np.array([
            [0, 1, 2, 3],  # Frente
            [4, 5, 6, 7],  # Trás
            [0, 1, 5, 4],  # Inferior
            [2, 3, 7, 6],  # Superior
            [0, 3, 7, 4],  # Esquerda
            [1, 2, 6, 5]   # Direita
        ])

        self.objeto_3d.arestas = np.array([
            [0, 1], [1, 2], [2, 3], [3, 0],  # Frente
            [4, 5], [5, 6], [6, 7], [7, 4],  # Traseira
            [0, 4], [1, 5], [2, 6], [3, 7]   # Conectando as faces
        ])

        self.objeto_3d.cores_faces = np.array([
            (255, 0, 0),    # Vermelho (frente)
            (0, 255, 0),    # Verde (traseira)
            (0, 0, 255),    # Azul (superior)
            (255, 255, 0),  # Amarelo (inferior)
            (255, 165, 0),  # Laranja (esquerda)
            (255, 0, 128)   # Roxo (direita)
        ])
    