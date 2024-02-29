"""
This code was developed by:
    - Miguel Meireles Teixeira, nº 2021217493
    - Damir Ferreira Baspayev Marques, nº 2021218858

Objective: Using pygame library the user can input the direction of the drone.
 
This code is available on Github: https://github.com/miguel-mmt2/PL5_Team_1_Repository
"""

# Import all the required libraries
import pygame
import sys
import djitellopy as tello
import time


drone = tello.Tello()

# Connecting to DJI Tello Drone
try:
    drone.connect()
    print("Connected to drone.")
except:
    print("Error connecting to drone.")
    print("Make sure you are on the same network as the drone.")
    print("Quitting...")
    

# Checking DJI Tello Drone battery
print(f"Battery: {drone.get_battery()}")
    
drone.connect()

# Pygame incialization
try:
    pygame.init()
except pygame.error:
    print("Error initializing pygame.")
    print("Make sure you imported all the required libraries.")
    print("Quitting...")
    sys.exit()

# Pygame display configuration
Pygame_Display_Width = 800
Pygame_Display_Lenght = 600

Display = pygame.display.set_mode((Pygame_Display_Width, Pygame_Display_Lenght))
pygame.display.set_caption("Keyboard Control Test 1")

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_w:
                print("Go Forward") 
                drone.move_forward(20)  
            elif evento.key == pygame.K_a:
                print("Turn Left")
                drone.move_left(20)
            elif evento.key == pygame.K_s:
                print("Go Backward")
                drone.move_back(20)
            elif evento.key == pygame.K_d:
                print("Turn Right")
                drone.move_right(20)
            elif evento.key == pygame.K_LEFT:
                print("Rotate the drone to the left")
                drone.rotate_counter_clockwise(90)
            elif evento.key == pygame.K_RIGHT:
                print("Rotate the drone to the right")
                drone.rotate_clockwise(90)
            elif evento.key == pygame.K_UP:
                print("Go up")
                drone.move_up(20)
            elif evento.key == pygame.K_DOWN:
                print("Go down")
                drone.move_down(20)
        sleep(0.5)

    # Limpa a tela
    Display.fill((0, 0, 0))
    pygame.display.flip()
