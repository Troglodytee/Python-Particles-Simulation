from tkinter import Tk, Canvas, Frame, Button, Scale
from math import sqrt
from random import random, randint


WIDTH = 800
HEIGHT = 600
FONT = "Consolas 10"
SCALE_LENGTH = 200

MIN_ADD_PARTICLES = 1
MAX_ADD_PARTICLES = 200
N_ADD_PARTICLES = 50
MIN_DETECTION_RADIUS = 50
MAX_DETECTION_RADIUS = int(sqrt(WIDTH**2+HEIGHT**2))
DETECTION_RADIUS = 100
MIN_SPEED = 1
MAX_SPEED = 10
SPEED = 1
MIN_RUN_DELAY = 1
MAX_RUN_DELAY = 100
RUN_DELAY = 1
MIN_PARTICLE_RADIUS = 1
MAX_PARTICLE_RADIUS = 20
PARTICLE_RADIUS = 10
MIN_VELOCITY_CONSERVATION = 0
MAX_VELOCITY_CONSERVATION = 1
VELOCITY_CONSERVATION = 0.5
MIN_N_RANDOMIZE_TYPE = 1
MAX_N_RANDOMIZE_TYPE = 20
N_RANDOMIZE_TYPES = 3
START_COLOR = 127

class Window:
    def __init__(self):
        self.__window = Tk()
        self.__canvas = Canvas(
            self.__window,
            width=WIDTH,
            height=HEIGHT,
            bg="#000000",
        )
        self.__canvas.grid(row=0, column=0)
        self.__frame_options = Frame(self.__window, borderwidth=0)
        self.__frame_options.grid(row=0, column=1, sticky="nw")
        self.__scale_randomize_types = Scale(
            self.__frame_options,
            orient="horizontal",
            label="Randomize number :",
            font=FONT,
            length=SCALE_LENGTH,
            resolution=1,
            from_=MIN_N_RANDOMIZE_TYPE,
            to=MAX_N_RANDOMIZE_TYPE,
        )
        self.__scale_randomize_types.grid(row=0, column=0, sticky="nw")
        self.__scale_randomize_types.set(N_RANDOMIZE_TYPES)
        self.__button_randomize = Button(
            self.__frame_options,
            text="Randomize",
            font=FONT,
            command=self.__randomize_types,
        )
        self.__button_randomize.grid(row=1, column=0, sticky="nw")
        self.__button_remove = Button(
            self.__frame_options,
            text="Remove all particles",
            font=FONT,
            command=self.__remove_particles,
        )
        self.__button_remove.grid(row=2, column=0, sticky="nw")
        self.__scale_add_particles = Scale(
            self.__frame_options,
            orient="horizontal",
            label="Add particles :",
            font=FONT,
            length=SCALE_LENGTH,
            resolution=1,
            from_=MIN_ADD_PARTICLES,
            to=MAX_ADD_PARTICLES,
        )
        self.__scale_add_particles.grid(row=3, column=0, sticky="nw")
        self.__scale_add_particles.set(N_ADD_PARTICLES)
        self.__button_add = Button(
            self.__frame_options,
            text="Add",
            font=FONT,
            command=self.__add_particles,
        )
        self.__button_add.grid(row=4, column=0, sticky="nw")
        self.__scale_detection_radius = Scale(
            self.__frame_options,
            orient="horizontal",
            label="Detection radius :",
            font=FONT,
            length=SCALE_LENGTH,
            resolution=1,
            from_=MIN_DETECTION_RADIUS,
            to=MAX_DETECTION_RADIUS,
        )
        self.__scale_detection_radius.grid(row=5, column=0, sticky="nw")
        self.__scale_detection_radius.set(DETECTION_RADIUS)
        self.__scale_max_speed = Scale(
            self.__frame_options,
            orient="horizontal",
            label="Max speed :",
            font=FONT,
            length=SCALE_LENGTH,
            resolution=1,
            from_=MIN_SPEED,
            to=MAX_SPEED,
        )
        self.__scale_max_speed.grid(row=6, column=0, sticky="nw")
        self.__scale_max_speed.set(SPEED)
        self.__scale_run_delay = Scale(
            self.__frame_options,
            orient="horizontal",
            label="Display delay (ms) :",
            font=FONT,
            length=SCALE_LENGTH,
            resolution=1,
            from_=MIN_RUN_DELAY,
            to=MAX_RUN_DELAY,
        )
        self.__scale_run_delay.grid(row=7, column=0, sticky="nw")
        self.__scale_run_delay.set(RUN_DELAY)
        self.__scale_particles_radius = Scale(
            self.__frame_options,
            orient="horizontal",
            label="Particles radius :",
            font=FONT,
            length=SCALE_LENGTH,
            resolution=1,
            from_=MIN_PARTICLE_RADIUS,
            to=MAX_PARTICLE_RADIUS,
        )
        self.__scale_particles_radius.grid(row=8, column=0, sticky="nw")
        self.__scale_particles_radius.set(PARTICLE_RADIUS)
        self.__scale_velocity_conservation = Scale(
            self.__frame_options,
            orient="horizontal",
            label="Velocity conservation :",
            font=FONT,
            length=SCALE_LENGTH,
            resolution=0.05,
            from_=MIN_VELOCITY_CONSERVATION,
            to=MAX_VELOCITY_CONSERVATION,
        )
        self.__scale_velocity_conservation.grid(row=9, column=0, sticky="nw")
        self.__scale_velocity_conservation.set(VELOCITY_CONSERVATION)
        self.__button_pause = Button(
            self.__frame_options,
            text=" ► ",
            font=FONT,
            command=self.__change_pause,
        )
        self.__button_pause.grid(row=10, column=0, sticky="nw")
        self.__pause = 1
        self.__matrice = []
        self.__particles = []
        self.__window.mainloop()

    def __randomize_types(self):
        for i in self.__matrice:
            del i[:]
        del self.__matrice[:]
        n_particles = self.__scale_randomize_types.get()
        color = START_COLOR
        delta = (16777216-START_COLOR)//n_particles
        for i in range(n_particles):
            c = str(hex(color))[2:]
            while len(c) < 6:
                c = "0"+c
            self.__matrice += [["#"+c]]
            color += delta
            for j in range(n_particles):
                self.__matrice[-1] += [random()*2-1]

    def __change_pause(self):
        self.__pause = 1-self.__pause
        self.__button_pause["text"] = [ "| |"," ► "][self.__pause]
        if not self.__pause:
            self.__run()

    def __remove_particles(self):
        del self.__particles[:]

    def __add_particles(self):
        if len(self.__matrice) > 0:
            for i in range(self.__scale_add_particles.get()):
                self.__particles += [Particle(
                    randint(0, len(self.__matrice)-1),
                    randint(0, WIDTH-1),
                    randint(0, HEIGHT-1),
                    1,
                    0
                )]
            self.__pause = 1
            self.__button_pause["text"] = " ► "
            self.__run()

    def __run(self):
        self.__canvas.delete("all")
        n_particles = len(self.__particles)
        detection_radius = self.__scale_detection_radius.get()
        max_speed = self.__scale_max_speed.get()
        particle_radius = self.__scale_particles_radius.get()
        velocity_conservation = self.__scale_velocity_conservation.get()
        if n_particles:
            for i in range(n_particles-1):
                p1 = self.__particles[i]
                for j in range(i+1, n_particles):
                    p2 = self.__particles[j]
                    v = p2.get_coords()-p1.get_coords()
                    distance = v.norm()
                    if distance <= detection_radius:
                        p1.interact(
                            p2,
                            v,
                            distance,
                            max_speed,
                            particle_radius*2,
                            self.__matrice
                        )
                p1.compute_interact(max_speed, velocity_conservation)
            for i in range(n_particles-1):
                p1 = self.__particles[i]
                for j in range(i+1, n_particles):
                    p2 = self.__particles[j]
                    v = p2.get_coords()-p1.get_coords()
                    distance = v.norm()
                    if distance <= particle_radius*2:
                        p1.take_away(p2, v, distance, particle_radius*2)
                p1.compute_take_away(particle_radius)
                self.__canvas.create_oval(
                    p1.get_x()-particle_radius,
                    p1.get_y()-particle_radius,
                    p1.get_x()+particle_radius,
                    p1.get_y()+particle_radius,
                    fill=self.__matrice[p1.get_type()][0],
                    outline=self.__matrice[p1.get_type()][0],
                )
            if not self.__pause:
                self.__window.after(self.__scale_run_delay.get(), self.__run)


class Particle:
    def __init__(self, type, x, y, vx, vy):
        self.__type = type
        self.__coords = Vector(x, y)
        self.__velocity = Vector(vx, vy)
        self.__spacing = Vector(0, 0)
        self.__acceleration = Vector(0, 0)

    def get_type(self):
        return self.__type

    def get_coords(self):
        return self.__coords

    def get_x(self):
        return self.__coords.x

    def get_y(self):
        return self.__coords.y

    def interact(self, other, v, distance, max_speed, spacing, matrice):
        force1 = matrice[self.get_type()][other.get_type()+1]
        force2 = matrice[other.get_type()][self.get_type()+1]
        if distance == 0:
            v = Vector(spacing, 0)
        else:
            v *= max_speed/distance*((distance-spacing)/distance)
        self.__acceleration += v*force1
        other.__acceleration -= v*force2

    def compute_interact(self, max_speed, velocity_conservation):
        self.__velocity += self.__acceleration
        if self.__velocity.norm() > max_speed:
            self.__velocity.set_norm(max_speed)
        self.__coords += self.__velocity
        self.__velocity *= velocity_conservation
        self.__acceleration *= 0

    def take_away(self, other, v, distance, spacing):
        if distance == 0:
            v = Vector(spacing/2-distance, 0)
        else:
            v.set_norm(distance-spacing)
        self.__coords += v
        other.__coords -= v

    def compute_take_away(self, radius):
        self.__coords += self.__spacing
        if self.__coords.x-radius < 0:
            self.__coords.x = radius
        elif self.__coords.x+radius >= WIDTH:
            self.__coords.x = WIDTH-radius-1
        if self.__coords.y-radius < 0:
            self.__coords.y = radius
        elif self.__coords.y+radius >= HEIGHT:
            self.__coords.y = HEIGHT-radius-1
        self.__spacing *= 0


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def norm(self):
        return sqrt(self.x**2+self.y**2)

    def set_norm(self, n):
        norm = self.norm()
        if norm == 0:
            self.x = n
        else:
            self.x *= n/norm
            self.y *= n/norm

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)

    def __mul__(self, n):
        return Vector(self.x*n, self.y*n)


window = Window()
