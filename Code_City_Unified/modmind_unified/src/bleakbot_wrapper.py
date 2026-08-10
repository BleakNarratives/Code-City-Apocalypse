import pickle
import os

class BleakBotCheckpoint:
    def __init__(self, filepath="data/bleakbot_checkpoint.pkl"):
        self.filepath = filepath
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading checkpoint: {e}")
                return {'last_batch': 0, 'total_batches': 0}
        return {'last_batch': 0, 'total_batches': 0}

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, 'wb') as f:
                pickle.dump(self.data, f)
            print(f"Checkpoint saved to {self.filepath}")
        except Exception as e:
            print(f"Error saving checkpoint: {e}")

    def get_progress(self):
        return self.data.get('last_batch', 0), self.data.get('total_batches', 0)

    def update_progress(self, current_batch, total_batches=None):
        self.data['last_batch'] = current_batch
        if total_batches is not None:
            self.data['total_batches'] = total_batches
        self.save()

if __name__ == "__main__":
    # Test
    bot = BleakBotCheckpoint("data/bleakbot_checkpoint.pkl")
    print(f"Current Progress: {bot.get_progress()}")
