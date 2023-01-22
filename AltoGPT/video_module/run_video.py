import cv2
import pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(r"D:/AltoTech/ALTO_CERO/Alto_Playground/epjom-bot/AltoGPT/assets/bot-videos/Elon_listening.mp3")

# TODO: Move to config file
CONFIG = {
    "idle_video_path": r"D:/AltoTech/ALTO_CERO/Alto_Playground/epjom-bot/AltoGPT/assets/bot-videos/Elon_idle.mp4",
    "listening_video_path": r"D:/AltoTech/ALTO_CERO/Alto_Playground/epjom-bot/AltoGPT/assets/bot-videos/Elon_listening.mp4",
    "talking_video_path": None,
    "listening_audio_path": r"D:/AltoTech/ALTO_CERO/Alto_Playground/epjom-bot/AltoGPT/assets/bot-videos/Elon_listening.mp3",
    "talking_audio_path": None,
}


class FrameHandler:
    def __init__(self, config):
        self.frame_status = "idle"  # ['idle', 'listening', 'talking']

        # Parse config
        self.idle_cap = cv2.VideoCapture(config["idle_video_path"])
        self.listening_cap = cv2.VideoCapture(config["listening_video_path"])
        self.talking_cap = cv2.VideoCapture(config["talking_video_path"])
        self.fps = self.idle_cap.get(cv2.CAP_PROP_FPS)

        self.listening_audio_path = config["listening_audio_path"]
        self.talking_audio_path = config["talking_audio_path"]

        self.active_audio = None

    def get_frame(self):

        if self.frame_status == "idle":
            ret, frame = self.idle_cap.read()
            if not ret:
                self.idle_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return frame
        elif self.frame_status == "listening":
            self.start_audio_track()
            ret, frame = self.listening_cap.read()
            if not ret:
                self.listening_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.frame_status = "idle"
                self.active_audio = None
            return frame
        elif self.frame_status == "talking":
            self.start_audio_track()
            ret, frame = self.talking_cap.read()
            if not ret:
                self.talking_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.frame_status = "idle"
                self.active_audio = None
            return frame

    def start_audio_track(self):
        if pygame.mixer.music.get_busy():
            return

        if self.frame_status == "listening":
            if self.active_audio != self.listening_audio_path:
                self.active_audio = self.listening_audio_path
                pygame.mixer.music.load(self.listening_audio_path)
                print(f"Starting listening audio track ... {self.listening_audio_path}")
                pygame.mixer.music.play()
        elif self.frame_status == "talking":
            if self.active_audio != self.talking_audio_path:
                self.active_audio = self.talking_audio_path
                pygame.mixer.music.load(self.talking_audio_path)
                pygame.mixer.music.play()

    def update_frame_status(self, new_status):
        if new_status == self.frame_status:
            return
        print(f"Updating frame status from {self.frame_status} to {new_status}")
        self.frame_status = new_status

        if self.frame_status == "idle":
            self.fps = self.idle_cap.get(cv2.CAP_PROP_FPS)
        elif self.frame_status == "listening":
            self.fps = self.listening_cap.get(cv2.CAP_PROP_FPS)

        self.fps = 40


def run_video():
    print("Starting Video...")
    frame_handler = FrameHandler(CONFIG)
    frame_handler.fps = 40

    while True:

        frame = frame_handler.get_frame()

        if frame is None:
            continue
        else:
            frame = cv2.resize(frame, (640, 640))
            cv2.imshow("Video", frame)

        if cv2.waitKey(int(1000 / frame_handler.fps)) & 0xFF == ord('q'):
            break
        # TODO: Add a way to update frame status
        # elif RECEIVE_MESSAGE.state == 'listening':
        #     frame_handler.update_frame_status("listening")
        # elif RECEIVE_MESSAGE.state == 'talking':
        #     frame_handler.update_frame_status("talking")

    frame_handler.idle_cap.release()
    frame_handler.listening_cap.release()
    frame_handler.talking_cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_video()