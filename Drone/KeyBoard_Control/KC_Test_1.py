"""
This code was developed by:
    - Miguel Meireles Teixeira, nº 2021217493
    - Damir Ferreira Baspayev Marques, nº 2021218858

Objective: Print keyboard pressed keys.
           
This code is available on Github: https://github.com/miguel-mmt2/PL5_Team_1_Repository
"""

# Import all the required libraries
import pygame
import sys

# Pygame incialization
try:
    pygame.init()
except pygame.error:
    print("Error initializing pygame.")
    print("Make sure you imported all the required libraries.")
    print("Quitting...")
    sys.exit()

# Pygame display configuration
Pygame_Display_Width = int(input("Width: "))
Pygame_Display_Lenght = int(input("Lengt: "))

Display = pygame.display.set_mode((Pygame_Display_Width, Pygame_Display_Lenght))
pygame.display.set_caption("Keyboard Control Test 1")

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_w or evento.key == pygame.K_UP:
                print("Go Forward")
            elif evento.key == pygame.K_a or evento.key == pygame.K_LEFT:
                print("Turn Left")
            elif evento.key == pygame.K_s or evento.key == pygame.K_DOWN:
                print("Go Backward")
            elif evento.key == pygame.K_d or evento.key == pygame.K_RIGHT:
                print("Turn Right")

    # Limpa a tela
    Display.fill((0, 0, 0))
    pygame.display.flip()
