import pygame
import threading

def play_audio_with_stop(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    def wait_for_enter():
        input("Press Enter to stop playback...\n")
        pygame.mixer.music.stop()
        print("Playback stopped.")

    t = threading.Thread(target=wait_for_enter)
    t.start()
    t.join()

play_audio_with_stop("temp_talk.wav")