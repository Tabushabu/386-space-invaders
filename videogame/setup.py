import pygame
import json


window_width = 800
window_height = 600
player_width = 50
player_height = 50
player_x = window_width // 2 - player_width // 2
player_y = window_height - player_height - 10
player_width = 50
player_height = 50
player_speed = 5
enemy_width = 50
enemy_height = 50
enemy_speed = 2
bullet_width = 5
bullet_height = 20
bullet_speed = 7
obstacle_width = 100
obstacle_height = 20
obstacle_spacing = 100

high_scores = []
try:
    with open("high_scores.json") as file:
        high_scores = json.load(file)
except FileNotFoundError:
    pass
