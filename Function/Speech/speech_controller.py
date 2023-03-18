from Function.Speech import talking


class SpeechController:
    LISTENING_RATE = 16000
    LISTENER_CHUNK_SIZE = 1024 * 4
    MAX_BUFFER_LENGTH = 40000
    NEW_BUFFER_LENGTH = 20000

    def __init__(self):
        self.talking_pipeline = talking.TalkingController()


def concatenate(a, b):
    if a is None:
        return b
    return np.concatenate([a, b])


