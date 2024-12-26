import numpy as np
import pygame

class Objeto_3D:
    def __init__(self, pygame: pygame):
        """
        Inicializa o objeto 3D (como um cubo) e define as propriedades necessárias para sua renderização.
        
        :param pygame: Instância do pygame para renderização.
        """
        self.faces: np.array = np.array([])  # Faces do objeto 3D
        self.arestas: np.array = np.array([])  # Arestas do objeto 3D
        self.vertices: np.array = np.array([])  # Vértices do objeto 3D
        self.cores_faces: np.array = np.array([])  # Cores para as faces
        self.cor_aresta = (255, 255, 255)  # Cor da aresta (branco)
        self.pygame = pygame  # Referência do pygame
        self.angulo_visao = (0.0, 0.0, 0.0)  # Ângulos de visão (X, Y, Z)
        self.largura = pygame.display.get_surface().get_size()[0]  # Largura da tela
        self.altura = pygame.display.get_surface().get_size()[1]  # Altura da tela

    def set_vertices(self, novos_vertices):
        """
        Define os vértices do objeto 3D.

        :param novos_vertices: Lista de novos vértices para o objeto.
        """
        self.vertices = np.array(novos_vertices)
    
    def desenhar_objeto(self, posicao_dos_vertices):
        """
        Desenha as faces e arestas do objeto 3D na tela.

        :param posicao_dos_vertices: Vértices do objeto após transformação (como rotação).
        """
        posicao_dos_vertices = self.__centralizar_objeto(posicao_dos_vertices)

        # Desenhar as faces de trás para frente, para garantir a ordem de sobreposição
        for _, i, face in self.__ordenar_face_por_profundidade(posicao_dos_vertices):
            # Obter os vértices da face
            pontos_da_face_3d = [posicao_dos_vertices[ponto] for ponto in face]

            # Projeção dos vértices da face para 2D
            pontos_face_projetado_2d = [self.__projetar_3d_em_2d(ponto) for ponto in pontos_da_face_3d]

            # Desenhar a face preenchida
            self.pygame.draw.polygon(self.pygame.display.get_surface(), self.cores_faces[i], pontos_face_projetado_2d)

            # Desenhar as arestas sobrepondo as faces
            for ponto in range(len(pontos_face_projetado_2d)):
                inicio_aresta = pontos_face_projetado_2d[ponto]
                fim_aresta = pontos_face_projetado_2d[(ponto + 1) % len(pontos_face_projetado_2d)]
                self.pygame.draw.line(self.pygame.display.get_surface(), self.cor_aresta, inicio_aresta, fim_aresta, 2)
    
    def rotacionar(self, angulo: tuple) -> np.array:
        """
        Aplica uma rotação 3D nos vértices do objeto em torno dos eixos X, Y e Z.

        :param angulo: Tupla contendo os ângulos de rotação nos eixos (X, Y, Z).
        :return: Vértices rotacionados.
        """
        # Matrizes de rotação para cada eixo
        rot_x = np.array([
            [1, 0, 0],
            [0, np.cos(angulo[0]), -np.sin(angulo[0])],
            [0, np.sin(angulo[0]), np.cos(angulo[0])]
        ])
        
        rot_y = np.array([
            [np.cos(angulo[1]), 0, np.sin(angulo[1])],
            [0, 1, 0],
            [-np.sin(angulo[1]), 0, np.cos(angulo[1])]
        ])
        
        rot_z = np.array([
            [np.cos(angulo[2]), -np.sin(angulo[2]), 0],
            [np.sin(angulo[2]), np.cos(angulo[2]), 0],
            [0, 0, 1]
        ])
        
        # Aplicando as rotações nos vértices
        rotated_vertices = np.dot(self.vertices, rot_x)  # Rotação no eixo X
        rotated_vertices = np.dot(rotated_vertices, rot_y)  # Rotação no eixo Y
        rotated_vertices = np.dot(rotated_vertices, rot_z)  # Rotação no eixo Z

        return np.round(rotated_vertices, 3)  # Arredonda os resultados para 3 casas decimais
    
    def atualizar_angulo_de_visao(self, incremento_x=0.01, incremento_y=0.01, incremento_z=0.01):
        """
        Atualiza os ângulos de rotação do objeto.

        :param incremento_x: Incremento do ângulo de rotação no eixo X.
        :param incremento_y: Incremento do ângulo de rotação no eixo Y.
        :param incremento_z: Incremento do ângulo de rotação no eixo Z.
        """
        x, y, z = self.angulo_visao
        self.angulo_visao = np.round((x + incremento_x, y + incremento_y, z + incremento_z), 3)
    
    def __ordenar_face_por_profundidade(self, posicao_vertices) -> np.array:
        """
        Ordena as faces do objeto 3D pela profundidade média dos seus vértices, do mais distante para o mais próximo.
        
        :param posicao_vertices: Vértices transformados do objeto.
        :return: Lista de faces ordenadas pela profundidade.
        """
        faces_ordenadas = []
        for i, face in enumerate(self.faces):
            profundidade = np.round(np.mean([posicao_vertices[v][2] for v in face]), 5)
            faces_ordenadas.append((profundidade, i, face))
        
        faces_ordenadas.sort(reverse=True)  # Ordenação decrescente pela profundidade

        return faces_ordenadas    
    
    def __projetar_3d_em_2d(self, ponto_3d, fov=256, distancia_da_visao=4) -> tuple:
        """
        Projeta um ponto 3D para as coordenadas 2D da tela.

        :param ponto_3d: Coordenadas 3D do ponto a ser projetado.
        :param fov: Fator de escala da projeção (Field of View).
        :param distancia_da_visao: Distância da visão para o cálculo da perspectiva.
        :return: Coordenadas 2D do ponto projetado.
        """
        x_2d = int(ponto_3d[0] * fov / (ponto_3d[2] + distancia_da_visao) + self.largura / 2)
        y_2d = int(-ponto_3d[1] * fov / (ponto_3d[2] + distancia_da_visao) + self.altura / 2)
        return x_2d, y_2d
    
    def __centralizar_objeto(self, vertices) -> np.array:
        """
        Centraliza os vértices do objeto, deslocando-os para que o centro do objeto esteja na origem (0, 0, 0).
        
        :param vertices: Vértices do objeto a serem centralizados.
        :return: Vértices centralizados.
        """
        centro = np.mean(vertices, axis=0)
        vertices_centralizados = vertices - centro  # Subtrai o centro de cada vértice
        return np.round(vertices_centralizados, 3)  # Arredonda para 3 casas decimais
    

