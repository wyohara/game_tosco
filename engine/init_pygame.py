import pygame
import math

# Inicializa o Pygame
pygame.init()

# Definindo o tamanho da janela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Cubo 3D Girando')

# Definindo as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definindo as coordenadas dos vértices do cubo
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

# Conectando os vértices para formar as arestas do cubo
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Função para projetar um ponto 3D em 2D
def project_3d_to_2d(x, y, z, width, height, fov, viewer_distance):
    factor = fov / (viewer_distance + z)
    x_2d = int(x * factor + width / 2)
    y_2d = int(-y * factor + height / 2)
    return x_2d, y_2d

# Função para rotacionar o cubo em torno do eixo Y
def rotate_y(angle, vertex):
    x, y, z = vertex
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    x_new = cos_angle * x - sin_angle * z
    z_new = sin_angle * x + cos_angle * z
    return [x_new, y, z_new]

# Função para rotacionar o cubo em torno do eixo X
def rotate_x(angle, vertex):
    x, y, z = vertex
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    y_new = cos_angle * y - sin_angle * z
    z_new = sin_angle * y + cos_angle * z
    return [x, y_new, z_new]

# Definindo a posição do cubo e a distância do espectador
fov = 256  # Campo de visão
viewer_distance = 4  # Distância do espectador

# Loop principal
running = True
clock = pygame.time.Clock()
angle_y = 0
angle_x = 0

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotacionando o cubo ao longo dos eixos X e Y
    rotated_vertices = []
    for vertex in vertices:
        rotated_vertex = rotate_y(angle_y, vertex)
        rotated_vertex = rotate_x(angle_x, rotated_vertex)
        rotated_vertices.append(rotated_vertex)

    # Desenhando as arestas do cubo
    for edge in edges:
        start_vertex = rotated_vertices[edge[0]]
        end_vertex = rotated_vertices[edge[1]]
        
        start_2d = project_3d_to_2d(start_vertex[0], start_vertex[1], start_vertex[2], screen_width, screen_height, fov, viewer_distance)
        end_2d = project_3d_to_2d(end_vertex[0], end_vertex[1], end_vertex[2], screen_width, screen_height, fov, viewer_distance)

        pygame.draw.line(screen, WHITE, start_2d, end_2d, 2)

    # Atualizando os ângulos para a próxima rotação
    angle_y += 0.02
    angle_x += 0.02

    # Atualizando a tela
    pygame.display.flip()

    # Limitando a taxa de quadros
    clock.tick(60)

# Finalizando o Pygame
pygame.quit()
