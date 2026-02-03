import sys
import pygame
from distribution_quiz import DistributionQuiz
from button import Button
from plot_adapter import make_plot_surface

# ---------- Init ----------
pygame.init()
pygame.font.init()

FONT = pygame.font.SysFont("arial", 28)

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 900
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
GREEN = (100, 255, 150)
RED = (255, 0, 0)
GRAY = (180, 180, 180)

GRAPH_X = 20
GRAPH_Y = 50
GRAPH_WIDTH = 800
GRAPH_HEIGHT = 700

BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40
BUTTON_SPACING_X = 80
BUTTON_SPACING_Y = 20
BUTTON_START_X = 850
BUTTON_START_Y = 80

FEEDBACK_TEXT_X = 50
FEEDBACK_TEXT_Y = 800

# ---------- Helpers ----------
def build_answer_buttons(quiz):
    buttons = []
    for i, (key, (name, _)) in enumerate(quiz.distribution.items()):
        row = i // 2
        col = i % 2

        x = BUTTON_START_X + col * (BUTTON_WIDTH + BUTTON_SPACING_X)
        y = BUTTON_START_Y + row * (BUTTON_HEIGHT + BUTTON_SPACING_Y)

        buttons.append(Button(
            x=x, y=y,
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            text=name, color=BLUE, key=key
        ))
    return buttons

def new_round(quiz, plot_policy="hist"):
    correct_key = quiz.rng.choice(list(quiz.distribution.keys()))
    correct_name, gen_fn = quiz.distribution[correct_key]
    data = gen_fn()
    mode = ""

    if plot_policy == "hist":
        mode = "hist"
    elif plot_policy == "ogive":
        mode = "ogive"
    elif plot_policy == "both":
        mode = quiz.rng.choice(["hist", "ogive"])
    else:
        raise ValueError("plot_policy must be hist, ogive or both")
        
    surf = make_plot_surface(
        data,
        mode=mode, 
        size_px=(GRAPH_WIDTH - 4, GRAPH_HEIGHT - 4),
        bins=40,
        title="Guess the distribution"
    )
    return correct_key, correct_name, data, surf, mode

# ---------- Main ----------
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Distribution Quiz")
    clock = pygame.time.Clock()

    quiz = DistributionQuiz()
    buttons = build_answer_buttons(quiz)

    next_round_button = Button(
        x=BUTTON_START_X,
        y=FEEDBACK_TEXT_Y + 50,
        width=200,
        height=40,
        text="Next round",
        color=GRAY,
        key="next"
    )
    hist_btn  = Button(
        x=850,  
        y=320, 
        width=120, 
        height=40, 
        text="Hist",  
        key="mode_hist",  
        color=GRAY)
    ogive_btn = Button(
        x=990,  
        y=320, 
        width=120, 
        height=40, 
        text="Ogive", 
        key="mode_ogive", 
        color=GRAY)
    both_btn  = Button(
        x=1130, 
        y=320, 
        width=120, 
        height=40, 
        text="Both",  
        key="mode_both",  
        color=GRAY)


    plot_policy = "hist"
    correct_key, correct_name, data, plot_surface, current_mode = new_round(quiz, plot_policy)

    feedback_msg = ""
    feedback_color = BLACK
    answered = False

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if hist_btn.is_over(pos):
                    plot_policy = "hist"
                    feedback_msg = ""
                    answered = False
                    correct_key, correct_name, data, plot_surface, current_mode = new_round(quiz, plot_policy)

                elif ogive_btn.is_over(pos):
                    plot_policy = "ogive"
                    feedback_msg = ""
                    answered = False
                    correct_key, correct_name, data, plot_surface, current_mode = new_round(quiz, plot_policy)

                elif both_btn.is_over(pos):
                    plot_policy = "both"
                    feedback_msg = ""
                    answered = False
                    correct_key, correct_name, data, plot_surface, current_mode = new_round(quiz, plot_policy)

                
                if answered and next_round_button.is_over(pos):
                    feedback_msg = ""
                    feedback_color = BLACK
                    answered = False
                    correct_key, correct_name, data, plot_surface, current_mode = new_round(quiz, plot_policy)

                
                elif not answered:
                    for button in buttons:
                        if button.is_over(pos):
                            if button.key == correct_key:
                                feedback_msg = "Correct!"
                                feedback_color = GREEN
                                quiz.score += 1
                                quiz.streak += 1
                            else:
                                feedback_msg = f"Incorrect, it should have been {correct_name}"
                                feedback_color = RED
                                quiz.streak = 0
                            answered = True
                            break

        screen.fill(WHITE)

        if feedback_msg:
            screen.blit(FONT.render(feedback_msg, True, feedback_color), (FEEDBACK_TEXT_X, FEEDBACK_TEXT_Y))
        screen.blit(FONT.render(f"Score: {quiz.score}", True, BLACK), (BUTTON_START_X, 20))
        screen.blit(FONT.render(f"Streak: {quiz.streak}", True, BLACK), (BUTTON_START_X+100, 20))

        pygame.draw.rect(screen, (220, 220, 220), (GRAPH_X, GRAPH_Y, GRAPH_WIDTH, GRAPH_HEIGHT), 2)
        screen.blit(plot_surface, (GRAPH_X + 2, GRAPH_Y + 2))

        for button in buttons:
            button.draw(screen, outline=BLACK)
        next_round_button.draw(screen, outline=BLACK)
        hist_btn.draw(screen, outline=BLACK)
        ogive_btn.draw(screen, outline=BLACK)
        both_btn.draw(screen, outline=BLACK)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
