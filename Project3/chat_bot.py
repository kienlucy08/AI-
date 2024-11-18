'''
File: chat_bot.py
Author: Lucy Kien
Date: 06/06/2024

Python module to create a chat bot
'''

# Imports
from openai import OpenAI
import weaviate
import weaviate.classes as wvc
from preload_database import create_client, create_collection, load_animal_data, load_bot_instructions
from query_database import check_age, check_breed, check_exercise_amount, check_name, check_type, check_price

# create a client object to access the OpenAI API
client = OpenAI()

# all possible types and breeds in the database
types = ["dog", "cat", "bird", "rodent"]
breeds = ["Bernese Mountain Dog", "Retriever", "Beagle", "Bengal", "Siamese", "German Shepherd", "Boxer", "Ragdoll", "Scottish Fold", "Maine Coon",
          "Mutt", "Persian", "Shih Tzu", "Poodle", "Husky", "British Shorthair", "Hamster", "Guinea Pig", "Mouse", "Canary", "Parrot", "English Budgerigar"]
# all names and exercise amounts in the database
names = ["Bear", "Max", "Bella", "Pepper", "Chralie", "Rio", "Pip", "Chester", "Nibbles", "Lola", "Rocky",
         "Sophie", "Shadow", "Cooper", "Molly", "Toby", "Bailey", "Milo", "Daisy", "Oreo", "Luna", "Simba"]
exercise_amounts = ["Low", "Medium", "High"]

# get llm response method which takes the weaviate client, user input and context
def get_llm_response(client: weaviate.WeaviateClient, user_input: str, conversation_context: list) -> str:
    """Gets the llm response from the client using the user input and context.

    Parameters:
        - client (weaviate.WeaviateClient): The OpenAI object used to access the LLM.
        - user_input (str): The users input.
        - conversation_context (list): List of previous messages and rules from the conversation.

    Returns:
        - clientObject (str): The completed llm response.
    """
    # retrieve instructions from the database
    instructions = client.collections.get(
        "AdoptionDatabase")
    # fetch by type instruction
    get_intructions = instructions.query.fetch_objects(
        filters=(wvc.query.Filter.by_property("type").equal('instruction'))
    )

    # construct context from instructions
    context = [instruction.properties["response"]
               for instruction in get_intructions.objects]
    # add the conversation with the user context
    context += conversation_context

    # query the LLM
    llm_client = OpenAI()
    completion = llm_client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': message} for message in context
        ] + [{'role': 'user', 'content': user_input}],
        # temperature is the randomness of your result
        temperature=0
    )
    return completion


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
        response_message = response.choices[0].message.content
        context.append(response_message)
        print("Adoption Bot:", response_message)
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
    conclusionLLM = get_llm_response(
        client, "Please conclude the conversation", context)
    if conclusionLLM.choices:
        conclusionMessage = conclusionLLM.choices[0].message.content
        print(f"\nAdoptionBot: {conclusionMessage}")

def perform_adoption_simulation(client, name, context):
    """Conclude the conversation. This function provides a concluding message for the user when
    they have no more questions.

    Parameters:
        - client (OpenAI Object): The OpenAI object used to access the LLM.
        - context (list): List of previous messages and rules.

    Returns:
        - None
    """
    conclusionLLM = get_llm_response(
        client, f"Please tell the user that they have successfully adopted {name}. Send a bunch of emojis to let them know you are excited. End the conversation", context)
    if conclusionLLM.choices:
        conclusionMessage = conclusionLLM.choices[0].message.content
        context.append(conclude_conversation)
        print(f"\nAdoptionBot: {conclusionMessage}")

# Running chat bot functions

# function to run the chat bot based on user input
def run_chatbot(client: weaviate.WeaviateClient, collection_name: str):
    """Run the chat bot using the user input direct from terminal.

    Parameters:
        - client (weaviate.WeaviateClient): The OpenAI object used to access the LLM.
        - collection_name (str): The name of the collection.

    Returns:
        - None
    """
    # create or get the collection
    collection = create_collection(client, collection_name)

    # load data
    load_animal_data(client, collection, 'Project3/animal.json')
    load_bot_instructions(client, collection)

    # set the context
    context = []
    adoption = False

    # introduction
    print()
    introduction(client, context)

    # User interaction loop
    # User interaction loop
    while not adoption:
        # Get user input
        print()
        user_input = input("You: ")
        context.append(user_input)

        # Get LLM response
        llm_response = get_llm_response(client, user_input, context)
        if llm_response and llm_response.choices:
            llm_response_content = llm_response.choices[0].message.content
            print()
            # Print LLM response
            print(f"Adoption Bot: {llm_response_content}")
            context.append(llm_response_content)

            # Store the interaction
            interaction_data = {
                'type': 'user_interaction',
                'user_input': user_input,
                'bot_response': llm_response_content
            }
            # Insert interaction data into the collection
            collection.data.insert_many([interaction_data])

            # Check for adoption request
            if 'adopt' in user_input.lower():
                # Check if the user mentions a name from the list
                for name in names:
                    if name.lower() in user_input.lower():
                        # Perform adoption simulation for the specified animal
                        perform_adoption_simulation(client, name, context)
                        # Set adoption flag to True
                        adoption = True
                        break
                else:
                    print("Adoption Bot: Please specify the name of the animal you want to adopt.")
            else:
                # check for other queries
                results = []
                if any(t in user_input.lower() for t in types):
                    # query tyle
                    results = check_type(
                        client, collection_name, user_input, types)
                elif any(b in user_input.lower() for b in breeds):
                    # query breed
                    results = check_breed(
                        client, collection_name, user_input, breeds)
                elif any(n in user_input.lower() for n in names):
                    # query name
                    results = check_name(
                        client, collection_name, user_input, names)
                elif any(e.lower() in user_input.lower() for e in exercise_amounts):
                    # query exercise amount
                    results = check_exercise_amount(
                        client, collection_name, user_input, exercise_amounts)
                    # query age
                elif 'age' in user_input.lower() or 'years old' in user_input.lower():
                    results = check_age(client, collection_name, user_input)
                    # query price
                elif 'price' in user_input.lower() or 'dollars' in user_input.lower():
                    results = check_price(client, collection_name, user_input)

                if results:
                    # Get llm response
                    llm_response = get_llm_response(
                        client, f"Talk about the results from the query: {results}", context)
                    if llm_response and llm_response.choices:
                        llm_response_content = llm_response.choices[0].message.content
                        print()
                        print(f"Adoption Bot: {llm_response_content}")
                        context.append(llm_response_content)
                    else:
                        print("Adoption Bot: Error while processing the query results.")
                else:
                    print("Adoption Bot: Please provide more details about the type, breed, name, age, or exercise amount of the animal you are interested in.")

        # Check if user wants to exit
        if user_input.lower() == "exit":
            conclude_conversation(client, context)
            break
        
# the method runs the test prompts file
def run_chatbot_testing(client: weaviate.WeaviateClient, collection_name: str, input_file: str):
    """Run the chat bot using the testing file

    Parameters:
        - client (weaviate.WeaviateClient): The OpenAI object used to access the LLM.
        - collection_name (str): The name of the collection.
        - input_file (str): The test_prompts.txt file.

    Returns:
        - None
    """
    # Create or get the collection
    collection = create_collection(client, collection_name)

    # Load data
    load_animal_data(client, collection, 'Project3/animal.json')
    load_bot_instructions(client, collection)

    # create contex and adoption
    context = []
    adoption = False

    introduction(client, context)

    # read the input file
    with open(input_file, 'r') as file:
        user_inputs = file.read().splitlines()

    # while not adoption
    while not adoption:
        # user interaction loop splits up the file
        for user_input in user_inputs:
            sentences = user_input.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue

                # mimic user interaction 
                print()
                print(f"You: {sentence}")
                context.append(sentence)
            

                # get llmm response
                llm_response = get_llm_response(client, sentence, context)
                if llm_response and llm_response.choices:
                    llm_response_content = llm_response.choices[0].message.content
                    print()
                    # print llm response
                    print(f"Adoption Bot: {llm_response_content}")
                    context.append(llm_response_content)

                    # store the interaction
                    interaction_data = {
                        'type': 'user_interaction',
                        'user_input': sentence,
                        'bot_response': llm_response_content
                    }
                    # insert interaction data into the collection
                    collection.data.insert_many([interaction_data])

                    # exit condition
                    if 'adopt' in sentence.lower():
                        # check if the user mentions a name from the list
                        for name in names:
                            if name.lower() in sentence.lower():
                                # perform adoption simulation for the specified animal
                                perform_adoption_simulation(client, name, context)
                                # set adoption to true
                                adoption = True
                                break
                            else:
                                # get the llm response
                                llm_response = get_llm_response(
                                client, "Ask the user questions about what kind of pet they are looking to adopt or the name of pet they want to adopt", context)
                                if llm_response and llm_response.choices:
                                    llm_response_content = llm_response.choices[0].message.content
                                    print()
                                    print(f"Adoption Bot: {llm_response_content}")
                                    context.append(llm_response_content)
                                    break
                    else:
                        # check for other queries
                        results = []
                        if any(t in sentence.lower() for t in types):
                            # query tyle
                            results = check_type(
                                client, collection_name, sentence, types)
                        elif any(b in sentence.lower() for b in breeds):
                            # query breed
                            results = check_breed(
                                client, collection_name, sentence, breeds)
                        elif any(n in sentence.lower() for n in names):
                            # query name
                            results = check_name(
                                client, collection_name, sentence, names)
                        elif any(e.lower() in sentence.lower() for e in exercise_amounts):
                            # query exercise amount
                            results = check_exercise_amount(
                                client, collection_name, sentence, exercise_amounts)
                            # query age
                        elif 'age' in sentence.lower() or 'years old' in sentence.lower():
                            results = check_age(client, collection_name, sentence)
                            # query price
                        elif 'price' in sentence.lower() or 'dollars' in sentence.lower():
                            results = check_price(client, collection_name, sentence)

                        if results:
                            # get llm response
                            llm_response = get_llm_response(
                                client, f"Talk about the results from the query: {results}", context)
                            if llm_response and llm_response.choices:
                                llm_response_content = llm_response.choices[0].message.content
                                print()
                                print(f"Adoption Bot: {llm_response_content}")
                                context.append(llm_response_content)
                            else:
                                print("Adoption Bot: Error while processing the query results.")
                        else:
                            print("Adoption Bot: Please provide more details about the type, breed, name, age, or exercise amount of the animal you are interested in.")

                # Check if user wants to exit
                if sentence.lower() == "exit":
                    conclude_conversation(client, context)
                    break


# Main function
def main():
    # Create Weaviate client
    weaviate_client = create_client()
    collection_name = "AdoptionDatabase"
    #run_chatbot_testing(weaviate_client, collection_name,'Project3/test_prompts.txt')
    run_chatbot(weaviate_client, collection_name)


if __name__ == "__main__":
    main()
