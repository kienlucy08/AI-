'''
File: chat_bot.py
Author: Lucy Kien
Date: 05/08/2024

Python module to create a chat bot
'''

# Imports
from openai import OpenAI
import re

# create a client object to access the OpenAI API
client = OpenAI()

# Comprehensive Chat Bot instructions.
chatBotInstructions = [
    "Medical Help Chatbot is here to help with mental health and minor symptom tracking. It will ask users questions about their health and offer advice and simple remedies.",
    "Please use this introduction only when prompted to introduce yourself: 'Medical Bot: Hello! I am your medical chat bot, how can I assist you today? Ask any medical or mental health related questions.'. Only say this once.",
    "Please start every response with a 'Medical Bot:' followed by the llm's response. This indicates that the bot is talking",
    "When concluding an interaction with a user always say: 'Medical Bot: Thank you for using Medical Help Chatbot, I hope I was of help! If you have any more medical-related questions in the future, feel free to ask. Take care!'",
    "Please take the users inputted symptoms or questions. For example: 'I have a fever and headache'. If nothing has been inputted yet, just ask the user to put in a symptom or question.",
    "You will provide the user with potential remedies or ideas to improve their health based on their symptoms. Immediately after ask about when the symptoms appeared and how bad they are",
    "If the symptoms have presisted past 2-3 days recommend visiting the doctor for further help",
    "If the condition seems serious or includes life-threatening symptoms included in the life threathening symptom list like chest pain or difficulty breathing, You will recommend contacting emergency services at 911 immediately.",
    "You may ask you further questions to gain a better understanding of your condition. For instance, when did your symptoms start? Are they getting worse?",
    "If the user has any mental health concerns, tell the user they are free to share. You are here to provide support. In this case the user can talk about other subjects that are effecting their mental health. This is an exception to medical related question rule.",
    "Once a question is answered follow up the answered question asking if the user has any more questions",
    "If they are feeling suicidal, you can offer assistance and provide resources such as the Suicide Prevention Lifeline.",
    "If there any questions not related to medical problems, mental health, or symptoms simply say: 'Medical Bot: This is not a subject I can assist in, if you have any medical related questions ask away!",
    "If a user inputs No or has no more questions regarding their health say:'Medical Bot: Thank you for using Medical Help Chatbot, I hope I was of help!'",
    "Do not make up interactions for testing. Simply use the file test sentences that are provided and respond to them. You're being too smart."
]

# List of life threatening symptoms
life_threatening_symptoms = [
    "severe chest pain",
    "difficulty breathing",
    "severe bleeding",
    "loss of consciousness",
    "seizures",
    "sudden severe headache",
    "severe abdominal pain",
    "difficulty speaking",
    "vision loss",
    "severe allergic reaction",
    "choking",
    "major trauma",
    "sudden confusion",
    "severe burns",
    "overdose",
    "heart attack",
    "stroke",
    "hopeless"
]

def get_llm_response(client: OpenAI, prompt: str, context=None) -> str:
    """This function obtains the client response

    Parameters:
    - client (OpenAI Object): The OpenAI object used to access the LLM.
    - prompt (string): User input that is inputted into the LLM.
    - context (list): List of previous messages and rules.

    Returns:
    - completion (string): The string output response from the LLM OpenAI.
    """
    if context is None:
        context = []
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': message} for message in context
        ] + [{'role': 'user', 'content': prompt}],
        # temperature is the randomness of your result
        temperature=0
    )
    return completion

# Run chatbot function that is used for testing the test prompts in the test_prompts.txt file
def run_chatbot_testing(client, context, symptomsInput=None, followUpInput=None):
    """Run the medical chatbot based on user input tests written in test_prompts.txt

    This function initiates the chatbot interaction and manages the conversation flow.

    Parameters:
    - client (OpenAI Object): The OpenAI object used to access the LLM.
    - context (list): List of previous messages and rules.
    - symptomsInput (string): The initial medical related question for the bot to answer
    - followUpInput (list): List of follow-up questions or inputs.

    Returns:
    - None
    """
    # questions answered starts as false when starting a convo
    questionAnswered = False

    while not questionAnswered:

        # response message introduction from the bot
        responseMessage = introduction(client, context)

        # error tracking
        if not responseMessage:
            return

        if not symptomsInput:
            print("Please provide valid symptoms or questions.")
            return
        
        # print user input
        print("\nUser: ", symptomsInput)

        # Handle life threatening symtpoms
        if handle_life_threatening_symptoms(client, symptomsInput, context):
            conclude_conversation(client, context)
            return

        # get the response for the symptoms 
        symptomResponse = get_llm_response(client, f"Respond to the symptom input do not introduce yourself: {symptomsInput}", context)
        if symptomResponse.choices:
            responseMessage = symptomResponse.choices[0].message.content
            # print the response and append it to the list
            print(f"\n{responseMessage}")
            context.append(symptomsInput)
            context.append(responseMessage) 

        # handle any follow up questions from the bot and user
        follow_up_responses_testing(client, context, responseMessage, followUpInput)

        # end the loop
        questionAnswered = True

# run chatbot function that works with live user input instead of pre-written test prompts. 
def run_chatbot(client, context):
    """Run the medical chatbot. This function will initiate the bot and user interactions
    To potentially solve any medical or mental health issues. This function is based on user
    input not pre-specified tests

    Parameters:
    - client (OpenAI Object): The OpenAI object used to access the LLM.
    - context (list): List of previous messages and rules.

    Returns:
    - None
    """
    questionAnswered = False

    while not questionAnswered:
        
        # get the introduction from the bot
        responseMessage = introduction(client, context)
        # error checking
        if not responseMessage:
            return
        
        # use the live user input as input
        symptomsInput = input("\nUser: ")

        if not symptomsInput:
            print("Please provide valid symptoms or questions.")
            return

        # handle life threathening symptoms
        if handle_life_threatening_symptoms(client, symptomsInput, context):
            conclude_conversation(client, context)
            return

        # get the symptom response
        symptomResponse = get_llm_response(client, f"Respond to the symptom input do not introduce yourself: {symptomsInput}", context)
        if symptomResponse.choices:
            responseMessage = symptomResponse.choices[0].message.content
            # print it and append it to the context lsit
            print(f"\n{responseMessage}")
            context.append(symptomsInput)
            context.append(responseMessage) 

        # get the follow up input
        followUpInput = input("\nUser: ")
        # handle the follow up input
        follow_up_responses_with_user_input(client, context, responseMessage, followUpInput)

        # end the loop
        questionAnswered = True


# Helper functions
# ----------------

# Introduction method that will write the introduction said by the medical help bot.
def introduction(client, context):
    """Introduce the chatbot. This function generates an introduction for the chatbot.

    Parameters:
    - client (OpenAI Object): The OpenAI object used to access the LLM.
    - context (list): List of previous messages and rules.

    Returns:
    - responseMessage (string): The introductory message from the LLM.
    """
    # get the introduction based on the rules
    response = get_llm_response(client, "Introduce yourself.", context)
    if response.choices:
        # return the response
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    else:
        # error tracking
        print("Unexpected reaction from bot, try again")
        return None
    
# conclusion method to write the conclusion from the bot.
def conclude_conversation(client, context):
    """Conclude the conversation. This function provides a concluding message for the user when
    they have no more questions.

    Parameters:
    - client (OpenAI Object): The OpenAI object used to access the LLM.
    - context (list): List of previous messages and rules.

    Returns:
    - None
    """
    conclusionLLM = get_llm_response(client, "Conclude the conversation", context)
    if conclusionLLM.choices:
        conclusionMessage = conclusionLLM.choices[0].message.content
        print(f"\n{conclusionMessage}")  

# Life threatening symptoms method that will track if any life threatening symptoms are specified by the user.
def handle_life_threatening_symptoms(client, symptomsInput, context):
    """Handle life-threatening symptoms. This function checks for life-threatening symptoms 
    in the user's input and generates an appropriate response if any are found.

    Parameters:
    - client (OpenAI Object): The OpenAI object used to access the LLM.
    - symptoms_input (string): The user's input symptoms.
    - context (list): List of previous messages and rules.

    Returns:
    - (bool): True if life-threatening symptoms are found and false otherwise.
    """
    # go through the list of life_threatening_symptoms
    for symptom in life_threatening_symptoms:
        # if there is a symptom in the input produce an appropriate response from the bot
        if symptom in symptomsInput.lower():
            lifeThreatenResponse = get_llm_response(client, f"This is a life-threatening condition: {symptomsInput}", context)
            if lifeThreatenResponse.choices:
                responseMessage = lifeThreatenResponse.choices[0].message.content
                # print the response and append it to the lsit
                print(f"\n{responseMessage}")
                context.append(symptomsInput)
                context.append(responseMessage) 
                # return true
                return True
    return False

# Method to handle follow up responses from the user and bot.
def follow_up_responses_testing(client, context, responseMessage, followUpInput):
    """Handle follow-up responses. This function processes follow-up questions from the user 
    and generates appropriate responses from the LLM.

    Parameters:
    - client (OpenAI Object): The OpenAI object used to access the LLM.
    - context (list): List of previous messages and rules.
    - responseMessage (string): The response from the chatbot.
    - followUpInput (list): List of follow-up questions or inputs.

    Returns:
    - None
    """
    # if there is a question in the response
    if "?" in responseMessage:
        # go through the followUp input in the list
        for followUp in followUpInput:
            print("\nUser: ", followUp)
            # check for life threatening symptoms
            for symptom in life_threatening_symptoms:
                if symptom in followUp.lower():
                    followUpResponse = get_llm_response(client, f"This is a life-threatening condition: {followUp}", context)
                    followUpResponseMessage = followUpResponse.choices[0].message.content
                    print(f"\n{followUpResponseMessage}")
                    conclude_conversation(client, context)
                    # exit if there is one
                    return
            # if not get a response from the follow up questions
            followUpResponse = get_llm_response(client, f"Answer the follow up question in relation to the context: {followUp}", context)
            followUpResponseMessage = followUpResponse.choices[0].message.content
            # print and append to the list
            print(f"\n{followUpResponseMessage}")
            context.append(followUp)
            context.append(followUpResponseMessage)
        # while there are still questions in the follow up response from the bot
        while "?" in followUpResponseMessage:
            for followUp in followUpInput:
                print("\nUser: ", followUp)
                # check life threatening symptoms
                for symptom in life_threatening_symptoms:
                    if symptom in followUp.lower():
                        followUpResponse = get_llm_response(client, f"This is a life-threatening condition: {followUp}", context)
                        followUpResponseMessage = followUpResponse.choices[0].message.content
                        print(f"\n{followUpResponseMessage}")
                        conclude_conversation(client, context)
                        return
                followUpResponse = get_llm_response(client, f"Answer the follow up question in relation to the context: {followUp}", context)
                followUpResponseMessage = followUpResponse.choices[0].message.content
                print(f"\n{followUpResponseMessage}")
                context.append(followUp)
                context.append(followUpResponseMessage)     

# function to handle follow up when there is user input
def follow_up_responses_with_user_input(client, context, responseMessage, followUp):
    """Handle follow-up responses. This function processes follow-up questions from the live user 
    and generates appropriate responses from the LLM.

    Parameters:
    - client (OpenAI Object): The OpenAI object used to access the LLM.
    - context (list): List of previous messages and rules.
    - responseMessage (string): The response from the chatbot.
    - followUp (string): The follow up question from the live user. 

    Returns:
    - None
    """
    # if there is a question in the response
    if "?" in responseMessage:
        # check the life threatening symptoms
        for symptom in life_threatening_symptoms:
            if symptom in followUp.lower():
                # get the response
                followUpResponse = get_llm_response(client, f"This is a life-threatening condition: {followUp}", context)
                followUpResponseMessage = followUpResponse.choices[0].message.content
                # print and conclude the conversation
                print(f"\n{followUpResponseMessage}")
                conclude_conversation(client, context)
                return
        followUpResponse = get_llm_response(client, f"Answer the follow up question in relation to the context: {followUp}", context)
        followUpResponseMessage = followUpResponse.choices[0].message.content
        print(f"\n{followUpResponseMessage}")
        context.append(followUp)
        context.append(followUpResponseMessage)
        responseMessage = followUpResponseMessage
        # while there are still questions in the follow up response from the bot
        while "?" in followUpResponseMessage:
            followUp = input("\nUser: ")
            # check life threatening symptoms
            for symptom in life_threatening_symptoms:
                if symptom in followUp.lower():
                    # return if life threatening
                    followUpResponse = get_llm_response(client, f"This is a life-threatening condition: {followUp}", context)
                    followUpResponseMessage = followUpResponse.choices[0].message.content
                    print(f"\n{followUpResponseMessage}")
                    conclude_conversation(client, context)
                    return
            # other response to keep the conversation instead
            followUpResponse = get_llm_response(client, f"Answer the follow up question in relation to the context: {followUp}", context)
            followUpResponseMessage = followUpResponse.choices[0].message.content
            # print and append
            print(f"\n{followUpResponseMessage}")
            context.append(followUp)
            context.append(followUpResponseMessage)    


# Test chat bot method which will test the chat bot using test_prompts.txt
def test_chatbot():
    """Test the medical chatbot. This function runs tests on the chatbot using predefined prompts
    in test_prompts.txt to ensure its functionality.

    Parameters:
    - None

    Returns:
    - None
    """
    # create context
    context = []
    context = chatBotInstructions.copy()  # Initialize context with instructions

    # open the test_prompts file
    with open("Project2/test_prompts.txt", "r") as file:
        test_prompts = file.readlines()

    # for the prompts split the sentences and create an inital and a followup questions list
    for prompt in test_prompts:
        print("\nTesting with prompt:", prompt.strip())
        sentences = re.split(r'[.!?]', prompt.strip())
        symptoms_input = sentences[0].strip()
        additional_sentences = [sentence.strip() for sentence in sentences[1:] if sentence.strip()]
        # run the chat bot
        run_chatbot_testing(client, context, symptomsInput=symptoms_input, followUpInput=additional_sentences)
        print("-" * 50)


# Main
def main():
    context = chatBotInstructions.copy()
    run_chatbot(client, context)


if __name__ == "__main__":
    main()
