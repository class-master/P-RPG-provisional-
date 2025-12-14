# -*- coding: utf-8 -*-
"""
Day2 エンティティ（STUDENT版）：Player/Camera/HUDの骨格＋TODO
-----------------------------------------------------------
- ここから“走る／スタミナ／慣性／摩擦／衝突／HUD”を **段階導入**。
- まずは **移動→描画だけ** 完走できればOK。あとから一つずつ足す。

実装ガイド（こう書くと良いよ例）：
- 慣性: vel = vel*(1-ACCEL) + 目標速度*ACCEL
- 摩擦: vel *= FRICTION
- スタミナ: 走行中に減少、非走行時に回復（最大/最小でクリップ）
- 衝突: X→判定→巻戻し／Y→判定→巻戻し（軸分離）
"""
import pygame
from pygame import Surface
from config import (
    TILE_SIZE, PLAYER_SPEED, RUN_MULTIPLIER, PLAYER_ACCEL, PLAYER_FRICTION,
    STAMINA_MAX, STAMINA_RUN_COST, STAMINA_RECOVER, HP_MAX,
    WHITE, GREEN, YELLOW, BLUE
)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_px):
        super().__init__()
        self.image = Surface((TILE_SIZE - 6, TILE_SIZE - 6), pygame.SRCALPHA)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=pos_px)

        # ベクトル（慣性＆摩擦に使う）
        self.vel = pygame.math.Vector2(0, 0)

        self.hp = HP_MAX
        self.stamina = STAMINA_MAX

    def handle_input(self, keys, running: bool):
        move = pygame.math.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  move.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: move.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:    move.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  move.y += 1
        if move.length_squared() > 0:
            move = move.normalize()

        # ★STEP1: まずは一定速度でOK（走る/慣性は後で）
        speed = PLAYER_SPEED

        # TODO(走る/スタミナ):
        # if running and self.stamina > 0:
        #     speed *= RUN_MULTIPLIER
        #     self.stamina = max(0, self.stamina - STAMINA_RUN_COST)
        # else:
        #     self.stamina = min(STAMINA_MAX, self.stamina + STAMINA_RECOVER)

        # TODO(慣性/摩擦) — まずは“瞬間移動”でOK、後から補間に差し替え
        # self.vel.x = self.vel.x * (1 - PLAYER_ACCEL) + move.x * speed * PLAYER_ACCEL
        # self.vel.y = self.vel.y * (1 - PLAYER_ACCEL) + move.y * speed * PLAYER_ACCEL
        # self.vel *= PLAYER_FRICTION
        # 一旦は：
        self.vel.x = move.x * speed
        self.vel.y = move.y * speed

    def move_and_collide(self, grid):
        # TODO(衝突・軸分離)：最初は“壁すり抜け”でOK → 後で実装
        self.rect.x += int(self.vel.x)
        self.rect.y += int(self.vel.y)

    def update(self, grid, keys, running):
        self.handle_input(keys, running)
        self.move_and_collide(grid)

class Camera:
    def __init__(self, screen_size):
        self.offset = pygame.math.Vector2(0, 0)
        self.screen_w, self.screen_h = screen_size
    def follow(self, player_rect):
        self.offset.x = max(0, player_rect.centerx - self.screen_w // 2)
        self.offset.y = max(0, player_rect.centery - self.screen_h // 2)

class HUD:
    def __init__(self, font):
        self.font = font

    def draw_bar(self, screen, x, y, w, h, ratio, fg_color, bg_color=(40, 40, 40)):
        import pygame
        pygame.draw.rect(screen, bg_color, (x, y, w, h))
        fill_w = int(w * max(0.0, min(1.0, ratio)))
        pygame.draw.rect(screen, fg_color, (x, y, fill_w, h))
        pygame.draw.rect(screen, (20,20,20), (x, y, w, h), 1)

    def render(self, screen, player):
        # TODO(HUD)：最初は非表示でOK → 後でバーを描こう
        # self.draw_bar(screen, 16, 14, 200, 14, player.hp/float(HP_MAX), GREEN)
        # stamina_ratio = player.stamina/float(STAMINA_MAX)
        # color = YELLOW if stamina_ratio < 0.3 else WHITE
        # self.draw_bar(screen, 16, 34, 200, 10, stamina_ratio, color)
        pass
