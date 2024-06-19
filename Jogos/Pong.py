def jogar():    
    import pygame
    from sys import exit


    pygame.init()

    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    ball_speed_x = 9
    ball_speed_y = 9

    player_speed = 0
    enemy_speed = 0

    player_score = 0
    enemy_score = 0

    player_surf = pygame.Surface((10,75))
    player_surf.fill("White")
    player_rect = player_surf.get_rect(center=(5, 300))

    enemy_surf = pygame.Surface((10,75))
    enemy_surf.fill("White")
    enemy_rect = enemy_surf.get_rect(center=(795, 300))

    ball_surf = pygame.Surface((12,12))
    ball_surf.fill("White")
    ball_rect = ball_surf.get_rect(center=(400, 300))

    score_font = pygame.font.Font(None, 80)
    player_score_surf = score_font.render(f"{player_score}", True, "White")
    enemy_score_surf = score_font.render(f"{enemy_score}", True, "White")
    player_score_rect = player_score_surf.get_rect(center=(200, 100))
    enemy_score_rect = enemy_score_surf.get_rect(center=(600, 100))

    bg_surf = pygame.Surface((800, 600))
    bg_surf.fill("Black")

    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    enemy_speed -= 8
                elif event.key == pygame.K_DOWN:
                    enemy_speed += 8
                elif event.key == pygame.K_w:
                    player_speed -= 8
                elif event.key == pygame.K_s:
                    player_speed += 8          
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    enemy_speed += 8
                elif event.key == pygame.K_DOWN:
                    enemy_speed -= 8
                elif event.key == pygame.K_w:
                    player_speed += 8
                elif event.key == pygame.K_s:
                    player_speed -= 8 

        ball_rect.x += ball_speed_x
        ball_rect.y += ball_speed_y


        player_rect.y += player_speed
        enemy_rect.y += enemy_speed

        if player_rect.top <= 0:
            player_rect.top = 0
        elif player_rect.bottom >= 600:
            player_rect.bottom = 600

        if enemy_rect.top <= 0:
            enemy_rect.top = 0
        elif enemy_rect.bottom >= 600:
            enemy_rect.bottom = 600

        if ball_rect.top <= 0 or ball_rect.bottom >= 600:
            ball_speed_y *= -1
        elif ball_rect.left <= 0:
            ball_rect.center = (400,300)
            enemy_score +=1
            ball_speed_x *= -1
        elif ball_rect.right >= 800:
            ball_rect.center = (400,300)
            ball_speed_x *= -1
            player_score +=1
        elif ball_rect.colliderect(player_rect):
            ball_speed_x *= -1
        elif ball_rect.colliderect(enemy_rect):
            ball_speed_x *= -1

    

        
        screen.blit(bg_surf, (0, 0))
        screen.blit(player_surf, player_rect)
        screen.blit(enemy_surf, enemy_rect)  
        screen.blit(ball_surf, ball_rect)
        player_score_surf = score_font.render(f"{player_score}", True, "White")
        enemy_score_surf = score_font.render(f"{enemy_score}", True, "White")      
        screen.blit(player_score_surf, player_score_rect) 
        screen.blit(enemy_score_surf, enemy_score_rect)     
        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    jogar()