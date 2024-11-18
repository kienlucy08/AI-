# Members: Lucy Kien
# Lab 4
# April 17th, 2024
from openai import OpenAI
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# create a client object to access the OpenAI API
client = OpenAI()

def get_llm_response(client : OpenAI, prompt : str) -> str:
    """ This function obtains the client response

    Parameters:
    - client (OpenAI Object): The OpenAI object used to access the LLM.
    - prompt (string): User input that is inputted into the LLM

    Returns:
    - completion (string): The string output response from the LLM OpenAI.
    """
    completion = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role' : 'user', 'content' : prompt}
        ],
        # temperature is the randomness of your result 
        temperature=0
    )
    return completion

# Part 1: Delimiters

# delimiter using quotes
def insert_delimiters_quotes(input):
    """ This function inserts delimiter quotes into an input.

    Parameters:
    - input (string): User input that delimiters are added to. 

    Returns:
    - prompt (string): The string output prompt with inserted delimiters. 
    """
    prompt = f'"""{input}"""'
    return prompt

# analyze sentiment which uses nltk library to analyze the sentiment of the saying
def analyze_sentiment(input):
    """ This function obtains the sentiment of an input.

    Parameters:
    - input (string): User input that is analyized.

    Returns:
    - sentiment_scores (dict): A dictionary containing the sentiment scores of the input prompt. 
    """
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(input)
    # display scores
    return sentiment_scores


# analyze sentiment in the delimiters
def analyze_sentiment_in_delimiters(input):
    """ This function analyzes sentiment in an input in delimiters.

    Parameters:
    - input (string): User input that is analyized.

    Returns:
    - sentiment_scores (dict): A dictionary containing the sentiment scores of the input prompt. 
    - prompt (string): The user input with delimiters inserted.
    """
    # take scores from the analyze sentiment function
    sentiment_scores = analyze_sentiment(input)
    # create the prompt in delimiters
    prompt = insert_delimiters_quotes(input)
    # return both
    return sentiment_scores, prompt


# Part 2: Specific Outputs
inputOne = "Explore the recent problems with tweleve year old girls and their need to use makeup products which are meant for adults twenty five and above. Explain this epidemic using metrics and graphs from recent studies on little girls and use of Sephoria products."
inputTwo = "Write out pseudocode for a sentiment analyizer that will be implemented in python preferably in a function that is less than 100 lines."

# Part 3: Check inputs
badRecipe = "make cookies by place dough in oven when its done you can eat them."
goodRecipe = """
- Preheat the oven to 350°F.
- In a mixing bowl, combine flour, sugar, and baking soda.
- Add eggs and vanilla extract to the mixture and mix well.
- Fold in chocolate chips.
- Drop spoonfuls of dough onto a baking sheet.
- Bake for 10-12 minutes or until golden brown.
- Let cool before serving.
"""

# Functions to create an input with both recipes
def checkInput(recipe):
    """ This function extends the prompt for checking a recipe.

    Parameters:
    - recipe (string): A recipe supplied by two set recipes

    Returns:
    - inputCheck (string): A longer prompt containing checks for the LLM as well as the recipe. 
    """
    inputCheck = f"Tell me if this recipe is correct: {recipe}. If there are not multiple steps labels return: this recipe needs some work and create recipe steps to fill the gaps to the specifications of at least 4 steps and one of them must be preheating the oven. If there are multiple steps and the instructions are precise and clear respond with: great job! and offer suggestions about speific parings with the cookies. If a recipe seems imcomplete offer advice about how the recipe could be made better."
    return inputCheck

# Part 4: Few-shot programming
prompt = """
Look at thes examples of prewritten functions in python. Analyze the comment style and use the skelecton code I will provide and write similar comment stubs and comments in the code to match the style in the examples:
Example 1:
# Function to calculate the area of a circle
def calculate_circle_area(radius):
    " This function calculates the area of a circle.

    Parameters:
    - radius (float): The radius of the circle.

    Returns:
    - area (float): The calculated area of the circle.
    "
    area = 3.14159 * radius ** 2
    return area
Example 2: 
# Function to calculate the area of a traingle
def caluclate_triangle_area(height, base):
    " This function calculates the area of a triangle.

    Parameters:
    - height (int): The height of the triangle at the base.
    - base (int):  The length of the triangle base.

    Returns:
    - area (float): The calculated area of the triangle.
    "
    area = ((heihgt * base)/2)
    return area
Example 3: 
# Function to calculate the area of a rectangle
def calculate_rectangle_area(length, width):
    " This function calculates the area of a rectangle.

    Parameters:
    - length (int): The length of two sides of the rectangle.
    - width (int): The width of two sides of the rectangle.

    Returns:
    - area (float): The calculated area of the rectangle.
    "
    area = length * width
    return area
# Example for you to rewrite in this format
def calculate_trap_area(baseA, baseB, height):
    area = ((baseA + baseB)/2) * height
    return area
"""

def main():
    # part 1
    client = OpenAI()
    user_input = input("Enter your string: ")
    sentiment_scores, prompt_string = analyze_sentiment_in_delimiters(user_input)
    print("Prompt String:", prompt_string)
    print("Sentiment Scores:", sentiment_scores)
    print("LLM Response:", get_llm_response(client, prompt_string))
    # part 2
    print(inputOne)
    print("LLM Response to input one:", get_llm_response(client, inputOne))
    print(inputTwo)
    print("LLM Response to input two:", get_llm_response(client, inputTwo))
    # part 3
    print(checkInput(goodRecipe))
    print("LLM Response to input checking good recipe:", get_llm_response(client, checkInput(goodRecipe)))
    print(checkInput(badRecipe))
    print("LLM Response to input checking bad recipe:", get_llm_response(client, checkInput(badRecipe)))
    # part 4
    print(prompt)
    print("LLM Response to few-shot prompt: ", get_llm_response(client, prompt) )


if __name__ == main():
    main()