import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()

    # Set window dimensions
    window_width = 800
    window_height = 600

    # Create a resizable window
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    pygame.display.set_caption("The Dragon's Slayer")

    # Define fonts and colors
    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)  # White
    background_color = (0, 0, 0)  # Black

    # Story and choices variables
    story = [
        "You are a knight on a quest to find the dragon's lair.",
        "You stand before the entrance of a dark cave.",
        "Do you ENTER the cave, LOOK around, or RETURN to the village?"
    ]

    choices = {
        "ENTER": [
            "You enter the cave and hear a low growl echoing.",
            "Do you DRAW your sword or PROCEED quietly?"
        ],
        "DRAW": [
            "You draw your sword and confront the dragon head-on!",
            "The dragon is startled and breathes fire.",
            "Prepare for battle!"
        ],
        "PROCEED": [
            "You proceed quietly and discover the dragon sleeping.",
            "Do you STEAL its treasure or SLAY the dragon?"
        ],
        "STEAL": [
            "You carefully gather some treasure and escape unnoticed.",
            "You return to the kingdom a hero, wealthy beyond your dreams.",
            "Something slumbers underneath the ancient mountain..."
        ],
        "SLAY": [
            "You strike the dragon while it sleeps, but it awakens!",
            "A fierce battle ensues!"
        ],
        "LOOK": [
            "You look around and notice strange claw marks on the rocks.",
            "Do you INVESTIGATE the marks or ENTER the cave?"
        ],
        "INVESTIGATE": [
            "The marks lead you to a hidden path, bypassing the dragon.",
            "You find an ancient artifact that grants you immense power.",
            "Do you RETURN to the village or EXPLORE deeper into the cave?"
        ],
        "RETURN": [
            "You decide the quest is too dangerous and return to the village.",
            "Life goes on, but you are haunted by what could have been.",
            "Something slumbers underneath the ancient mountain..."
        ],
        "EXPLORE": [
            "You delve deeper into the cave, your artifact glowing faintly.",
            "You discover an elder-dragon, guarding even greater treasure.",
            "Do you USE the artifact to challenge the elder-dragon or NEGOTIATE with it?"
        ],
        "USE": [
            "You unleash the artifact's power, overwhelming even the elder-dragon.",
            "The elder-dragon yields and grants you its treasure, cowering in fear.",
            "You return to the kingdom as the most powerful entity of all.",
            "Nothing remains to challenge you underneath the ancient mountain"
        ],
        "NEGOTIATE": [
            "You negotiate with the elder-dragon, offering a truce.",
            "The elder-dragon agrees to a pact, and you form a powerful alliance.",
            "Together, you bring people and dragons under one banner."
        ]
    }

    # Game state variables
    def reset_game():
        """Reset the game to its initial state."""
        return {
            'current_story': story,
            'current_valid_choices': ["ENTER", "LOOK", "RETURN"],  # Valid choices for the initial story
            'user_choice': "",
            'invalid_choice_flag': False,
            'battle_in_progress': False,
            'player_hp': 50,
            'dragon_hp': 100,
            'game_ended': False  # Flag to track if the game is ended
        }

    # Initialize game state
    game_state = reset_game()

    def render_text(text, font, color, x, y):
        """Render text onto the screen at a specific position."""
        lines = text.split("\n")
        for i, line in enumerate(lines):
            rendered_text = font.render(line, True, color)
            screen.blit(rendered_text, (x, y + i * 30))

    def update_story(choice):
        """Update the story based on the user's choice."""
        nonlocal game_state
        if choice in game_state['current_valid_choices']:
            game_state['current_story'] = choices[choice]
            game_state['invalid_choice_flag'] = False
            if choice == "ENTER":
                game_state['current_valid_choices'] = ["DRAW", "PROCEED"]
            elif choice == "LOOK":
                game_state['current_valid_choices'] = ["INVESTIGATE", "ENTER"]
            elif choice == "PROCEED":
                game_state['current_valid_choices'] = ["STEAL", "SLAY"]
            elif choice == "SLAY" or choice == "DRAW":
                game_state['battle_in_progress'] = True
                game_state['current_valid_choices'] = ["ATTACK", "DEFEND"]
            elif choice == "STEAL":
                game_state['current_valid_choices'] = []
                game_state['game_ended'] = True  # Mark the game as ended
            elif choice == "INVESTIGATE":
                game_state['current_valid_choices'] = ["RETURN", "EXPLORE"]
            elif choice == "RETURN":
                game_state['game_ended'] = True
            elif choice == "EXPLORE":
                game_state['current_valid_choices'] = ["USE", "NEGOTIATE"]
            elif choice == "USE":
                game_state['current_valid_choices'] = []  # Mark the game as ended
                game_state['game_ended'] = True
            elif choice == "NEGOTIATE":
                game_state['current_valid_choices'] = []  # Mark the game as ended
                game_state['game_ended'] = True
        else:
            game_state['invalid_choice_flag'] = True  # Flag invalid input

    def battle():
        """Handle the battle between the player and the dragon."""
        nonlocal game_state
        if game_state['player_hp'] > 0 and game_state['dragon_hp'] > 0:
            game_state['current_story'] = [
                f"Player HP: {game_state['player_hp']} | Dragon HP: {game_state['dragon_hp']}",
                "Do you ATTACK or DEFEND?"
            ]
        elif game_state['player_hp'] <= 0:
            game_state['current_story'] = ["You have been defeated by the dragon...", "GAME OVER."]
            game_state['battle_in_progress'] = False
            game_state['game_ended'] = True
        elif game_state['dragon_hp'] <= 0:
            game_state['current_story'] = ["The dragon has been slain!", "You emerge victorious!"]
            game_state['battle_in_progress'] = False
            game_state['game_ended'] = True
        return game_state['current_story']

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_state['user_choice'].lower() == "restart":
                        game_state = reset_game()  # Reset game if "restart" is entered
                    else:
                        update_story(game_state['user_choice'].upper())
                    game_state['user_choice'] = ""
                elif event.key == pygame.K_BACKSPACE:
                    game_state['user_choice'] = game_state['user_choice'][:-1]  # Remove the last character
                elif event.unicode.isalpha():
                    game_state['user_choice'] += event.unicode
            elif event.type == pygame.VIDEORESIZE:
                window_width, window_height = event.size
                screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

        # If battle is in progress, process the battle system
        if game_state['battle_in_progress']:
            # Simple battle logic: attack or defend
            if game_state['user_choice'].upper() == "ATTACK":
                game_state['dragon_hp'] -= 10
                game_state['player_hp'] -= 10  # Dragon retaliates
                game_state['user_choice'] = ""  # Reset user input
            elif game_state['user_choice'].upper() == "DEFEND":
                game_state['player_hp'] += 5  # Less damage when defending
                game_state['user_choice'] = ""  # Reset user input
            # Update the battle story based on current health points
            game_state['current_story'] = battle()

        # Clear the screen
        screen.fill(background_color)

        # Display feedback if invalid choice was made
        y_offset = 20
        if game_state['invalid_choice_flag']:
            render_text("Invalid choice. Try again:", font, text_color, 20, y_offset)
            y_offset += 50

        # Display the current part of the story
        for i, line in enumerate(game_state['current_story']):
            render_text(line, font, text_color, 20, y_offset + i * 40)

        # Display the user's input
        render_text(f"> {game_state['user_choice']}", font, text_color, 20, y_offset + len(game_state['current_story']) * 40 + 20)

        # Display the "The End" message if the game has ended
        if game_state['game_ended']:
            render_text("The End. Type 'Restart' to restart the game.", font, text_color, 20, y_offset + len(game_state['current_story']) * 40 + 60)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()