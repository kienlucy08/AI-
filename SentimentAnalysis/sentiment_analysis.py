
'''
File: sentiment_analysis.py
Author: Lucy Kien
Date: 04/15/2024

This provides sentiment analysis functions for processing tweets in particular,
but relies on tweet_processing to handle the cleanup of the tweets. Analysis is
done using Naive Bayes.

'''
import random
import tweet_processor as tp
import numpy as np
from openai import OpenAI

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

def partition_training_and_test_sets(pos_tweets : list[str],
                                     neg_tweets : list[str], 
                                     split : float = .8) -> tuple[list[str], 
                                                                  np.ndarray[float], 
                                                                  list[str], 
                                                                  np.ndarray[float], 
                                                                  int, int, int, int]:
    '''
    Partition our sets of tweets into positive and negative tweets based
    on a split factor. 

    Parameters: 
        pos_tweets -- list of strings that are positive tweets
        neg_tweets -- list of strings that are negative tweets
        split -- factor to split the training and partition sets into.
            Defaults to .8, or 80% training, 20% testing.

    Returns:
        A list of training tweets
        A list of the same size of training labels, which will be 1 or 0 for positive or negative tweets
        A list of testing tweets
        A list of testing labels, which 
    '''
    if split < 0 or split > 1:
        raise Exception('split must be between 0 and 1')
    
    # multiply the length of the list of tweets by our split factor and convert to an int
    pos_train_size = int(split * len(pos_tweets))
    neg_train_size = int(split * len(neg_tweets))
    
    # split our sets
    pos_x = pos_tweets[:pos_train_size]
    neg_x = neg_tweets[:neg_train_size]
    
    # test sets
    test_pos = pos_tweets[pos_train_size:]
    test_neg = neg_tweets[neg_train_size:]

    # combine the sets for training and testing
    train_x = pos_x + neg_x
    test_x = test_pos + test_neg

    # our labels are 1 for positive, 0 for negative, so we'll create
    # arrays of 1s and 0s for the training and test sets
    train_y = np.append(np.ones(len(pos_x)), np.zeros(len(neg_x)))
    test_y = np.append(np.ones(len(test_pos)), np.zeros(len(test_neg)))

    pos_test_size = len(pos_tweets) - pos_train_size
    neg_test_size = len(neg_tweets) - neg_train_size
    return (train_x, train_y, test_x, test_y, pos_train_size, 
            neg_train_size, pos_test_size, neg_test_size)


# takes a list of tweets        
def build_word_freq_dict(tweets : list[list[str]], labels : np.ndarray[int]) -> dict[(str, int),  int]:
    '''
    Creates a frequency dictionary based on the tweets. The frequency dictionary
    has keys which are (word, label) pairs, for example, ('happi', 1), while the
    value associated with it is the number of times that word was seen in a given
    class. For example, if 'happi' is seen 10 times in positive tweets, then we'd 
    see freqs[('happi', 1)] = 10. If it were seen 3 times in negative tweets, we'd
    see freqs[('happi', 0)] = 3.

    Parameters: 
    tweets -- A list of strings, each a tweet
    labels -- A list of integers either 0 or 1 for negative or positive classes

    Note that the number of tweets and labels must match. 

    Return: 
    A dictionary containing (word, class) keys mapping to the number of 
    times that word in that class appears in the data set
    '''
    freqs = {}
    vocab = set()

    zippedData = zip(tweets, labels)

    for tweet, label in zippedData:

        for word in tweet:
            # Add the word to the vocabulary set
            vocab.add(word)
            # Construct the key as (word, label)
            key = (word, label)

            if key in freqs:
                freqs[key] += 1

            # else, if the key is new, add it to the dictionary and set the count to 1
            else:
                freqs[key] = 1
            # Update the frequency dictionary
            # freqs[key] = freqs.get(key, 0) + 1


    return freqs, vocab

def test_word_freq_dict(tweets, labels):
    '''
    Simple function that tests some tweets and if your build_word_freq_dict is built correctly
    '''
    print(f'test of word frequency: {build_word_freq_dict(tweets, labels)}')


def count_pos_neg(freqs : dict[(str, int),  int]) -> tuple[int, int]:
    '''a
    Count the number of positive and negative words in the
    frequency dictionary.

    Parameters:
    freqs -- a dictionary of ((str, int), int) pairs, where the key is a
    word and label of 0 or 1 for negative or positive sentiment, and the value
    associated with the key is the number of times it was seen.

    Returns:
    Returns two values, the number of times any positive word was seen (i.e., the
    total number of positive events), and the number of times a negative word was
    seen. 
    '''
    # set the number of pos and neg to 0
    num_pos = 0
    num_neg = 0
    # go over each tuple in the dictionary which is set up
    # with a word, then label then the count that word
    for (word, label), count in freqs.items():
        # label is one it is a pos
        if label == 1:
            num_pos += count
        # label is 0 it is neg
        elif label == 0:
            num_neg += count

    return num_pos, num_neg



def build_loglikelihood_dict(freqs : dict[(str, int),  int], N_pos : int, N_neg : int, vocab : list[str]) -> dict[str, float]:
    '''
    Create a dictionary based on the frequency of each word in each class appearing
    of the probability of that word occuring, using Laplacian smoothing by adding
    1 to each occurrence and the size of the vocabulary. 

    Thus, we'd calculate (freq(w_i, class) + 1) / (N_class + V_size)

    Parameters:
        freqs -- dictionary from (word, class) to occurrence count mapping
        N_pos -- number of positive events for all words
        N_neg -- number of negative events for all words
        vocab -- list vocabulary of words

    Returns:
        A dictionary of words to the ratio of positive and negative usage of the word
    '''
    loglikelihood = {}
    vocab_size = len(vocab)

    # calculate the loglikelihood dictionary from the given parameters
    for word in vocab:
        freq_neg = freqs.get((word, 0), 0)
        freq_pos = freqs.get((word, 1), 0)

        # take the log of the freq of the word and add one, divide by the number of positive words + the vocab size
        pos_log = np.log((freq_pos + 1) / (N_pos + vocab_size))
        neg_log = np.log((freq_neg + 1) / (N_neg + vocab_size))

        # log of each word will take the pos log minus the neg log
        # if it is neg overall the word is negative
        loglikelihood[word] =  pos_log - neg_log

    return loglikelihood


def naive_bayes_predict(loglikelihood : dict[str, float], log_pos_neg_ratio : float, tweet : list[str]) -> float:
    '''
    Calculates the prediction based on our dictionary of log-likelihoods of each
    word in a tweet added to the log of the ratio of positive and negative tweets

    Parameters:
        loglikelihood -- a dictionary of words to the ratio of postive/negative probabilities of the words
        log_pos_neg_ratio -- the log of the ratio of total positive to total negative events
        tweet -- a list of tokens (likely from process_tweet)
    '''
    # set the sentiment store to the ratio
    sentiment_score = log_pos_neg_ratio

    # for words in the tweet if its in the likelihood add to the sentiment score
    for word in tweet:
        if word in loglikelihood:
            sentiment_score += loglikelihood.get(word, 0)

    # return the sentiment score
    return sentiment_score

def main():
    # first, set up our samples
    pos_tweets, neg_tweets, stopwords, full_pos_tweets, full_neg_tweets = tp.process_tweets('SentimentAnalysis/positive_tweets.json', 'SentimentAnalysis/negative_tweets.json', 'TweetProcessor/english_stopwords.txt')
    
    print(f'random positive: {pos_tweets[random.randint(0, len(pos_tweets) - 1)]}')
    print(f'random negative: {neg_tweets[random.randint(0, len(neg_tweets) - 1)]}')
    print(f'random stopword: {stopwords[random.randint(0, len(stopwords) - 1)]}')

    # defines the partition between training and test sets
    SPLIT = .8
    
    # next, partition the sets into training sets, test sets, and labels
    train_x, train_y, test_x, test_y, N_train_pos, N_train_neg, N_test_pos, N_test_neg = partition_training_and_test_sets(pos_tweets, neg_tweets, SPLIT)
    print(f'N_train_pos = {N_train_pos}, N_train_neg = {N_train_neg}')
    print(f'N_test_pos = {N_test_pos}, N_test_neg = {N_test_neg}')

    # create a frequency dictionary
    freq_train, vocab = {}, {}
    freq_train, vocab = build_word_freq_dict(train_x, train_y)
    print(f'freq dictionary size: {len(freq_train)}, vocab size: {len(vocab)}')

    # count the number of positive and negative words
    num_pos, num_neg = 0, 0
    num_pos, num_neg = count_pos_neg(freq_train)
    print(f'Number of positive events: {num_pos}, Number of negative events: {num_neg}')

    # log of the ratio of the total positive and total negative tweets from the training set
    log_pos_neg_ratio = 0
    log_pos_neg_ratio = np.log(num_pos / num_neg)
    print(f'log_pos_neg_ratio of the training set = {log_pos_neg_ratio}')

    # now calculate the log likelihood dictionary
    log_likelihood = build_loglikelihood_dict(freq_train, num_pos, num_neg, vocab)

    print("Random Tweets:")
    print()

    # print predictions for 10 random tweets
    for i in range(10):
        idx = random.randint(0, N_test_pos + N_test_neg - 1)
        print(f'Tweet: {test_x[idx]}')
        print(f'Label: {test_y[idx]}')
        print(f'Prediction: {naive_bayes_predict(log_likelihood, log_pos_neg_ratio, test_x[idx])}')
        print()
    
    # now let's see what our error rate is
    # Calculate the error rate and print it out
    # also print out the mislabeled tweets
    # Calculate the error rate
    error_count = 0
    mislabeled_tweets = []
    true_tweets = []

    for (tweet, label) in zip(test_x, test_y):
        prediction = naive_bayes_predict(log_likelihood, log_pos_neg_ratio, tweet)
        # Check if the prediction doesn't match the true label
        if (prediction > -0.0005 and int(label) == 0):
            error_count += 1
            mislabeled_tweets.append((tweet, label, prediction))
        elif(prediction < 0.0005 and int(label) == 1):
            error_count += 1
            mislabeled_tweets.append((tweet, label, prediction))
        else:
            true_tweets.append((tweet, label, prediction))

    print("Mislabeled Tweets:")
    print()

    count = 0
    # Part 2 my LLM
    # # Print out the mislabeled tweets and determine why they are mislabeled
    for tweet, label, prediction in mislabeled_tweets:
        print("Tweet:", tweet)
        print("True Label:", label)
        print("Prediction:", prediction)
        llm_response = get_llm_response(client, f'Using the {tweet} please determine the sentiment either positive or negative and tell me by saying Positive Sentiment, or Negative Sentiment')
        extracted_message = llm_response.choices[0].message.content
        print("LLM Prediction:", extracted_message)
        if(extracted_message == "Positive Sentiment" and label == 0.0) or (extracted_message == "Negative Sentiment" and label == 1.0):
            expanded_llm_response = get_llm_response(client, f'Using the {tweet} you just analysized you actually got it wrong. The is not the correct sentiment of the tweet. Can you please explain why you chose that sentiment?')
            expand_extracted_message = expanded_llm_response.choices[0].message.content
            count += 1
            print("LLM Explanation for mislabeling tweets:", expand_extracted_message)
        print()

    # error rate and len of mislabeled and true tweets
    print("# of mislabeled tweets: ", len(mislabeled_tweets))
    print("# of truely labeled tweets:", len(true_tweets))
    print(f'Error rate: {error_count / (N_test_pos + N_test_neg)}')



# run the main function if this is where our program was executed from
if __name__ == '__main__':
    main()