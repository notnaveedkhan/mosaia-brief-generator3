import asyncio
import os

import openai

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
        "content": "You are a helpful assistant specialized in creating project overview briefs that can be handed to a service provider to help in establishing whether the project is a fit for their skills. Your project overview brief will elaborate on every question and answer provided by the user to build a document that is useful and will save them time by building much of the final document for them. Milestones you should include in every project overview brief are: identify 3x possible vendors, vet vendors, generate a comprehensive scope of work with those vendors, get quotes from each vendor, compare quotes and select a vendor, build the solution with them, execute the plan, measure and modify as required. You should not suggest any vendors or service providers in your response. If you believe any information needs to be added to this rough draft project overview brief to be useful for a service provider, then you will use your knowledge of the type of project, problem statement and proposed solution to generate and add that information.Your tone should be professional. When you provide a reply you will format it with H2, H3 and paragraph tags in HTML as appropriate so that it renders nicely on a webpage."
    }, {
        "role": "user",
        "content": rough_request
    }]
    rough_brief = await chat_with_bot(messages, model="gpt-3.5-turbo")
    print("Finishing summarize_with_gpt4 from generate_sow.py")
    print(rough_brief)
    return rough_brief


def get_draft_feedback():
    print("starting get_draft_feedback")
    return "How did we do for a first draft? Anything that you want changed?"


async def improve_sow_with_gpt4(rough_brief, success_questions, feedback):
    print("Starting improve_sow_with_gpt4 from generate_sow.py")
    summary_request = f"Please improve the following project brief: {rough_brief}, {success_questions}, and based on this feedback: {feedback}"
    messages = [{
        "role":
            "system",
        "content":
            "You are a helpful assistant specialized in improving project overview briefs that can be handed to a service provider to help in establishing whether the project is a fit for their skills.  You modify the brief based on feedback provided by the client. When you provide a reply you will format it with H2, H3 and paragraph tags in HTML as appropriate so that it renders nicely on a webpage."
    }, {
        "role": "user",
        "content": summary_request
    }]
    summary = await chat_with_bot(messages, model="gpt-4")
    print("Finishing improve_sow_with_gpt4 from generate_sow.py")
    return summary


async def propose_questions_with_gpt4(brief):
    print("Starting propose_questions_with_gpt4 from generate_sow.py")
    summary_request = f"Please recommend questions I should ask a service provider before hiring them to help me with this project: {brief}"
    messages = [{
        "role":
            "system",
        "content":
            "You are an expert in hiring service providers and know what questions to ask them in order to help identify whether you should hire them. You always ask lots of questions because it's important to find the right fit. When you provide a reply you will format it with H2, H3 and paragraph tags in HTML as appropriate so that it renders nicely on a webpage."
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


project_info = {}
sow_questions = []
experience_info = {}
category = ""
success_questions = []
success_info = {}
rough_task = {}
rough = ""


async def generate_sow(chat_messages):  # add chat_messages as parameter
    length = len(chat_messages)

    print("Starting generate_sow...")

    if (length == 1):
        # Step 0: Ask for summary
        _response = {
            "message": welcome_message(),
            "result": None
        }
        return _response

    elif (length == 2):
        # Step 1: Ask Questions to gather experience info
        _response = {
            "message": experience_question(),
            "result": None
        }
        return _response

    elif (length == 3):
        # Step 2: Ask Questions in Groups and gather info in project_info dict
        global experience_info, category, sow_questions
        question, experience_info, category = ask_experience_questions(chat_messages[2])
        sow_questions = ask_scope_questions(category)
        _response = {
            "message": question + sow_questions[0][0],
            "result": None
        }
        return _response
    elif (length == 4):
        # Step 2: Ask Questions in Groups and gather info in project_info dict
        global project_info
        key = sow_questions[0][1]
        answer = chat_messages[3]
        if not chat_messages[3].strip():
            answer = sow_questions[0][2]
        project_info[key] = answer
        _response = {
            "message": sow_questions[1][0],
            "result": None
        }
        return _response
    elif (length == 5):
        # Step 2: Ask Questions in Groups and gather info in project_info dict
        key = sow_questions[1][1]
        answer = chat_messages[4]
        if not chat_messages[4].strip():
            answer = sow_questions[1][2]
        project_info[key] = answer
        _response = {
            "message": sow_questions[2][0],
            "result": None
        }
        return _response
    elif (length == 6):
        # Step 2: Ask Questions in Groups and gather info in project_info dict
        key = sow_questions[2][1]
        answer = chat_messages[5]
        if not chat_messages[5].strip():
            answer = sow_questions[2][2]
        project_info[key] = answer

        global rough_task
        rough_task = asyncio.create_task(generate_sow_with_gpt4(project_info, sow_questions))

        message = ""
        message += "Great, give me a minute to generate your project brief leveraging LLMs. It can take a few minutes with this much information, but hopefully we're saving you 20 minutes!"

        generic_success = await get_generic_success_keys()

        message += "<br/>While the project scope is getting built, let’s take a moment to talk about what else is needed for a successful engagement. Based on our experience working with hundreds of projects, we know these 3 keys are critical for you to succeed."
        message += "<br/>" + generic_success
        message += "<br/>We also know that 44% of projects fail due to lack of a proper scope of work, but you're on track to have one built for you, so all good there!"

        message += "<br/>Now that we know what it takes to be successful, let's make sure you set up for success by asking a few more questions:"

        global success_questions
        success_questions = ask_success_questions(category)
        _response = {
            "message": "<br/>".join([message, success_questions[0][0]]),
            "result": None
        }
        return _response
    elif length == 7:
        global success_info
        key = success_questions[0][1]
        success_info[key] = chat_messages[6]
        _response = {
            "message": success_questions[1][0],
            "result": None
        }
        return _response
    elif length == 8:
        key = success_questions[1][1]
        success_info[key] = chat_messages[7]
        _response = {
            "message": success_questions[2][0],
            "result": None
        }
        return _response
    elif length == 9:
        key = success_questions[2][1]
        success_info[key] = chat_messages[8]

        message = "We'll come back to these keys shortly, but your project overview brief is almost ready so let's take a look!"
        message += "<br/>"

        global rough
        rough = await rough_task

        draft_feedback_message = "How did we do for a first draft? Anything that you want changed?"
        message += draft_feedback_message

        _response = {
            "message": message,
            "result": {
                "rough": rough,
                "brief": None,
                "proposed": None
            }
        }
        return _response
    elif length == 10:
        feedback = chat_messages[9]
        brief = await improve_sow_with_gpt4(rough, success_questions, feedback)

        message = "This should be enough to get you started on your conversations with service providers."
        message = message + "<br/>" + "I'm also going to generate some recommended questions that you should consider asking any prospective service providers."

        proposed = await propose_questions_with_gpt4(brief)
        _response = {
            "message": message,
            "result": {
                "rough": rough,
                "brief": brief,
                "proposed": proposed
            }
        }
        return _response


def welcome_message():
    print("Starting opening question in generate_sow.py")
    welcome_message = "Welcome to the Mosaia Project Overview Generator!<br/>We're building the best platform leveraging multiple LLMs to help you scope projects more quickly.<br/>It cuts down on the time needed to build the document to hand a service provider by 90%.<br/>Let's get started!"
    summary_statement = "What's the one line summary of this project? e.g. Hire an agency to build us a go to market plan."
    return ("<br/>".join([welcome_message, summary_statement]))


def experience_question():
    return "Have you done a project like this before? (yes/no) "