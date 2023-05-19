# Python helper for Forex Tester

This is a python helper for asking openai api a question related to Forex Tester  

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.
    ```bash
   $ git clone https://github.com/DavidGlusch/helper-forex.git
   ```

3. Navigate into the project directory:

   ```bash
   $ cd helper-gpt
   ```

4. Create a new virtual environment:

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

7. Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

8. Upload your file for prompting and set its name to `.env` file

9. Run the app:

   ```bash
   $ flask run
   ```

You should now be able to access the app at [http://localhost:5000](http://localhost:5000)! 
