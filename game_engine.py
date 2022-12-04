import time

class Image():
    def __init__(self, path):
        with open(path, "rb") as f:
            img_format = f.readline()
            if img_format != b"P4\n":
                print("Wrong image format")
                exit()
            dimensions = f.readline()
            w, h = [int(x) for x in dimensions.split(b" ")]
            img = bytearray(f.read())
        self.bitmap, self.width, self.height = img, w, h

class Sprite():
    def __init__(self, x, y, image, display):
        self.set_pos(x, y)
        self.image = image
        self.display = display

    def change_image(self, image):
        self.image = image

    def draw(self):
        if self.image != None:
            self.display.image(self.image.bitmap, w=self.image.width, h=self.image.height, x=int(self.x), y=int(self.y))

    def set_pos(self, x = None, y = None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y


class MovingObject(Sprite):
    def __init__(self, x, y, image, display, ground=0, gravity=0):
        super().__init__(x, y, image, display)
        self.motion_vector = [0, 0]
        self.gravity = gravity
        self.ground = ground
        self.last_tick = 0

    def set_motion_vector(self, x, y):
        if x != None:
            self.motion_vector[0] = x
        if y != None:
            self.motion_vector[1] = y

    def physics_tick(self, now):
        diff = time.ticks_diff(now, self.last_tick) * 0.1
        self.motion_vector[1] += self.gravity * diff
        self.x += self.motion_vector[0] * diff
        self.y += self.motion_vector[1] * diff
        if self.gravity != 0 and self.y >= self.ground - self.image.height:
            self.y = self.ground - self.image.height
            self.motion_vector[1] = 0
        self.last_tick = now

    def on_ground(self):
        return self.y == self.ground - self.image.height

    def collision_test(self, obstacles):
        for obstacle in obstacles:
            if (self.x + self.image.width >= obstacle.x and obstacle.x + obstacle.image.width >= self.x and
                self.y + self.image.height >= obstacle.y and obstacle.y + obstacle.image.height >= self.y):
                return obstacle
        return None
