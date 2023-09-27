from flask import Flask, request, jsonify

# Brief builder imports
import os
import openai
import time
import concurrent.futures
import asyncio

from artifact_generator import generate_artifacts_list
from SOWquestions import ask_scope_questions
from experience_questions import ask_experience_questions
from success_questions import ask_success_questions
from success_questions import get_generic_success_keys
# Import the main function from the generate_sow module
from generate_sow import generate_sow

# Existing imports
from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
import json
from answer_questions import answer_question

app = Flask(__name__)


@app.route('/<path:path>')
def serve_static(path):
  # Serve file from public directory
  return send_from_directory('public', path)


@app.route('/')
def index():
  print("app.route('/') starting")
  return send_from_directory('public', 'index.html')


@app.route('/ask', methods=['POST'])
async def ask():
  print("app.route('/ask') starting")
  # call generate_sow
  welcome_msg, message, etc = await generate_sow(transcript)

  # package up response
  response_data = {"bot": welcome_msg + "\n" + message}
  
  # Get message from request body
  data = json.loads(request.data)
  
  # Extract transcript from data
  transcript = data['transcript']
  
  # Check if transcript is a list
  if not isinstance(transcript, list):
      # If transcript is a simple string, promote it to a list
      transcript = [transcript]
  
  # Call generate_sow function with transcript as an argument
  print("Preparing to call generate_sow...")
  
  answer = asyncio.run(generate_sow(transcript))
  
  response_data = {"bot": answer}
  print(response_data)
  return jsonify(response_data)


@app.route('/generateSOW', methods=['POST'])
def generate_SOW_endpoint():
    print("app.route('/generateSOW') starting")
    try:
        data = request.json
        chat_messages = data.get("project_info", [])
        
        output = asyncio.run(generate_sow(chat_messages))
        
        print("Successfully called generate_sow.")
        return jsonify({"success": True, "output": output})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.errorhandler(Exception)
def error(e):
  print("error: " + str(e))
  print(request.url)
  return "error! " + str(e)


def run():
  app.run(host='0.0.0.0')

