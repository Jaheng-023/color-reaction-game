import platform

def play_sound(correct=True):
    if platform.system() == "Windows":
        try:
            import winsound
            if correct:
                winsound.Beep(800, 150)
            else:
                winsound.Beep(300, 250)
        except Exception:
            print('\a')
    else:
        print('\a')