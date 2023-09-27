def ask_scope_questions(category):
  print("Starting ask_scope_questions from SOWquestions.py")
  project_info = {}

  beginner_questions = [
    (" Can you elaborate on why you decided to do this project and what pain points you were experiencing?",
     "problem_statement",
     "We need to get more leads is why we're doing it.  Our visioon is that we build a system that reliably generates new leads for us to evaluate."
     ),
    (" What is the purpose and vision of your project? It doesn't have to be anything grandiose, we're just trying to get a better understanding of 'why' you are want to do this project.",
     "solution_statement",
     "Success for us is walking away with a strategy we can execute that generates more leads after having worked through a collaborative process with an agency we trust because we know they truly care about our business."
     ),
    (" Do you have any major due-outs and/or milestones in mind already? (Due-outs are significant tasks or milestones that need to be completed. If so, can you outline them here?)",
     "major_due_outs",
     "We know we'll need to build out our ideal customer profile (ICP) and that we'll need to identify a priority list of our target channels."
     )
  ]

  intermediate_questions = [
    (" Can you elaborate on why you decided to do this project and what pain points you were experiencing?",
     "problem_statement",
     "We need to get more leads is why we're doing it.  Our visioon is that we build a system that reliably generates new leads for us to evaluate."
     ),
    (" What is the purpose and vision of your project? It doesn't have to be anything grandiose, we're just trying to get a better understanding of 'why' you are want to do this project.",
     "solution_statement",
     "We need to find a marketing agency that specializes in helping early stage companies like ours build out a marketing strategy and associated plan that we can execute.."
     ),
    (" Any key milestones and/or due-outs already planned?",   
     "major_due_outs",
     "We know we'll need to build out our ideal customer profile (ICP) and that we'll need to identify a priority list of our target channels."
     )
  ]

  expert_questions = [
    (" Can you elaborate on why you decided to do this project and what pain points you were experiencing?",
     "problem_statement",
     "We need to get more leads is why we're doing it.  Our visioon is that we build a system that reliably generates new leads for us to evaluate."
     ),
    (" What is the purpose and vision of your project? Trying to understand the big picture.",
     "solution_statement",
     "We need to find a marketing agency that specializes in helping early stage companies like ours build out a marketing strategy and associated plan that we can execute."
     ),
    (" What deliverables and/or milestones do you envision for a successful collaboration?",
     "major_due_outs",
     "We know we'll need to build out our ideal customer profile (ICP) and that we'll need to identify a priority list of our target channels."
     )
  ]

  if category == 'beginner':
    questions_to_ask = beginner_questions
  elif category == 'intermediate':
    questions_to_ask = intermediate_questions
  elif category == 'expert':
    questions_to_ask = expert_questions
  else:
    print("Couldn't categorize experience level. Asking generic questions.")
    questions_to_ask = beginner_questions

  return questions_to_ask

  # # Ask the questions
  # for question, key, dummy_answer in questions_to_ask:
  #   answer = input(f"{question} ")
  #   # Use dummy answer if the input is blank
  #   if not answer.strip():
  #     answer = dummy_answer
  #   project_info[key] = answer

  # questions_asked = questions_to_ask
  # print("Finishing chat_with_bot from SOW_questions.py")
  # return {'project_info': project_info, 'questions_asked': questions_asked}
