from gtts import gTTS
from pydub import AudioSegment
from pathlib import Path
import uuid
from Logging.logger import get_logger


logger = get_logger(__name__)

class TTS:
    def convert_text_to_voice(self, text: str, lang: str) -> Path:
        self.check_files()
        TMP_DIR = Path("tmp")
        TMP_DIR.mkdir(exist_ok=True)

        name_file = uuid.uuid4().hex
        mp3_path = TMP_DIR / f"TTS_{name_file}.mp3"
        ogg_path = TMP_DIR / f"TTS_{name_file}.ogg"

        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(str(mp3_path))

            audio = AudioSegment.from_mp3(mp3_path)
            audio.export(ogg_path, format="ogg", codec="libopus")
            return ogg_path
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
