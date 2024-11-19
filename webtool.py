from flask import Flask, request, jsonify, render_template,redirect
import openai
import pandas as pd

# Set up OpenAI API credentials
openai.api_key = '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'

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-input', methods=['POST'])
def process_input():
    input_text = request.get_json()['input']

    # Call OpenAI API with the user input as the prompt
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=input_text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    generated_text = response.choices[0].text.strip()

    return jsonify({'response': generated_text})

df = pd.read_excel('Q&A.xlsx', sheet_name='Sheet1')
questions = df['Questions'].tolist()
answers = df['Answers'].tolist()
lines = [f"Patient: {q}\nDoctor: {a}\n" for q, a in zip(questions, answers)]

# @app.route('/')
# def index():
#     return render_template('editor.html.j2', lines=enumerate(lines))


@app.route('/add_line', methods=['POST'])
def add_line():
    lines.append("")
    return jsonify({'index': len(lines) - 1})


@app.route('/update_line', methods=['POST'])
def update_line():
    line_index = int(request.form.get('line_index', -1))
    new_content = request.form.get('new_content', '')

    if line_index >= 0 and line_index < len(lines):
        lines[line_index] = new_content

    return redirect('/')


@app.route('/move_line', methods=['POST'])
def move_line():
    line_index = int(request.form['line_index'])
    direction = request.form['direction']

    if direction == 'up':
        if line_index > 0:
            lines[line_index], lines[line_index - 1] = lines[line_index - 1], lines[line_index]
    elif direction == 'down':
        if line_index < len(lines) - 1:
            lines[line_index], lines[line_index + 1] = lines[line_index + 1], lines[line_index]

    return 'success'

if __name__ == '__main__':
    app.run(debug=True)
