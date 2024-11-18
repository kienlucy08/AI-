
---

# Animal Adoption Help Bot with Lucy

Welcome to the Animal Adoption Help Bot, designed to assist users in finding their perfect pet. This README will have all the rules and guidelines for interacting with the Animal Adoption Help Bot.

## Table of Contents

- [Purpose](#purpose)
- [Rules](#rules)
- [Usage](#usage)
- [Tests](#tests)

## Purpose

The Animal Adoption Help Bot is supposed to provide support and guidance to users looking to adopt pets. It creates a mock animal shelter database that the users can than browse through. It offers recommendations based on the user's preferences and assists in finding suitable pets for adoption.

## Rules

1. **Introduction**: The bot will introduce itself with the message: "Adoption Bot: Hello! I'm here to help you find the perfect animal companion. Ask me any questions related to pet adoption."
2. **Response Format**: Every response from the bot or the user will start with "Adoption Bot:" or "User:", depending on whose turn it is to chat. This format indicates who is speaking and creates a flow of conversation.
3. **User Input**: Users should provide their preferences or questions in a clear and concise manner. For example, "I'm looking for a playful dog named Max."
4. **Follow-up Questions**: The bot may ask follow-up questions to better understand the user's preferences. Users should respond appropriately to these inquiries. All interactions within one session will be recorded to memory.
5. **Budget Constraints**: If the user has budget constraints, they can specify a price range, and the bot will recommend pets within that range.
6. **Age Preferences**: Users can specify age preferences for pets, and the bot will provide recommendations accordingly.
7. **Breed Preferences**: Users can specify breed preferences for pets, and the bot will provide recommendations accordingly.
8. **Name Preferences**: If a user knows of an animal name they are looking for they can also input the name and the animal should appear. 
9. **Animal Preferences**: Users can specify animal types as well searching for dogs, cats, birds, or rodents. Any other animals are not in the database so the bot will tell the user to search for specific types. 
10. **Compatibility**: If users have specific requirements such as compatibility with children or other pets, they can mention them, and the bot will suggest suitable pets based on the pets description.
11. **Adoption**: To adopt a pet the user simply needs to say: I would like to adopt {name_of_pet} and that will exit the program.
12. **Exit**: Users can end the interaction by typing "Exit" as well

## Usage

1. Begin the interaction by providing your preferences or questions about pet adoption.
2. Follow the bot's prompts and respond to any follow-up questions it may ask.
3. If you find a pet you're interested in adopting, you can indicate your choice to the bot.
4. Once you're done with your questions or have found a pet, you can end the interaction by typing "Exit."

## Tests

The following tests have been used to ensure the functionality of the Animal Adoption Help Bot:

1. **Test 1**: "Hi, who are you?"

Test 1 tests the introduction of the bot.

2. **Test 2**: "I am looking for a dog. A Boxer would be great. I like Cooper."
3. **Test 3**: "I am looking for a dog named Max."
4. **Test 4**: "I am looking for a Bengal Cat."

Tests 2-4 tests the ability to access the database with specifc queries.

5. **Test 5**: "I want a bear."

Test 5 tests to make sure the adoption bot doesn't suggest an odd or unusual animal. 

6. **Test 6**: "I'm looking to adopt a pet. What pets are available for adoption?"
7. **Test 7**: "Can you tell me about the dogs available for adoption?"
8. **Test 8**: "I'm interested in adopting a cat. Which cats do you have?"
9. **Test 9**: "I'm interested in adopting a bird, what birds do you have?"
10. **Test 10**: "I'm interested in adopting a rodent, what rodents do you have?"

Tests 6-10 test the access to the database for each type of animal.

11. **Test 11**: "I'm looking for a playful dog, can you suggest one?"
12. **Test 12**: "I'm looking for a calm and gentle cat, do you have any recommendations?"

Tests 11-12 tests the temprement of animals. 

13. **Test 13**: "I have a budget of $200 for adopting a pet, what pets are within my budget?"
14. **Test 14**: "I am looking for a dog between the ages of 2 to 4 years old, what do you have?"

Tests 13-14 tests the two number related properties with a set number and a range. 

15. **Test 15**: "I'm looking for a pet that is good with kids. Do you have any recommendations?"

Test 15 tests for the description property to see if a pet is friendly or not.

16. **Test 16**: "I'm interested in a low-maintenance pet, what do you suggest? I like Oreo."
17. **Test 17**: "I want to adopt a pet that requires high exercise, can you suggest one? I like Daisy."

Tests 16-17 tests the exercise amount property. 

18. **Test 18**: "I want to adopt a pet that is good with other pets. Do you have any recommendations?"
20. **Test 20**: "I have allergies, can you recommend a hypoallergenic pet?"

Tests 18 and 20 test normally asked adoption questions.

19. **Test 19**: "I'm interested in adopting a senior pet, what do you have available?"

Test 19 tests the age query which mentioning a number age.

21. **Test 21**: "I'm interested in adopting a small pet, what do you have available?"
22. **Test 22**: "I want a pet that can stay alone for a few hours during the day, do you have any suggestions?"

Tests 21-22 tests the properties without directly mentioning them.

23. **Test 23**: "I'm want a husky that is low energy."

Test 23 tests two properties that are contradictory. There is a husky in the database but he is high energy. 

24. **Test 24**: "Where should I go on vacation?"

Test 24 tests the bot for staying on topic

25. **Test 25**: "I would like to adopt Rocky."
26. **Test 26**: "Exit."

Tests 25-26 test the end condition. This should conclude the bot and end the socket

---