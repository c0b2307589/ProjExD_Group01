import pygame as pg
import sys
import random

# 定数
WIDTH, HEIGHT = 800, 600
BOMB_SIZE = 50
KOKATON_SPEED = 5
MAX_HP = 10

# 色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 初期化
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("こうかとんの冒険")
clock = pg.time.Clock()

# 画像読み込み
kk_img = pg.image.load("koukaton.png")
kk_img = pg.transform.scale(kk_img, (80, 80))
bomb_img = pg.image.load("bomb.png")
bomb_img = pg.transform.scale(bomb_img, (BOMB_SIZE, BOMB_SIZE))

# ゲームオーバー画面
def gameover(screen):
    font = pg.font.Font(None, 80)
    text = font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pg.display.update()
    pg.time.wait(2000)
    sys.exit()

# HPゲージ描画
def draw_hp_gauge(screen, hp):
    gauge_width = 200
    gauge_height = 20
    pg.draw.rect(screen, RED, (10, 10, gauge_width, gauge_height))
    pg.draw.rect(screen, GREEN, (10, 10, gauge_width * (hp / MAX_HP), gauge_height))

# メニュー画面
def menu():
    font = pg.font.Font(None, 50)
    options = ["戦う", "終了"]
    selected = 0

    while True:
        screen.fill(WHITE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pg.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pg.K_RETURN:
                    if selected == 0:  # 戦う
                        return
                    elif selected == 1:  # 終了
                        pg.quit()
                        sys.exit()

        for i, option in enumerate(options):
            color = RED if i == selected else BLACK
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
            screen.blit(text, text_rect)

        pg.display.update()

# バトル画面
def battle():
    tmr = 0
    hp = MAX_HP
    bombs = []

    kk_rct = kk_img.get_rect()
    kk_rct.center = WIDTH // 2, HEIGHT // 2

    while True:
        screen.fill(WHITE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            kk_rct.move_ip(0, -KOKATON_SPEED)
        if keys[pg.K_DOWN]:
            kk_rct.move_ip(0, KOKATON_SPEED)
        if keys[pg.K_LEFT]:
            kk_rct.move_ip(-KOKATON_SPEED, 0)
        if keys[pg.K_RIGHT]:
            kk_rct.move_ip(KOKATON_SPEED, 0)

        kk_rct.clamp_ip(screen.get_rect())

        # 爆弾の生成と移動
        if tmr % 100 == 0:
            bomb_rct = bomb_img.get_rect()
            bomb_rct.topleft = (random.randint(0, WIDTH - BOMB_SIZE), random.randint(0, HEIGHT - BOMB_SIZE))
            bombs.append(bomb_rct)

        for bomb in bombs:
            bomb.move_ip(random.choice([-2, 2]), random.choice([-2, 2]))
            screen.blit(bomb_img, bomb)

            # 衝突判定
            if kk_rct.colliderect(bomb):
                hp -= 1
                bombs.remove(bomb)
                if hp <= 0:
                    gameover(screen)

        # HPゲージとこうかとん描画
        draw_hp_gauge(screen, hp)
        screen.blit(kk_img, kk_rct)

        pg.display.update()
        tmr += 1
        clock.tick(60)

# メイン関数
def main():
    menu()  # メニュー画面を表示
    battle()  # 戦闘画面に移行

if __name__ == "__main__":
    main()
