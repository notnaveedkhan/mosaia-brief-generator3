from flask import jsonify
import os
import openai
from openai.error import RateLimitError
import time
import concurrent.futures
import asyncio
from artifact_generator import generate_artifacts_list
from SOWquestions import ask_scope_questions
from experience_questions import ask_experience_questions
from success_questions import ask_success_questions
from success_questions import get_generic_success_keys

openai.api_key = os.environ.get("OPENAI_API_KEY")


def opening_question(summary_question):
  return summary_question


def generate_sow_points(project_info, questions_asked):
  sow_points = []
  for question, key, _ in questions_asked:  # add _ to hold the dummy answers
    if key in project_info:
      sow_points.append(f"Question: {question}\nAnswer: {project_info[key]}")
  return sow_points


async def summarize_with_gpt4(sow_points):
  print("Starting summarize_with_gpt4 from generate_sow.py")
  rough_request = f"Please elaborate on the following points: {sow_points}"
  messages = [{
    "role":
    "system",
    "content":
    "You are a helpful assistant specialized in creating project overview briefs that can be handed to a service provider to help in establishing whether the project is a fit for their skills.  Your project overview brief will elaborate on every question and answer provided by the user to build a document that is useful and will save them time by building much of the final document for them. Milestones you should include in every project overview brief are: identify 3x possible vendors, vet vendors, generate a comprehensive scope of work with those vendors, get quotes from each vendor, compare quotes and select a vendor, build the solution with them, execute the plan, measure and modify as required. You should not suggest any vendors or service providers in your response.  If you believe any information needs to be added to this rough draft project overview brief to be useful for a service provider, then you will use your knowledge of the type of project, problem statement and proposed solution to generate and add that information.Your tone should be professional and use plain language as defined at https://www.plainlanguage.gov/. You will not make up or hallucinate any information.  Do not say 'Note: As an AI assistant, I am unable to provide specific recommendations for vendors or service providers. It is recommended to thoroughly research potential vendors, review their portfolios, and request references to ensure they are the right fit for your project.' or anything like that."
  }, {
    "role": "user",
    "content": rough_request
  }]
  rough_brief = await chat_with_bot(messages, model="gpt-4")
  print("Finishing summarize_with_gpt4 from generate_sow.py")
  print(rough_brief)
  return rough_brief


def get_draft_feedback():
  print("starting get_draft_feedback")
  return "How did we do for a first draft? Anything that you want changed?"


async def improve_sow_with_gpt4(rough_brief, feedback):
  print("Starting improve_sow_with_gpt4 from generate_sow.py")
  summary_request = f"Please improve the following project brief: {rough_brief} and based on this feedback: {feedback}"
  messages = [{
    "role":
    "system",
    "content":
    "You are a helpful assistant specialized in improving project overview briefs that can be handed to a service provider to help in establishing whether the project is a fit for their skills.  You modify the brief based on feedback provided by the client."
  }, {
    "role": "user",
    "content": summary_request
  }]
  summary = await chat_with_bot(messages, model="gpt-4")
  print(summary)
  print("Finishing improve_sow_with_gpt4 from generate_sow.py")
  return summary


async def propose_questions_with_gpt4(brief):
  print("Starting propose_questions_with_gpt4 from generate_sow.py")
  summary_request = f"Please recommend questions I should ask a service provider before hiring them to help me with this project: {brief}"
  messages = [{
    "role":
    "system",
    "content":
    "You are an expert in hiring service providers and know what questions to ask them in order to help identify whether you should hire them. You always ask lots of questions because it's important to find the right fit."
  }, {
    "role": "user",
    "content": brief
  }]
  proposed = await chat_with_bot(messages, model="gpt-4")
  print("Finishing propose_questions_with_gpt4 from generate_sow.py")
  return proposed


async def chat_with_bot(messages, model="gpt-4", retries=3, delay=5):
  while retries > 0:
    try:
      response = openai.ChatCompletion.create(model=model, messages=messages)
      return response['choices'][0]['message']['content']
    except openai.error.ServiceUnavailableError:
      retries -= 1
      await asyncio.sleep(delay)
  return "Failed to connect to OpenAI server after multiple retries."


async def generate_sow_with_gpt4(project_info, questions_asked):
  sow_points = generate_sow_points(project_info, questions_asked)
  summary2 = await summarize_with_gpt4(sow_points)  # Use 'await' here
  return summary2


async def generate_sow(chat_messages):  # add chat_messages as parameter
  # return None
  # print("Starting generate answer...")
  # messages = [{"role": "user", "content": chat_messages[1]['text']}]
  # print("========chat_messages==========")
  # print(messages)
  # print("========chat_messages==========")

  # try:
  #   response = openai.ChatCompletion.create(model="gpt-4", messages=messages)
  #   print("=========response============")
  #   print(response)
  #   print("=========response============")
  #   content = response.choices[0].message["content"]
  # except RateLimitError:
  #   content = "The server is experiencing a high volume of request. Please try again later."

  # return content

  print("chat_messages==============", chat_messages)
  print("length of chat_messages==========", len(chat_messages))

  print("Starting generate_sow...")
  welcome_message = "Welcome to the Mosaia Project Overview Generator! We're building the best platform leveraging multiple LLMs to help you scope projects more quickly. It cuts down on the time needed to build the document to hand a service provider by 90%. Let's get started!"

  # Step 0: Ask for summary

  print("Starting opening question in generate_sow.py")
  summary_statement = opening_question(
    "What's the one line summary of this project? e.g. Hire an agency to build us a go to market plan."
  )
  print(summary_statement)
  # Step 1: Ask for rough summary

  # User provides feedback to summary_question
  chat_messages_summary = chat_messages

  # Step 1: Ask Questions to gather experience info
  experience_info, category = ask_experience_questions()

  # Step 2: Ask Questions in Groups and gather info in project_info dict
  result = ask_scope_questions(category)
  project_info = result.get("project_info", {})
  questions_asked = result.get("questions_asked", [])

  message = ""
  message += "\nGreat, give me a minute to generate your project brief leveraging LLMs. It can take a few minutes with this much information, but hopefully we're saving you 20 minutes!"

  generic_success = await get_generic_success_keys()

  message += "\nWhile the project scope is getting built, let’s take a moment to talk about what else is needed for a successful engagement. Based on our experience working with hundreds of projects, we know these 3 keys are critical for you to succeed."
  message += "\n" + generic_success
  message += "\nWe also know that 44% of projects fail due to lack of a proper scope of work, but you're on track to have one built for you, so all good there!"

  message += "\nNow that we know what it takes to be successful, let's make sure you set up for success by asking a few more questions:"

  rough = await generate_sow_with_gpt4(project_info, questions_asked)

  feedback = get_draft_feedback()

  brief = await improve_sow_with_gpt4(rough, feedback)

  message += "\n" + brief

  message += "\nThis should be enough to get you started on your conversations with service providers."
  message += "\nI'm also going to generate some recommended questions that you should consider asking any prospective service providers."

  final_brief = await propose_questions_with_gpt4(brief)
  proposed_questions = (
    f"{message}\n\nRecommended questions to ask a service provider before hiring them:\n{proposed}"
  )

  # construct the full response
  full_response = (
    welcome_message + "\n" + message + "\n" + summary_statement + "\n" +
    chat_messages_summary + "\n" + experience_info + "\n" + category + "\n" +
    project_info + "\n" + questions_asked + "\n" + generic_success + "\n" +
    rough + "\n" + proposed_questions + "\n" + brief + "\n" + final_brief
    # etc...
  )

  print("Finished generate_sow.")

  return full_response
