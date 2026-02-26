import asyncio
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

import agent
from models import db, Drug, SideEffectReport
from agent import local_tools, get_mcp_tools

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drugs.db'

db.init_app(app)
agent.flask_app = app

with app.app_context():
    db.create_all()

mcp_tools = asyncio.run(get_mcp_tools())
all_tools = local_tools + mcp_tools

llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL"), 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

agent = create_agent(llm, tools=all_tools, system_prompt='''You are a helpful assistant for finding side effects of drugs.

Available tools:
- list_drugs: List all drugs in the database
- create_drug: Create a new drug in the database
- delete_drug: Delete a drug and all its side effects from the database
- create_side_effect: Add a side effect report for a drug
- list_side_effects: List all side effects for a given drug
- delete_side_effect: Delete a specific side effect from a drug

So the procedure should always be: 
1. List all drugs in the database
2. If the drug already exists, list all side effects for that drug
3. Get new side effects from the internet
4. If there is any new side effect, that is not in the database, create a new side effect report for that drug in the DB
''')

@app.route('/')
def home():
    drugs = Drug.query.all()
    return render_template('home.html', drugs=drugs)

@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get('query')
    result = asyncio.run(agent.ainvoke({'messages': user_query}))

    response = result['messages'][-1].content

    return jsonify({'response': 'response'})


if __name__ == '__main__':
    app.run(debug=True)