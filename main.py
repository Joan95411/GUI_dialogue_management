import json
from flask import Flask, render_template, request, jsonify
import traceback
import openai
import ConvertoWool as cw
openai.organization = ""
openai.api_key = ''

# Set up OpenAI API credentials

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('flowchart.html')


@app.route('/get-option-names', methods=['GET'])
def get_option_names():
    with open('templates/prompts.json', 'r') as file:
        prop_data = json.load(file)

    option_names = list(prop_data.keys())

    return jsonify(option_names)


@app.route('/process-input', methods=['POST'])
def process_input():
    with open('templates/prompts.json', 'r') as file:
        prop_data = json.load(file)
    try:
        input_text= request.get_json()['input']
        selected_options = request.get_json()['options']

        full_prompts = ['This is a Dutch dialogue between a medical consultant and a potential patient of hypertrofische cardiomyopathie (HCM). \n'
                        'Please generate more content related to hypertrofische cardiomyopathie based on below requests:']

        i=0
        for option in selected_options:
            i+=1
            if option in prop_data:
                full_prompt = str(i)+". "+prop_data[option]['prompt']
                if full_prompt:
                    full_prompts.append(full_prompt)

        reprompt = '\n'.join(full_prompts)
        if len(selected_options)==0:
            reprompt=''
        prompt =''

        for item in input_text:
            keys = item['keys']
            content = item['content']
            if keys == 'Doc':
                prompt += 'Doctor: ' + content + '\n'
            elif content!="":
                prompt += 'Patient: ' + content + '\n'
        prompt +=reprompt

        print(prompt)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.5
        )

        generated_text = response.choices[0].text.strip()
        return jsonify({'response': generated_text})
    except Exception as e:
        # Capture traceback information
        tb_str = traceback.format_exc()
        # Log the traceback for debugging
        print(tb_str)
        # Include the traceback in the error response
        return jsonify({'error': str(e), 'traceback': tb_str}), 500


@app.route('/role-play', methods=['POST'])
def role_play():
    try:
        input_text= request.get_json()['input']
        msg=[{"role": "system", "content": "You're a patient asking for information and medical suggestions about "
                                              "hypertrofische cardiomyopathie (HCM)."},
                ]
        for item in input_text:
            keys = item['keys']
            content = item['content']
            if keys == 'Doc':
                msg.append({"role": "assistant", "content":content})
            elif content != "":
                msg.append({"role": "user", "content":content})

        print(msg)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=msg
        )
        generated_text = response.choices[0].message.content.strip()
        return jsonify({'response': generated_text})
    except Exception as e:
        # Capture traceback information
        tb_str = traceback.format_exc()
        # Log the traceback for debugging
        print(tb_str)
        # Include the traceback in the error response
        return jsonify({'error': str(e), 'traceback': tb_str}), 500

@app.route('/save-model', methods=['POST'])
def save_model():
    try:
        json_data = request.get_json()
        data = json_data['data']
        with open('templates/model.json', 'w') as file:
            file.write(data)
        wool_file = cw.convert_json_to_wool('templates/model.json')
        with open('templates/model.wool', 'w') as file:
            file.write(wool_file)
        return 'Model JSON saved successfully!', 200
    except Exception as e:
        return str(e), 500

@app.route('/model.json')
def serve_model():
    with open('templates/model.json') as file:
        data = json.load(file)
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=8080,debug=True)
