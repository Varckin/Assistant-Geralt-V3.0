from pydub import AudioSegment
import whisper, warnings
from pathlib import Path
from Logging.logger import get_logger


logger = get_logger(__name__)
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

class STT:
    def __init__(self):
        self.model = whisper.load_model("base")

    def convert_voice_to_text(self, source_path, destination_path) -> str:
        try:
            sound = AudioSegment.from_file(source_path)
            sound = sound.set_channels(1).set_frame_rate(16000)
            sound.export(destination_path, format="wav")

            result = self.model.transcribe(str(destination_path))
            self.check_files()
            return result['text'], result['language']
        except Exception as e:
            logger.error(e)

    def check_files(self):
        tmp_dir = Path('tmp')
        files = [f for f in tmp_dir.iterdir() if f.is_file()]
        if len(files) > 40:
            logger.info(f"In folder {tmp_dir} {len(files)} files, i delete all...")
            for file in files:
                try:
                    file.unlink()
                except Exception as e:
                    logger.error(e)
        else:
            logger.info(f"In folder - {len(files)} files, dont delete...")
