'''
File: query_database.py
Author: Lucy Kien
Date: 06/06/2024

Python module to query the loaded database for specifc properties
'''

import weaviate
import weaviate.classes as wvc
import re

# query functions

def query_animal_type(client: weaviate.WeaviateClient, collection_name: str, animal_type: str):
    """Query the database for animals of a specific type.

    Parameters:
        - weaviate_client (weaviate.WeaviateClient): The Weaviate client.
        - animal_type (str): The type of animal to query.

    Returns:
        - list: List of animals of the specified type.
    """
    # get the collection
    query = client.collections.get(collection_name)
    # query by type
    result = query.query.fetch_objects(
        filters=(wvc.query.Filter.by_property("animal_type").equal(animal_type))
    )
    # return
    return result.objects


def query_breed(client: weaviate.WeaviateClient, collection_name: str, breed: str):
    """Query the database for animals of a specific breed.

    Parameters:
        - weaviate_client (weaviate.WeaviateClient): The weaviate client.
        - breed (str): The breed of the animal to query.

    Returns:
        - list: List of animals of the specified breed.
    """
    # get the collection
    query = client.collections.get(collection_name)
    # query the breed
    result = query.query.fetch_objects(
        filters=(wvc.query.Filter.by_property("breed").equal(breed))
    )
    return result.objects

def query_name(client: weaviate.WeaviateClient, collection_name: str, name: str):
    """Query the database for animals with a specific name.

    Parameters:
        - client (weaviate.WeaviateClient): The weaviate client.
        - collection_name (str): The name of the collection.
        - name (str): The name of the animal to query.

    Returns:
        - list: List of animals with the specified name.
    """
    # get the collection
    query = client.collections.get(collection_name)
    # query the collection
    result = query.query.fetch_objects(
        filters=(wvc.query.Filter.by_property("name").equal(name))
    )
    return result.objects

def query_age(client: weaviate.WeaviateClient, collection_name: str, age: int = None, age_range: tuple = None, similarity_threshold: float = 0.2):
    """Query the database for animals with a specific age or within a specified age range.

    Parameters:
        - client (weaviate.WeaviateClient): The Weaviate client.
        - collection_name (str): The name of the collection.
        - age (int, optional): The exact age of the animal to query. Defaults to None.
        - age_range (tuple, optional): A tuple specifying the age range (min_age, max_age) to query. Defaults to None.
        - similarity_threshold (float, optional): The similarity threshold for querying ages similar to the specified age. Defaults to 0.2.

    Returns:
        - list: List of animals with the specified age or within the specified age range.
    """
    # get the collection
    query = client.collections.get(collection_name)
    # store result
    result = []

    try:
        # if there is an age range
        if age_range:
            # set min and max
            min_age, max_age = age_range
            # get the results
            result = query.query.fetch_objects(
                filters=(
                    wvc.query.Filter.by_property("age").greater_or_equal(min_age) &
                    wvc.query.Filter.by_property("age").less_or_equal(max_age)
                )
            )
        elif age is not None:
            # if no age range specified, attempt to find animals with exact age
            result = query.query.fetch_objects(
                filters=(wvc.query.Filter.by_property("age").equal(age))
            )
            if not result.objects:
                # if no exact match found, search for ages within a certain threshold
                min_age_threshold = max(0, age - similarity_threshold * age)
                max_age_threshold = age + similarity_threshold * age
                result = query.query.fetch_objects(
                    filters=(
                        wvc.query.Filter.by_property("age").greater_or_equal(min_age_threshold) &
                        wvc.query.Filter.by_property("age").less_or_equal(max_age_threshold)
                    )
                )
        else:
            # no age or age range found
            raise ValueError("Either age or age_range must be provided.")

    # exception
    except Exception as e:
        print(f"Error while querying age: {e}")

    # return the result or empty
    return result.objects if result else []

def query_price(client: weaviate.WeaviateClient, collection_name: str, price: float = None, price_range: tuple = None, similarity_threshold: float = 0.2):
    """Query the database for animals with a specific price or within a specified price range.

    Parameters:
        - client (weaviate.WeaviateClient): The weaviate client.
        - collection_name (str): The name of the collection.
        - price (float, optional): The exact price of the animal to query.
        - price_range (tuple, optional): A tuple specifying the price range (min_price, max_price) to query.
        - similarity_threshold (float, optional): The similarity threshold for querying prices similar to the specified price. Defaults to 0.2.

    Returns:
        - list: List of animals with the specified price or within the specified price range.
    """
    # get the collection
    query = client.collections.get(collection_name)
    # store the result
    result = []

    try:
        # if there is a price range set the min and max
        if price_range:
            min_price, max_price = price_range
            # query the collection
            result = query.query.fetch_objects(
                filters=(
                    wvc.query.Filter.by_property("price").greater_or_equal(min_price) &
                    wvc.query.Filter.by_property("price").less_or_equal(max_price)
                )
            )
        elif price is not None:
            # if no price range attempt to find animals with exact price
            result = query.query.fetch_objects(
                filters=(wvc.query.Filter.by_property("price").equal(price))
            )
            if not result.objects:
                # if no exact match found search for prices within a certain threshold
                min_price_threshold = max(0, price - similarity_threshold * price)
                max_price_threshold = price + similarity_threshold * price
                result = query.query.fetch_objects(
                    filters=(
                        wvc.query.Filter.by_property("price").greater_or_equal(min_price_threshold) &
                        wvc.query.Filter.by_property("price").less_or_equal(max_price_threshold)
                    )
                )
        else:
            # if there are no price or price range
            raise ValueError("Either price or price_range must be provided.")

    # exception to prevent breaking
    except Exception as e:
        print(f"Error while querying price: {e}")

    # return the objects or empty
    return result.objects if result else []


def query_exercise_amount(client: weaviate.WeaviateClient, collection_name: str, exercise_amount: str):
    """Query the database for animals with a specific exercise amount.

    Parameters:
        - client (weaviate.WeaviateClient): The weaviate client.
        - collection_name (str): The name of the collection.
        - exercise_amount (str): The exercise amount of the animal to query.

    Returns:
        - list: List of animals with the specified exercise amount.
    """
    # get the collection
    query = client.collections.get(collection_name)
    # query the exercise amount
    result = query.query.fetch_objects(
        filters=(wvc.query.Filter.by_property("exercise_amount").equal(exercise_amount))
    )
    return result.objects

# check type methods to be called in the chat bot file

def check_type(client: weaviate.WeaviateClient, collection_name: str, user_input: str, animal_types: list):
    """Check if a type of animal has been input in the user input then query the information.

    Parameters:
        - client (weaviate.WeaviateClient): The weaviate client.
        - collection_name (str): The name of the collection.
        - user_input (str): The user's input.
        - animal_types (list): list of all possible types.

    Returns:
        - List: List of animals matching the specified animal type.
    """

    # check if any animal type is mentioned in the user input
    for animal_type in animal_types:
        if animal_type in user_input.lower():
            # if animal type mentioned, query animals of that type
            return query_animal_type(client, collection_name, animal_type)

    # if no animal type mentioned, return an empty list
    return []


def check_breed(client: weaviate.WeaviateClient, collection_name: str, user_input: str, breeds: list):
    """Check if a breed has been mentioned in the user input then query the information.

    Parameters:
        - client (weaviate.WeaviateClient): The weaviate client.
        - collection_name (str): The name of the collection.
        - user_input (str): The user's input.
        - reeds (list): list of all possible breeds at the shelter.

    Returns:
        - List: List of animals matching the specified breed.
    """
    # go through the breeds in the list
    for breed in breeds:
        if breed.lower() in user_input.lower():
            # query the breeds if found
            return query_breed(client, collection_name, breed)

    # if no breed mentioned, return an empty list
    empty_response = print("There is no breeds of that kind at this shelter.")
    return empty_response

def check_name(client: weaviate.WeaviateClient, collection_name: str, user_input: str, names: list):
    """Check if a name has been mentioned in the user input then query the information.

    Parameters:
        - client (weaviate.WeaviateClient): The weaviate client.
        - collection_name (str): The name of the collection.
        - user_input (str): The user's input.
        - names (list): List of all possible names at the shelter.

    Returns:
        - List: List of animals matching the specified name.
    """
    # go through the list of names
    for name in names:
        if name.lower() in user_input.lower():
            # if it appears than query it
            return query_name(client, collection_name, name)

    # if no name mentioned return an empty list
    empty_response = print("There is no names that you specified at this shelter.")
    return empty_response

def check_age(client: weaviate.WeaviateClient, collection_name: str, user_input: str):
    """Check if an age or age range has been mentioned in the user input then query the information.

    Parameters:
        - client (weaviate.WeaviateClient): The weaviate client.
        - collection_name (str): The name of the collection.
        - user_input (str): The user's input.

    Returns:
        - list: List of animals matching the specified age or age range.
    """
    # get age or age range from user input and query the database
    age_range_match = re.search(r'(\d+)\s*-\s*(\d+)', user_input)
    age_match = re.search(r'\b(\d+)\b', user_input)
    
    # if there is a match set the min and max
    if age_range_match:
        min_age, max_age = map(int, age_range_match.groups())
        # query
        return query_age(client, collection_name, age_range=(min_age, max_age))
    elif age_match:
        # if an age match query
        age = int(age_match.group(1))
        return query_age(client, collection_name, age=age)
    
    # if no age mentioned, return an empty list with a message
    print("Adoption Bot: No age range mentioned in the input.")
    return []

def check_exercise_amount(client: weaviate.WeaviateClient, collection_name: str, user_input: str, exercise_amounts: list):
    """Check if an exercise amount has been mentioned in the user input then query the information.

    Parameters:
        - client (weaviate.WeaviateClient): The weaviate client.
        - collection_name (str): The name of the collection.
        - user_input (str): The user's input.
        - exercise_amounts (list): List of all possible exercise amounts.

    Returns:
        List: List of animals matching the specified exercise amount.
    """
    # go through the given list and if it is found query the database
    for exercise_amount in exercise_amounts:
        if exercise_amount.lower() in user_input.lower():
            return query_exercise_amount(client, collection_name, exercise_amount)
    
    # if no exercise amount found return an empty list
    empty_response = print("There is no exercise amount at that level.")
    return empty_response

def check_price(client: weaviate.WeaviateClient, collection_name: str, user_input: str):
    """Check if a price or price range has been mentioned in the user input then query the information.

    Parameters:
        - client (weaviate.WeaviateClient): The weaviate client.
        - collection_name (str): The name of the collection.
        - user_input (str): The user's input.

    Returns:
        - List: List of animals matching the specified price or price range.
    """
    # get price or price range from user input and query the database
    price_range_match = re.search(r'(\d+)\s*-\s*(\d+)', user_input)
    price_match = re.search(r'\b(\d+)\b', user_input)
    
    # if there is a matching price range set the min and max
    if price_range_match:
        min_price, max_price = map(float, price_range_match.groups())
        # query
        return query_price(client, collection_name, price_range=(min_price, max_price))
    # if price match
    elif price_match:
        # query
        price = float(price_match.group(1))
        return query_price(client, collection_name, price=price)
    
    # if no price found return an empty list with a message
    print("Adoption Bot: There are no animals listed for the price mentioned.")
    return []

