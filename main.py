import typer
import os
from dotenv import load_dotenv
from google import genai
from typing import Annotated
from pypdf import PdfReader

load_dotenv()

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEYがありません")
client = genai.Client(api_key=api_key)

app = typer.Typer()

MODEL = "models/gemini-flash-lite-latest"

# PDFを読み込む
def read_pdf(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    MAX_CHARS = 10000
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text[:MAX_CHARS]


# クイズを生成する
@app.command()
def generate_quiz(
    file_path: Annotated[str, typer.Argument()] = "file/sample.pdf",
    num_questions: Annotated[int, typer.Argument(min=1, max=10)] = 2):
    text = read_pdf(file_path)
    prompt = f"""
    {text}に関する4択クイズを{num_questions}個作成してください。
    出力形式:
    問題1: [問題文]
    A) [選択肢]
    B) [選択肢]
    C) [選択肢]
    D) [選択肢]
    正解: [A/B/C/D]
    解説: [簡単な説明]
    """
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    print(response.text)

if __name__ == "__main__":
    app()