# main.py

import pygame

# Import game-specific constants, input handlers, asset loader, and core Game class
from pong.constants import *
from pong.input import p1_controls, p2_controls
from pong.assets import load_sfx
from pong.game import Game


"""Initialize everything, then enter the main game loop."""
# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Game window
pygame.display.set_caption("Pong!")
clock = pygame.time.Clock()  # For framerate control

# --- Load audio assets ---
sfx = load_sfx()  # Load all sound effects

# Load and play background music on loop
pygame.mixer.music.load("music/theme.ogg")
pygame.mixer.music.set_volume(0.01)  # Lower music volume
pygame.mixer.music.play(-1)  # Loop indefinitely

# --- Initial game state ---
state = "menu"
num_players = 1  # Default to single-player
controls = (None, None)  # Placeholder until start
game = Game(controls, sfx)  # Instantiate game logic

# Preload fonts for rendering text
big_font = pygame.font.SysFont("Arial", 64, bold=True)
small_font = pygame.font.SysFont("Arial", 32)

while True:
    # --- Event handling ---
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            exit()  # Exit the loop on window close

        # Start the game when SPACE is pressed
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
            if state == "menu":
                state = "play"
                # Assign control functions: p2 only if two players
                controls = (
                    p1_controls,
                    p2_controls if num_players == 2 else None
                )
                game = Game(controls, sfx)  # Reset game state

            if state == "game over":
                state = "menu"
                num_players = 1
                controls = (None, None)
                game = Game(controls, sfx)

    # --- Input polling ---
    keys = pygame.key.get_pressed()

    # --- State: Main Menu ---
    if state == "menu":
        # Switch between 1-player and 2-player options
        if keys[pygame.K_UP] and num_players == 2:
            sfx["up"][0].play()
            num_players = 1
        elif keys[pygame.K_DOWN] and num_players == 1:
            sfx["down"][0].play()
            num_players = 2

        # Draw menu screen
        screen.fill(BLACK)
        title_surf = big_font.render("Pong!", True, WHITE)
        opts_surf = small_font.render(f"{num_players} Player  (UP/DOWN)", True, WHITE)
        prompt_surf = small_font.render("Press SPACE to start", True, YELLOW)
        screen.blit(title_surf, title_surf.get_rect(center=(HALF_W, HALF_H - 50)))
        screen.blit(opts_surf, opts_surf.get_rect(center=(HALF_W, HALF_H + 20)))
        screen.blit(prompt_surf, prompt_surf.get_rect(center=(HALF_W, HALF_H + 70)))

    # --- State: Playing the Game ---
    elif state == "play":
        game.update()  # Advance game logic (ball, bats, scoring)
        game.draw(screen)  # Render gameplay

        # Check for winning condition (first to 10)
        if max(bat.score for bat in game.bats) > 9:
            state = "game over"

    # --- State: Game Over Screen ---
    else:  # state == State.GAME_OVER

        # Draw game-over screen
        screen.fill(BLACK)
        over_surf = big_font.render("Game Over", True, RED)
        back_surf = small_font.render("Press SPACE to return", True, WHITE)
        screen.blit(over_surf, over_surf.get_rect(center=(HALF_W, HALF_H - 40)))
        screen.blit(back_surf, back_surf.get_rect(center=(HALF_W, HALF_H + 30)))

    # --- Finalize frame ---
    pygame.display.flip()  # Update the full display
    clock.tick(FPS)  # Cap the framerate
