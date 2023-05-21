import json
import os
import nltk
import openai
from flask import Flask, redirect, render_template, request, url_for, Response

from utils import get_chunks, get_best_fitting_question, get_similar_questions

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
FILE_NAME = os.getenv("FILE_NAME")

nltk.download("punkt")


def read_json_file(file_name: str) -> dict:
    """
    Reads and returns the data from a JSON file.

    Args:
        file_name (str): The name of the JSON file.

    Returns:
        dict: The loaded data from the JSON file.
    """
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def get_openai_response(question: str, data: dict) -> str:
    """
    Generates the OpenAI API response based on the user question.

    Args:
        question (str): The user's question.
        data (dict): The data.

    Returns:
        str: The generated response from the OpenAI API.
    """

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(question, data),
        temperature=0.1,
        max_tokens=50
    )
    return response.choices[0].text


def get_data() -> dict:
    """
    Retrieves data from a JSON file.

    Returns:
        dict: The data from the JSON file.
    """
    return read_json_file(FILE_NAME)


@app.route("/", methods=("GET", "POST"))
def index() -> str | Response:
    """
    Renders the index page and handles the form submission.

    Returns:
        str: The rendered template with the result if available.
    """

    if request.method == "POST":
        question = request.form["question"]
        result = get_openai_response(question, get_data())
        return redirect(url_for("index", result=result))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(question: str, data: dict) -> str:
    """
    Generates the prompt for the OpenAI API based on
    the provided user question and data.

    Args:
        question (str): The user's question.
        data (dict): The data.

    Returns:
        str: The generated prompt for the OpenAI API.
    """

    answer = ""
    notes = ""
    chunks = get_chunks(data)
    similarities = get_similar_questions(chunks, question)
    best_fitting_question = get_best_fitting_question(similarities, chunks)

    for item in data:
        question_alternatives = item["Question_original_alternatives"]
        question_short_alternatives = item["Question_short_alternatives"]

        if (best_fitting_question in question_alternatives
                or best_fitting_question in question_short_alternatives):
            notes += item["Notes"]
            answer += item["Answer_plain_text"]
            break

    prompt = (f"You are a Helper for Forex Tester\n "
              f"User question: f{best_fitting_question}\n"
              f"{notes}\n")
    # f"ANSWER EXAMPLE:{answer}")

    return prompt
