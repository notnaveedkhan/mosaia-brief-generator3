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


client_messages = []


@app.route('/ask', methods=['POST'])
async def ask():
  print("app.route('/ask') starting")
  # return "success"
  # Get message from request body
  data = json.loads(request.data)

  # Extract transcript from data
  transcript = data['transcript']
  if (transcript == "welcome_message"):
    if (len(client_messages) == 0):
      if not isinstance(transcript, list):
        transcript = [{'sender': 'user', 'text': transcript}]
      client_messages.append(transcript[-1]["text"])
    else:
      client_messages.clear()
      client_messages.append(transcript)
  else:
    if not isinstance(transcript, list):
      transcript = [{'sender': 'user', 'text': transcript}]
    client_messages.append(transcript[-1]["text"])

  # Check if transcript is a list
  # if not isinstance(transcript, list):
  #   # If transcript is a simple string, promote it to a list
  #   transcript = [{'sender': 'user', 'text': transcript}]

  # client_messages.append(transcript[-1]["text"])

  # Call generate_sow function with transcript as an argument
  print("Preparing to call generate_sow...")
  # loop = asyncio.get_event_loop()
  # future = asyncio.ensure_future(generate_sow(transcript))
  # answer = loop.run_until_complete(future)

  # answer = await generate_sow(transcript)
  answer = await generate_sow(client_messages)

  response_data = {"bot": answer}
  if (len(client_messages) == 10):
    client_messages.clear()
  # response_data = {"bot": "I am a student."}
  # print('response_data', response_data)
  return jsonify(response_data)


@app.route('/')
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


# if __name__ == '__main__':
#   app.run(host='0.0.0.0', port=5001, debug=True)


def run():

  app.run(host='0.0.0.0')
  # app.run(host='0.0.0.0', debug=True)
