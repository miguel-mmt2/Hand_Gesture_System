import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import keyboard
from keyboard import add_hotkey
import time

class Drone:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y 
        self.z = z

    def move_up(self, distance):
        self.z += distance

    def move_down(self, distance):
        if self.z - distance >= 0:
            self.z -= distance

    def move_forward(self, distance):
        self.x += distance

    def move_backward(self, distance):
        self.x -= distance

    def move_right(self, distance):
        self.y += distance

    def move_left(self, distance):
        self.y -= distance

    def get_position(self):
        return (self.x, self.y, self.z)

# Create a drone object
drone = Drone() 
 
# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

add_hotkey('w', 13) 
add_hotkey('a', 0)
add_hotkey('s', 1) 
add_hotkey('d', 2)

while True:
    if keyboard.is_pressed('w'):
        drone.move_up(1) 
    elif keyboard.is_pressed('s'):
        drone.move_down(1)
    elif keyboard.is_pressed('a'):
        drone.move_left(1)
    elif keyboard.is_pressed('d'):
        drone.move_right(1)
    elif keyboard.is_pressed('q'):
        drone.move_forward(1)
    elif keyboard.is_pressed('e'):
        drone.move_backward(1)
    elif keyboard.is_pressed('esc'):
        break

    x, y, z = drone.get_position()

    # Clear the plot
    ax.cla()   

    # Plot drone position
    ax.scatter(x, y, z, c='r', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Refresh plot
    plt.draw()
    plt.pause(0.01)

plt.show()
