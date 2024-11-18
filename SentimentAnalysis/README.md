Sentiment Analysis Asssignment 
Author: Lucy Kien
Date: 04/26/2024

1. Determine the tweets that Naive Bayes failed at. Print out the tweet, its Naive Bayes score, and its label.

Here are all the mislabeled tweets that Naive Bayes failed at. 

Tweet: ['truli', 'later', 'move', 'know', 'queen', 'bee', 'upward', 'bound', 'movingonup']
True Label: 1.0
Prediction: -1.4536565937140937

Tweet: ['new', 'report', 'talk', 'burn', 'calori', 'cold', 'work', 'harder', 'warm', 'feel', 'better', 'weather', ':p']
True Label: 1.0
Prediction: -1.0140253882937156

Tweet: ['harri', 'niall', '94', 'harri', 'born', 'ik', 'stupid', 'wanna', 'chang', ':d']
True Label: 1.0
Prediction: -0.49684756706512

Tweet: ['park', 'get', 'sunlight']
True Label: 1.0
Prediction: -0.9460582795220721

Tweet: ['uff', 'itna', 'miss', 'karhi', 'thi', 'ap', ':p']
True Label: 1.0
Prediction: -0.45179270591547827

Tweet: ['hello', 'info', 'possibl', 'interest', 'jonatha', 'close', 'join', 'beti', ':(', 'great']
True Label: 0.0
Prediction: 0.7176024042892504

Tweet: ['u', 'prob', 'fun', 'david']
True Label: 0.0
Prediction: 1.929589138312492

Tweet: ['pat', 'jay']
True Label: 0.0
Prediction: 1.389956251104192

Tweet: ['belov', 'grandmoth']
True Label: 0.0
Prediction: 0.014591858678808136

Tweet: ['sr', 'financi', 'analyst', 'expedia', 'inc', 'bellevu', 'wa', 'financ', 'expediajob', 'job', 'job', 'hire']
True Label: 0.0
Prediction: 0.8625695768956083

2. Prompt your LLM to see if it will identify the tweets correctly as positive or negative. Use concise prompting so it only responds with "positive sentiment" or "negative sentiment"

Here are all the mislabeled tweets with the LLM predicting weather or not the tweet has an overall positive sentiment or a negative sentiment. As you can see, it got some wrong so we can then prompt the LLM again to see why they thought the tweet was a positive or negative sentiment.

Tweet: ['truli', 'later', 'move', 'know', 'queen', 'bee', 'upward', 'bound', 'movingonup']
True Label: 1.0
Prediction: -1.4536565937140937
LLM Prediction: Positive Sentiment

Tweet: ['new', 'report', 'talk', 'burn', 'calori', 'cold', 'work', 'harder', 'warm', 'feel', 'better', 'weather', ':p']
True Label: 1.0
Prediction: -1.0140253882937156
LLM Prediction: Positive Sentiment

Tweet: ['harri', 'niall', '94', 'harri', 'born', 'ik', 'stupid', 'wanna', 'chang', ':d']
True Label: 1.0
Prediction: -0.49684756706512
LLM Prediction: Neutral Sentiment

Tweet: ['park', 'get', 'sunlight']
True Label: 1.0
Prediction: -0.9460582795220721
LLM Prediction: Positive Sentiment

Tweet: ['uff', 'itna', 'miss', 'karhi', 'thi', 'ap', ':p']
True Label: 1.0
Prediction: -0.45179270591547827
LLM Prediction: Negative Sentiment

Tweet: ['hello', 'info', 'possibl', 'interest', 'jonatha', 'close', 'join', 'beti', ':(', 'great']
True Label: 0.0
Prediction: 0.7176024042892504
LLM Prediction: Positive Sentiment

Tweet: ['u', 'prob', 'fun', 'david']
True Label: 0.0
Prediction: 1.929589138312492
LLM Prediction: Positive Sentiment

Tweet: ['pat', 'jay']
True Label: 0.0
Prediction: 1.389956251104192
LLM Prediction: Neutral Sentiment

Tweet: ['belov', 'grandmoth']
True Label: 0.0
Prediction: 0.014591858678808136
LLM Prediction: Positive Sentiment

Tweet: ['sr', 'financi', 'analyst', 'expedia', 'inc', 'bellevu', 'wa', 'financ', 'expediajob', 'job', 'job', 'hire']
True Label: 0.0
Prediction: 0.8625695768956083
LLM Prediction: Positive Sentiment


3. If the LLM is still incorrect, have it explain its decision--do you agree with the analysis?

Here are all the mislabeled tweets with LLM analysis of them if they got the tweets sentiment wrong. As you can see, it only got 4 out of the 10 wrong. I agree with some of the analysis as in you can't get the full context out of just a few words sometimes. For example, in the tweet where is says 'beloved grandmother' I would also assume the tweet would carry a positive sentiment as you are talking about a loved one. 

Tweet: ['truli', 'later', 'move', 'know', 'queen', 'bee', 'upward', 'bound', 'movingonup']
True Label: 1.0
Prediction: -1.4536565937140937
LLM Prediction: Positive Sentiment

Tweet: ['new', 'report', 'talk', 'burn', 'calori', 'cold', 'work', 'harder', 'warm', 'feel', 'better', 'weather', ':p']
True Label: 1.0
Prediction: -1.0140253882937156
LLM Prediction: Positive Sentiment

Tweet: ['harri', 'niall', '94', 'harri', 'born', 'ik', 'stupid', 'wanna', 'chang', ':d']
True Label: 1.0
Prediction: -0.49684756706512
LLM Prediction: Neutral Sentiment

Tweet: ['park', 'get', 'sunlight']
True Label: 1.0
Prediction: -0.9460582795220721
LLM Prediction: Positive Sentiment

Tweet: ['uff', 'itna', 'miss', 'karhi', 'thi', 'ap', ':p']
True Label: 1.0
Prediction: -0.45179270591547827
LLM Prediction: Positive Sentiment

Tweet: ['hello', 'info', 'possibl', 'interest', 'jonatha', 'close', 'join', 'beti', ':(', 'great']
True Label: 0.0
Prediction: 0.7176024042892504
LLM Prediction: Positive Sentiment
LLM Explanation for mislabeling tweets: I apologize for the incorrect sentiment analysis. I mistakenly categorized the tweet as having a negative sentiment based on the presence of the emoticon ":(" at the end of the tweet. Emoticons are often used to convey emotions or tone in text, and in this case, I incorrectly interpreted it as a negative sentiment indicator. However, it is important to consider the context and surrounding words in the tweet to accurately determine the sentiment. Thank you for bringing this to my attention.

Tweet: ['u', 'prob', 'fun', 'david']
True Label: 0.0
Prediction: 1.929589138312492
LLM Prediction: Positive Sentiment
LLM Explanation for mislabeling tweets: I apologize for the incorrect sentiment analysis. I mistakenly interpreted the words 'u', 'prob', 'fun', and 'david' as positive or neutral based on their individual meanings. However, sentiment analysis also takes into account the context and tone of the entire sentence or tweet. In this case, without the full context of the tweet, it is possible that the sentiment could be different than what was initially determined. It is important to consider the overall message and tone of the text when analyzing sentiment. Thank you for bringing this to my attention.

Tweet: ['pat', 'jay']
True Label: 0.0
Prediction: 1.389956251104192
LLM Prediction: Neutral Sentiment

Tweet: ['belov', 'grandmoth']
True Label: 0.0
Prediction: 0.014591858678808136
LLM Prediction: Positive Sentiment
LLM Explanation for mislabeling tweets: I apologize for the incorrect sentiment analysis. I chose the sentiment "beloved grandmother" based on the words "belov" and "grandmoth" which are likely misspellings of "beloved" and "grandmother." These words typically convey positive emotions and affection, which led me to interpret the sentiment as positive. However, I understand that sentiment analysis can be subjective and context-dependent, so I appreciate your feedback and will strive to improve the accuracy of my analysis in the future.

Tweet: ['sr', 'financi', 'analyst', 'expedia', 'inc', 'bellevu', 'wa', 'financ', 'expediajob', 'job', 'job', 'hire']
True Label: 0.0
Prediction: 0.8625695768956083
LLM Prediction: Positive Sentiment
LLM Explanation for mislabeling tweets: I apologize for the error in my analysis. I mistakenly identified the sentiment of the tweet based on the keywords provided, which led me to interpret it as a positive sentiment related to a job opportunity at Expedia Inc. in Bellevue, WA. However, without the full context of the tweet, it is possible that the sentiment is actually negative or neutral. I should have taken into account the overall tone and content of the tweet before making a determination about the sentiment. Thank you for bringing this to my attention.


4. Can you write a tweet that is subtly incorrect due to language which your Naive Bayes classifier will mislabel given that it doesn't care about word ordering? Will the LLM classify it correctly?

Yes I think this can happen easily espeically in English. Since English is a more informal language it is easy to write sentences or say something that is grammatically incorrect yet other humans will understand what you are trying to say regardless. If a sentnece is not structured with proper grammar, it can be easy for a language learning model to incorrectly guess the sentiment of a sentence especially if there is no prior context. Naive Bayes can also mislabel these things because nowadays we use a lot of slang in everyday life. Tweets are no exception to this rule and often time slang will be used in sentences, these slang words can be misinterpreted often as positive or negative depending on the word and this can overall impact the prediction of the label. I think that it is difficult for these models to be 100% correct due to language constantly changing and new rules are being applied. 