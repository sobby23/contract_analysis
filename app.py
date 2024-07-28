import os
from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import pandas as pd
import docx2txt
import json

app = Flask(__name__)

# OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    api_key=api_key,
)


# Load contract text
def load_contract_text(file_path):
    return docx2txt.process(file_path)


def extract_conditions(text):
    prompt = f"""
    Assume the Amendments in the below Contract Text, which may include price multipliers, are agreed and signed by both the parties.

    Please extract all relevant terms and conditions from the following contract along with the respective amendments which may include price multipliers. 
    Include specific constraints such as budget limits, types of allowable work, deadlines, payment terms, and any other relevant details. 
    The conditions should have clear explanation with examples if any in the Contract text.

    Provide the response strictly in JSON format with appropriate keys for each section.

    Contract Text:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert contract analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1512,
        temperature=0.0,
        top_p=1.0
    )

    conditions_json = response.choices[0].message.content
    print("Raw response from OpenAI API:", conditions_json)  # Debug print

    # Clean and parse the JSON
    conditions_json = conditions_json.strip().strip('```').strip('json').strip()

    try:
        conditions = json.loads(conditions_json)
        return conditions
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {}


# Load tasks data from a CSV file
def load_tasks_data(file_path):
    return pd.read_excel(file_path)


def analyze_tasks(tasks_df, conditions):
    # Prepare the data to be sent to OpenAI
    tasks_list = tasks_df.to_dict(orient='records')
    data = {
        "contract_conditions": conditions,
        "tasks": tasks_list
    }

    prompt = f"""
        Please understand the contract terms and conditions, which is provided below, including any amendments or modifications to the original terms which is very important. The contract conditions include specific details such as budget limits, allowable work types, deadlines, and other constraints. Amendments may adjust these conditions with additional rules or multipliers. 

        The Task List, which is also provided below, needs to be analyzed for compliance with these conditions and any related amendments. For each task:
        Determine if the amount is withing with the contract conditions, including all amendments and specific adjustments. This includes considering any specific multipliers made to any section. If a task is non-compliant, specify 'Non-Compliant' and provide the reasons for non-compliance, referencing specific contract conditions and/or secific amendments if any.

        Provide the response strictly in JSON format with the following keys:
        - 'task': The task description.
        - 'amount': The cost of the task.
        - 'compliance_status': 'Compliant' or 'Non-Compliant'.
        - 'reason': The reason for compliance or non-compliance. Keep this value blank if the task is 'Compliant' and no specific reason is necessary.       
        
        
        Contract Conditions: {json.dumps(data['contract_conditions'], indent=2)}
        Task List: {json.dumps(data['tasks'], indent=2)}
        """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a compliance checker analyzing tasks against contract conditions."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=3012,
        temperature=0.0,
        top_p=1.0
    )

    analysis_result = response.choices[0].message.content.strip().strip('```').strip('json').strip()
    print("Analysis result:", analysis_result)  # Debug print

    try:
        # Converting the response to a JSON object
        results = json.loads(analysis_result)
        print("Json Loads Analysis res 111 ========== ")
        print(results)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        results = {"error": "Failed to parse the response from OpenAI"}

    return results


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    contract_file = request.files['contract']
    tasks_file = request.files['tasks']

    contract_text = load_contract_text(contract_file)
    conditions = extract_conditions(contract_text)
    # print("Conditions ============= ")
    print(conditions)
    tasks_df = load_tasks_data(tasks_file)
    # print("Tasks ============= ")
    print(tasks_df)
    analysis_results = analyze_tasks(tasks_df, contract_text)
    # print("Analysis Results ============= ")
    print(analysis_results)

    return jsonify({
        'contract_conditions': conditions,
        'analysis_results': analysis_results
    })


if __name__ == '__main__':
    app.run(debug=True)
