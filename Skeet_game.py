"""
File: skeet.py
Original Author: Br. Burton
Designed to be completed by others
This program implements an awesome version of skeet.
"""
import arcade
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 3
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 10

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
TARGET_SAFE_RADIUS = 15


class Point:
    """
    This class will determine Point attributes
    """
    def __init__(self):
        # Set our Object center.
        self.x = 1
        self.y = 1


class Velocity:

    def __init__(self):
        """
        This class will determine velocity
        """
        self.dx = 10
        self.dy = 10


class FlyingObjects:
    """
    FLying objects parent class.
    """
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True

    def advance(self):
        """
        Ball moves here
        """
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def is_off_screen(self, screen_width, screen_height):
        """
        It will notice if the ball is off screen.
        :param screen_width:
        :param screen_height:
        :return: If the ball is in the screen limits or not
        """
        if self.center.x > screen_width:
            return True

        if self.center.y > screen_height:
            return True
        else:
            return False


class Bullet(FlyingObjects):

    def __init__(self):
        """
        The bullets are little balls that comes out from Rifle() to kill an target
        """
        super().__init__()
        self.radius = BULLET_RADIUS

    def draw(self):
        """
        Draw our Bullet on screen
        """
        arcade.draw_circle_filled(self.center.x, self.center.y, 5, BULLET_COLOR)

    def fire(self, angle: float):
        """
        Fire the bullet method.
        :param angle:
        :return: none
        """
        self.velocity.dx = math.cos(math.radians(angle)) * 10
        self.velocity.dy = math.sin(math.radians(angle)) * 10
        self.advance()


class Target(FlyingObjects):

    def __init__(self):
        """
        Targets will random appear.
        """
        super().__init__()
        self.center.y = random.uniform(SCREEN_HEIGHT / 2, SCREEN_HEIGHT)
        self.radius = TARGET_RADIUS
        self.velocity.dx = random.uniform(1, 4)
        self.velocity.dy = random.uniform(-15, 4)

    def draw(self):
        """
        Draw a standard target.
        """
        arcade.draw_circle_filled(self.center.x, self.center.y, 20, TARGET_COLOR)

    def hit(self):
        """
        When the bullet hits the target, The Target might die or decrease in life.
        """
        self.alive = False
        return 1


class StandardTarget(Target):

    def __init__(self):
        """
        Normal target
        """
        super().__init__()


class SafeTarget(Target):

    def __init__(self):
        """
        Safe target
        """
        super().__init__()

    def draw(self):
        """
        Draw our safe target.
        """
        arcade.draw_rectangle_filled(self.center.x, self.center.y, 50, 50, TARGET_SAFE_COLOR)

    def hit(self):
        """
        When the bullet hits the target, The Target might die or decrease in life.
        """
        self.alive = False
        return -10


class StrongTarget(Target):

    def __init__(self):
        """
        Safe target
        """
        super().__init__()
        self.velocity.dx = random.uniform(1, 3)
        self.velocity.dy = random.uniform(-3, 3)
        self.life = 3

    def draw(self):
        """
        Draw our safe target.
        """
        arcade.draw_circle_outline(self.center.x, self.center.y, self.radius, TARGET_COLOR)
        text_x = self.center.x - (self.radius / 2)
        text_y = self.center.y - (self.radius / 2)
        arcade.draw_text(repr(self.life), text_x, text_y, TARGET_COLOR, font_size=20)

    def hit(self):
        """
        When the bullet hits the target, The Target might die or decrease in life.
        """
        self.life -= 1
        if self.life == 0:
            self.alive = False
            return 5
        else:
            return 1




class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        self.center = Point()
        self.center.x = 0
        self.center.y = 0

        self.angle = 45

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, self.angle)


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.rifle = Rifle()
        self.score = 0

        self.bullets = []
        self.targets = []

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.rifle.draw()

        for bullet in self.bullets:
            bullet.draw()

        for target in self.targets:
            if target.alive:
                target.draw()
        # TODO: iterate through your targets and draw them...

        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
        if random.randint(1, 50) == 1:
            self.create_target()

        for bullet in self.bullets:
            bullet.advance()

        for target in self.targets:
            target.advance()

        # TODO: Iterate through your targets and tell them to advance

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """
        num = random.randint(1, 3)
        if num == 1:
            target = StandardTarget()

        elif num == 2:
            target = SafeTarget()

        else:
            target = StrongTarget()

        self.targets.append(target)

        # TODO: Decide what type of target to create and append it to the list

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                            abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.score += target.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
