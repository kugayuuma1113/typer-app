import typer
import os
from dotenv import load_dotenv
from google import genai
from typing import Annotated,List
from pypdf import PdfReader
from pydantic import BaseModel,Field

# gemini apiの設定
load_dotenv()
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEYがありません")
client = genai.Client(api_key=api_key)
MODEL = "models/gemini-flash-lite-latest"

app = typer.Typer()


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

# クイズのモデル定義
class Choice(BaseModel):
    A:str = Field(description="選択肢A")
    B:str = Field(description="選択肢B")
    C:str = Field(description="選択肢C")
    D:str = Field(description="選択肢D")

class Quiz(BaseModel):
    question:str = Field(description='問題の内容')
    choices:Choice = Field(description="選択肢")
    answer:str = Field(description="問題の正解記号（A/B/C/D）")
    explanation:str = Field(description="問題の解説")

class QuizList(BaseModel):
    quizzes:List[Quiz] = Field(description="クイズのリスト")

def quiz_generatar(file_path:str,num:int):
    text = read_pdf(file_path)
    prompt = f"""{text}を元に、４たくクイズを{num}門作って下さい。
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
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": QuizList.model_json_schema(),
    },)
    quiz = QuizList.model_validate_json(response.text)
    return quiz.quizzes

@app.command()
def generate_quiz(
    file_path: Annotated[str, typer.Argument()] = "file/sample.pdf",
    num_questions: Annotated[int, typer.Argument(min=1, max=10)] = 2):
    quizzes = quiz_generatar(file_path,num_questions)
    correct_answers = 0
    print(f"クイズを{num_questions}問出題します。")
    for i,quiz in enumerate(quizzes):
        print(f"問題{i}: {quiz.question}")
        print(f"A) {quiz.choices.A}")
        print(f"B) {quiz.choices.B}")
        print(f"C) {quiz.choices.C}")
        print(f"D) {quiz.choices.D}")
        your_answer = typer.prompt("あなたの回答 (A/B/C/D)").upper()
        if your_answer == quiz.answer:
            print("正解です！")
            correct_answers += 1
        else:
            print(f"不正解です。正解は{quiz.answer}です。")
            print(f"解説: {quiz.explanation}")
        print("--------------------------------")
    print(f"あなたの正解数: {correct_answers}/{num_questions}")


if __name__ == "__main__":
    app()