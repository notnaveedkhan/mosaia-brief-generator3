import json
import asyncio


async def get_generic_success_keys():
  generic_success_keys = [
    "- Having an explicit DRI who is the primary point of contact and ‘owns’ the project from start to finish.",
    "- Communicating any requirements around timeline.",
    "- Understanding if you already have a budget locked for this project."
  ]
  # Convert list to a formatted string for each key on a new line
  formatted_keys = '\n'.join(generic_success_keys)
  return formatted_keys


def ask_success_questions(category):

  success_info = {}

  beginner_questions = [
    # Client and DRI Details
    ("Who is the client Directly Responsible Individual (DRI) that will be the main point of contact?",
     "client_dri"),
    ("What’s your ideal timeline to complete this project?", "timeline"),
    ("Is there a set budget? We won’t share it with the vendor, but we ask to get a better understanding of which vendor is the best fit.",
     "set_budget"),
  ]
  expert_questions = [
    ("Who is the client Directly Responsible Individual (DRI) that will be the main point of contact?",
     "client_dri"),
    ("What’s your ideal timeline to complete this project?", "timeline"),
    ("Is there a set budget? We won’t share it with the vendor, but we ask to get a better understanding of which vendor is the best fit.",
     "set_budget"),
  ]
  if category == 'beginner':
    questions_to_ask = beginner_questions
  elif category == 'expert':
    questions_to_ask = expert_questions
  else:
    print("Couldn't categorize experience level. Asking beginner questions to be safe.")
    questions_to_ask = beginner_questions  # Fallback to beginner questions

  return questions_to_ask

  # for question, key in questions_to_ask:
  #   answer = input(f"{question} ")
  #   success_info[key] = answer

  # questions_asked = questions_to_ask

  # return {'project_info': success_info, 'questions_asked': questions_asked}
