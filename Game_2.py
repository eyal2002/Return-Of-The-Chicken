# -*- coding: utf-8 -*-
import pygame
# import sys
import random


def game_on():
    """
    Checks if the player closed the game.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def print_score(scr, score):
    white = (255, 255, 255)
    pygame.display.set_caption('Show Text')
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(str(score), True, white)
    scr.blit(text, (0, 0))


def en_hit(shots, enemies, boom, scr, dmg):
    """
    Checks if any shots hit an enemy
    """
    # print(boom)
    # print(scr)
    sc_ta = 0
    for enemy in enemies:
        en_hi_bx = pygame.Rect(enemy[1], enemy[2], enemy[3], enemy[4])
        for shot in shots:
            if enemy[0] > 0:
                sh_ht_bx = pygame.Rect(shot[1], shot[2], 8, 50)
                if en_hi_bx.colliderect(sh_ht_bx) == 1:
                    # scr.blit(boom, (enemy[1] - 20, enemy[2] - 20))
                    shots.remove(shot)
                    # pygame.mixer.music.load(r'C:\PR\sound\explosion.mp3')
                    # pygame.mixer.music.play(0)
                    enemy[0] -= dmg
                    sc_ta += 1
    return sc_ta


def dup_en(en):
    """
    creates a duplicate of a type of an enemy.
    """
    to_ret = [en[0], random.randint(10, 750), -20, en[3], en[4], (0, 50), en[6], en[7], en[8]]
    to_ret[5] = to_ret[1], 60
    return to_ret


def get_pos():
    """
    Returns the position of the mouse courser.
    """
    pos = pygame.mouse.get_pos()
    return pos[0] - 25, pos[1] - 13


def return_of_the_chicken():
    """
    main game function
    """
    # Game setup
    pygame.init()
    clock = pygame.time.Clock()
    scr = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Game_2')
    pygame.display.set_icon(pygame.image.load(r'C:\PR\img\SP_tr.png'))
    pygame.mouse.set_visible(1)

    # Images
    sp_tr = pygame.image.load(r'C:\PR\img\SP_1.png')
    sp_tr = pygame.image.load(r'C:\PR\img\SP_7.png')
    b_g = pygame.image.load(r'C:\PR\img\bg_2.jpg')
    boom = pygame.image.load(r'C:\PR\img\boom.png')
    ls_g = pygame.image.load(r'C:\PR\img\laser_g.png')
    ls_r = pygame.image.load(r'C:\PR\img\laser_r.png')
    ls_b = pygame.image.load(r'C:\PR\img\laser_b.png')
    ls_o = pygame.image.load(r'C:\PR\img\laser_o.png')
    ls = [ls_g, ls_r, ls_b, ls_o]
    ls_tp = pygame.image.load(r'C:\PR\img\laser_ro.png')

    pygame.mouse.set_visible(False)

    # Varibles
    run = True
    c_s = 0
    shot_delay = 0
    shot_amount = 8
    shots = []
    dmg = 10
    # enemies [0-hp points, 1-x,2-y, 3-length, 4-height, 5-(x, y) heading, 6-speed, 7-shot chance,8-png scr]
    en_blue = [300, 350, 160, 90, 75, (0, 0), 4, 0.5, pygame.image.load(r'C:\PR\img\chick_blue.png')]
    en_red = [1000, 350, 160, 90, 75, (0, 0), 4, 0.5, pygame.image.load(r'C:\PR\img\chick_red.png')]
    en_vader = [1000, 350, 160, 115, 105, (0, 0), 4, 0.5, pygame.image.load(r'C:\PR\img\chick_vader.png')]
    en_army = [1000, 350, 160, 130, 130, (0, 0), 4, 0.5, pygame.image.load(r'C:\PR\img\chick_army.png')]
    en_super = [1000, 350, 160, 130, 125, (0, 0), 4, 0.5, pygame.image.load(r'C:\PR\img\chick_super.png')]
    en_big = [1000, 350, 160, 105, 100, (0, 0), 4, 0.5, pygame.image.load(r'C:\PR\img\chick_big.png')]
    enemies = [dup_en(en_blue), dup_en(en_red), dup_en(en_army), dup_en(en_big), dup_en(en_vader), dup_en(en_super)]
    sh_lv = 11
    score = 0

    # ==============================================================================================================
    # ==============================================================================================================

    # Main Game function
    while run:
        clock.tick(60)
        run = game_on()

        # get the position
        pos = get_pos()

        # Shots
        if pygame.mouse.get_pressed()[0] == 1 and shot_delay == 0:
            c_s = 22
            shot_delay = shot_amount
            if sh_lv < 4:
                shots.append([c_s, pos[0] + 21, pos[1]])
                # pygame.mixer.music.load(r'C:\PR\sound\ls_sound.mp3')
                # pygame.mixer.music.play(0)
            elif sh_lv < 8:
                shots.append([c_s, pos[0] + 13, pos[1]])
                shots.append([c_s, pos[0] + 29, pos[1]])
                # pygame.mixer.music.load(r'C:\PR\sound\ls_sound.mp3')
                # pygame.mixer.music.play(0)
            else:
                shots.append([c_s, pos[0] + 21, pos[1]])
                shots.append([c_s, pos[0] + 39, pos[1]])
                shots.append([c_s, pos[0] + 3, pos[1]])
                # pygame.mixer.music.load(r'C:\PR\sound\ls_sound.mp3')
                # pygame.mixer.music.play(0)

        if c_s > 0:
            for shot in shots:
                shot[0] -= 1
                shot[2] -= 30
            c_s -= 1

        if shot_delay > 0:
            shot_delay -= 1

        # print(shots)
        to_remove = []
        try:
            for shot in shots:
                if shot[0] <= 0 or shot[2] < -30:
                    to_remove.append(shot)
                else:
                    break
            for rem in to_remove:
                shots.remove(rem)
        except IndexError:
            shots = []
        # print('=================================')
        # print(shots)

        # enemies movement
        for i in enemies:
            vec = (i[5][0] - i[1], i[5][1] - i[2])
            if vec == (0, 0):
                i[5] = random.randint(10, 750), random.randint(5, 400)
            else:
                try:
                    ratio = min(abs(round(i[6]/((vec[0]**2 + vec[1]**2)**0.5), 3)), 1)
                    vec = (i[1] + round(vec[0]*ratio), i[2] + round(vec[1]*ratio))
                except ZeroDivisionError:
                    pass
                i[1], i[2] = vec

        scr.fill((0, 0, 0))
        scr.blit(b_g, (0, 0))

        # Build the game grid

        for i in shots:
            scr.blit(ls_tp, (i[1], i[2]))

        for i in enemies:
            if i[0] > 0:
                scr.blit(i[8], (i[1], i[2]))
            else:
                enemies.remove(i)
        if len(enemies) == 0:
            enemies = [dup_en(en_blue), dup_en(en_blue), dup_en(en_blue), dup_en(en_blue)]

        scr.blit(sp_tr, pos)

        score += en_hit(shots, enemies, boom, scr, dmg) * (sh_lv % 4 + 1)
        print_score(scr, score)
        pygame.display.update()

    pygame.quit()


def main():
    """
    Add Documentation here
    """

    return_of_the_chicken()


if __name__ == '__main__':
    main()
