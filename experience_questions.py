import openai
import time  # Add this line


def chat_with_bot(messages, model="gpt-4", retries=3, delay=5):
  print("Starting chat_with_bot from experience_questions.py")
  while retries > 0:
    try:
      response = openai.ChatCompletion.create(model=model, messages=messages)
      return response['choices'][0]['message']['content']
    except openai.error.ServiceUnavailableError:
      print("OpenAI server is overloaded or not ready yet. Retrying...")
      retries -= 1
      time.sleep(delay)
  return "Failed to connect to OpenAI server after multiple retries."


def ask_experience_questions(answer):
  experience_info = {}

  # question = "Have you done a project like this before? (yes/no) "
  key = "experience_statement"

  # answer = input(f"{question} ").strip().lower()
  answer = answer.strip().lower()
  experience_info[key] = answer

  if answer == "yes":
    category = "expert"
    question = (
      "Fantastic, you're a pro at this!  We'll try to move quickly with the goal of saving you time."
    )
  elif answer == "no":
    category = "beginner"
    question = (
      "You came to the right place as we'll provide you with recommendations and guidance at every step of the process to make it easier."
    )
  else:
    # time to make an API call to OpenAI to infer the experience level if the answer is not "yes" or "no".
    api_question = f"Is the experience level described as '{answer}' best categorized as beginner, intermediate, or expert?"
    messages = [{
      "role":
      "system",
      "content":
      "You are a helpful assistant specialized in categorizing experience levels.  You only give one-word answers."
    }, {
      "role": "user",
      "content": api_question
    }]
    category = chat_with_bot(messages).strip().lower()
    if category == "beginner":
      question = (
        "You came to the right place as we'll provide you with recommendations and guidance at every step of the process to make it easier."
      )
    elif category == "intermediate":
      question = (
        "Nice! You've got some experience under your belt!  We'll try to provide you with a tailored experience that gives you the option to get more help when you need it, but doesn't slow you down."
      )
    elif category == "expert":
      question = (
        "Fantastic, you're a pro at this!  We'll try to move quickly with the goal of saving you time."
      )
    else:
      question = ("Hmm, couldn't quite get that. Let's keep going.")

  return question, experience_info, category


def ask_experience_questions_copy():
  experience_info = {}

  question = "Have you done a project like this before? (yes/no) "
  key = "experience_statement"

  answer = input(f"{question} ").strip().lower()
  experience_info[key] = answer

  if answer == "yes":
    category = "expert"
    print(
      "Fantastic, you're a pro at this!  We'll try to move quickly with the goal of saving you time."
    )
  elif answer == "no":
    category = "beginner"
    print(
      "You came to the right place as we'll provide you with recommendations and guidance at every step of the process to make it easier."
    )
  else:
    # time to make an API call to OpenAI to infer the experience level if the answer is not "yes" or "no".
    api_question = f"Is the experience level described as '{answer}' best categorized as beginner, intermediate, or expert?"
    messages = [{
      "role":
      "system",
      "content":
      "You are a helpful assistant specialized in categorizing experience levels.  You only give one-word answers."
    }, {
      "role": "user",
      "content": api_question
    }]
    category = chat_with_bot(messages).strip().lower()
    if category == "beginner":
      print(
        "You came to the right place as we'll provide you with recommendations and guidance at every step of the process to make it easier."
      )
    elif category == "intermediate":
      print(
        "Nice! You've got some experience under your belt!  We'll try to provide you with a tailored experience that gives you the option to get more help when you need it, but doesn't slow you down."
      )
    elif category == "expert":
      print(
        "Fantastic, you're a pro at this!  We'll try to move quickly with the goal of saving you time."
      )
    else:
      print("Hmm, couldn't quite get that. Let's keep going.")

  return experience_info, category
