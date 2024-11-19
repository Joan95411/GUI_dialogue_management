import openai
import time
import pandas as pd
# Set up OpenAI API credentials
openai.api_key = "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"
# Load Excel file
df = pd.read_excel('Q&A.xlsx',sheet_name='Sheet1')


# Define a function to ask the AI a question
def ask_question(prompt):
    if len(prompt) > 2048:
        prompt = prompt[-2048:]
    completions = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    message = completions.choices[0].text.strip()
    return message


chat_log = ""
initial_prompt = f"Give me more dialogues between patient and doctor about Hypertrophic cardiomyopathy like below:\n"
for i in range(2, 3):
    initial_prompt += f"\nPatient: {df.iloc[i]['Questions']}\nDoctor: {df.iloc[i]['Answers']}\n"

print(initial_prompt)
chat_log += initial_prompt + "\n"
num_exchanges = 0  # initialize a counter for the number of exchanges
while num_exchanges < 3:  # break out of the conversation after 3 exchanges
    # ask AI for a response
    response = ask_question(chat_log)
    # print AI's response
    if response:  # only print non-empty responses
        print(response)
        chat_log += response  # add the exchange to the conversation log
        num_exchanges += 1  # increment the counter
    # wait for a second before asking the next question
    time.sleep(1)
