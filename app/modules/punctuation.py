# Safe punctuation module without transformers

class Punctuator:
    def __init__(self, cfg=None):
        self.cfg = cfg or {}

    def restore(self, text: str) -> str:
        if not text:
            return text
        t = text.strip()
        if not t:
            return t
        # Capitalize first letter
        t = t[0].upper() + t[1:]
        # Ensure punctuation
        if t[-1] not in ".!?":
            t += "."
        return t
