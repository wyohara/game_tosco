from abc import ABC, abstractmethod
import numpy as np
import pygame

class Model_3D(ABC):
    def __init__(self,pygame:pygame, largura_tela:int, altura_tela:int):
        self.pygame = pygame
        self._faces = []
        self.arestas = []
        self.vertices = []
        self.ALTURA = altura_tela
        self.LARGURA = largura_tela
        self._linha_edge =  (255, 255, 255)

    def desenhar_cubo(self, tela, posicao_dos_vertices):
        """Desenha as faces e arestas do cubo rotacionado na tela."""
        posicao_dos_vertices = self.__centralizar_objeto(posicao_dos_vertices)


        # Desenhar as faces de trás para frente
        for _, i, face in self.__ordenar_face_por_profundidade(posicao_dos_vertices):
            # Obter os vértices da face
            pontos_da_face_3d = [posicao_dos_vertices[ponto] for ponto in face]

            # Projeção dos vértices da face
            pontos_face_projetado_2d = [self.__projetar_3d_em_2d(ponto) for ponto in pontos_da_face_3d]

            # Desenhar a face preenchida
            self.pygame.draw.polygon(tela, self.get_cores_faces()[i], pontos_face_projetado_2d)

            # Desenhar as arestas (sobrepondo a face)
            for ponto in range(len(pontos_face_projetado_2d)):
                inicio_aresta = pontos_face_projetado_2d[ponto]
                fim_aresta = pontos_face_projetado_2d[(ponto + 1) % len(pontos_face_projetado_2d)]
                self.pygame.draw.line(tela, self._linha_edge, inicio_aresta, fim_aresta, 2)

    def __ordenar_face_por_profundidade(self, posicao_vertices)->np.array:
        """Calcula a profundidade da face com base na média dos vértices projetados.
        
        """
        faces_ordenadas = []
        for i, face in enumerate(self._faces):
            profundidade = np.mean([posicao_vertices[v][2] for v in face])
            faces_ordenadas.append((profundidade, i, face))
        
        faces_ordenadas.sort(reverse=True)

        return faces_ordenadas
    
    def __projetar_3d_em_2d(self, ponto_3d, fov=256, distancia_da_visao=4):
        """Projeta as coordenadas 3D para 2D."""
        x_2d = int(ponto_3d[0] * fov / (ponto_3d[2] + distancia_da_visao) + self.LARGURA / 2)
        y_2d = int(-ponto_3d[1] * fov / (ponto_3d[2] + distancia_da_visao) + self.ALTURA / 2)
        return x_2d, y_2d
    
    def __centralizar_objeto(self, vertices):
        """Centraliza o cubo, deslocando-o para que o centro fique em (0, 0, 0)."""
        centro = np.mean(vertices, axis=0)
        # Subtrair o centro de cada vértice para centralizar o cubo
        vertices_centralizados = vertices - centro
        return vertices_centralizados
    
