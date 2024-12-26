import pygame
import sys
from cubo import Cubo

class Engine:
    def __init__(self, width=1366, height=720, fps=60):
        """
        Modulo inicial da engine do pygame

        Parameters:
        width (int, opcional): a largura da tela
        height (int, opcional): a altura da tela
        fps(int opcional): a taxa de atualização da tela
        """
        self.SCREEN_WIDTH = int(width)
        self.SCREEN_HEIGHT = int(height)
        self.FPS = int(fps)
        self.CAPTION = "Engine em pygame"
        self.BACKGROUND_COLOR = (0, 0, 0)
        self.screen = None

    def iniciar(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(self.CAPTION)
        pygame_clock = pygame.time.Clock()

        # Instanciando o cubo uma vez fora do loop
        cubo = Cubo(pygame=pygame)
        angulo_x, angulo_y, angulo_z = 0.0, 0.0, 0.0

        while True:
            # Processando eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Preenchendo a tela com a cor de fundo
            self.screen.fill(self.BACKGROUND_COLOR)

            # Desenhando o cubo
            cubo.controlar_objeto_3d()

            # Atualizando a tela
            pygame.display.flip()

            # Controlando a taxa de quadros
            pygame_clock.tick(self.FPS)

if __name__ == "__main__":
    Engine().iniciar()