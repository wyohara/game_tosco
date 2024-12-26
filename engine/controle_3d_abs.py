from abc import ABC
import pygame
from objeto_3d import Objeto_3D

class Controle_3D_Abs(ABC):
    """
    Classe base para modelos 3D. Gerencia a criação, rotação e desenho de objetos 3D.
    Esta classe é uma abstração e deve ser extendida para implementar funcionalidades adicionais.

    :param pygame: Instância do Pygame utilizada para renderização.
    """
    def __init__(self, pygame: pygame):
        """
        Inicializa o modelo 3D e o objeto 3D.

        :param pygame: Instância do Pygame utilizada para renderização.
        """
        self.pygame = pygame
        self.objeto_3d: Objeto_3D = Objeto_3D(pygame)  # Criação do objeto 3D
        self.largura, self.altura = pygame.display.get_surface().get_size()  # Largura e altura da tela

    def controlar_objeto_3d(self):
        """
        Controla o objeto 3D: realiza a rotação e o desenho das faces e arestas.

        Este método realiza a rotação do objeto 3D, atualiza seus ângulos de rotação
        e desenha as faces e arestas na tela.
        """
        # Realiza a rotação do objeto com base nos ângulos de visão atuais
        posicao_dos_vertices = self.objeto_3d.rotacionar(self.objeto_3d.angulo_visao)

        # Desenha o objeto 3D com os vértices rotacionados
        self.objeto_3d.desenhar_objeto(posicao_dos_vertices)

        # Atualiza os ângulos de rotação do objeto 3D
        self.objeto_3d.atualizar_angulo_de_visao()
