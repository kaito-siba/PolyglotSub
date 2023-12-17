import openai
import whisper
import yt_dlp
from srt import Subtitle, compose
import datetime

# APIキーを設定
openai.api_key = "YOUR_OPENAI_API_KEY"


def download_video(url):
    """動画をダウンロードする関数"""
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": "downloaded_audio.%(ext)s",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def transcribe_audio(file_path):
    """音声をテキストに変換する関数"""
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]


def translate_text(text):
    """テキストを翻訳する関数"""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate this to Japanese: {text}",
        max_tokens=1000,
    )
    return response.choices[0].text.strip()


def generate_srt(transcript, start_time=datetime.timedelta(0)):
    """SRT字幕ファイルを生成する関数"""
    subtitles = []
    for i, line in enumerate(transcript.split("\n")):
        end_time = start_time + datetime.timedelta(seconds=5)
        subtitles.append(
            Subtitle(index=i + 1, start=start_time, end=end_time, content=line)
        )
        start_time = end_time
    return compose(subtitles)


def main(url):
    download_video(url)
    transcript = transcribe_audio("downloaded_audio.mp3")
    translated_text = translate_text(transcript)
    srt_content = generate_srt(translated_text)
    with open("subtitles.srt", "w") as file:
        file.write(srt_content)


# 例としてのURL（お前自身で変更すること）
video_url = "https://www.bilibili.com/video/BV1iM4y1y7oA"
main(video_url)
