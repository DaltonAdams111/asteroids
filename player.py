import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot
pygame.font.init()
font = pygame.font.SysFont(name=pygame.font.get_default_font(), size=32)

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.position = pygame.Vector2(x, y)
        self.radius = PLAYER_RADIUS
        self.rotation = 0
        self.shoot_timer = 0
        self.score = 0

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        score_text = font.render(f"Score: {self.score}", 1, "white")
        screen.blit(score_text, (SCREEN_WIDTH / 2 - score_text.get_width() / 2, 10))

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        if self.position.x + forward.x * PLAYER_SPEED * dt < 0 or self.position.x + forward.x * PLAYER_SPEED * dt > SCREEN_WIDTH:
            return
        if self.position.y + forward.y * PLAYER_SPEED * dt < 0 or self.position.y + forward.y * PLAYER_SPEED * dt > SCREEN_HEIGHT:
            return
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED