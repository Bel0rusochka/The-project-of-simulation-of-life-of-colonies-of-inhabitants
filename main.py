from PygameModule import  *


if __name__ == "__main__":
    while True:
        pygame_module = PygameModule(InitialGame())
        pygame_module.start_game()

        if pygame_module.get_status_break_event():
            break
