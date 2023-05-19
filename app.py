import json
import os

import openai
from flask import Flask, redirect, render_template, request, url_for, Response

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
FILE_NAME = os.getenv("FILE_NAME")


def read_json_file(file_name: str) -> dict:
    """
    Reads and returns the FAQ data from a JSON file.

    Args:
        file_name (str): The name of the JSON file.

    Returns:
        dict: The loaded FAQ data from the JSON file.
    """
    with open(file_name, "r", encoding="utf-8") as file:
        faq_data = json.load(file)
    return faq_data


@app.route("/", methods=("GET", "POST"))
def index() -> str | Response:
    """
    Renders the index page and handles the form submission.

    Returns:
        str: The rendered template with the result if available.
    """
    faq_data = read_faq_data(FILE_NAME)

    if request.method == "POST":
        question = request.form["question"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(question, faq_data),
            temperature=1,
            max_tokens=50,  # Tune this parameter for a more descriptive
                            # output, more tokens means higher price
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(question: str, faq_data: dict) -> str:
    """
    Generates the prompt for the OpenAI API based on
    the provided user question and FAQ data.

    Args:
        question (str): The user's question.
        faq_data (dict): The FAQ data.

    Returns:
        str: The generated prompt for the OpenAI API.
    """
    prompt = ""
    for faq_item in faq_data:
        original_question = faq_item["Question_original"]
        prompt += f"Question: {original_question}\n\n"
    prompt += f"User Question: {question}\n\n"
    return prompt
