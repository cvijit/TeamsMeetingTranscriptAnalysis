import streamlit as st
from textblob import TextBlob
import nltk
import tweepy

# Download NLTK corpora for sentence tokenization
nltk.download("punkt")

# Twitter API Authentication (No user login required)
def authenticate_twitter_api():
    consumer_key = "your_consumer_key"
    consumer_secret = "your_consumer_secret"
    access_token = "your_access_token"
    access_token_secret = "your_access_token_secret"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth)
    return api

# Streamlit App
def main():
    st.title("Sentiment Analysis App")
    
    # Add a selectbox to choose input type
    input_type = st.selectbox("Select input type:", ["Text Input", "Upload File", "Twitter Hashtags"])
    
    if input_type == "Text Input":
        text_input = st.text_area("Enter text for sentiment analysis:")
        transcript = text_input
    elif input_type == "Upload File":
        uploaded_file = st.file_uploader("Upload a text file (txt)", type=["txt"])
        if uploaded_file is not None:
            transcript = uploaded_file.read().decode("utf-8")
    elif input_type == "Twitter Hashtags":
        hashtag_input = st.text_input("Enter hashtags (comma-separated):")
        if hashtag_input:
            hashtags = [tag.strip() for tag in hashtag_input.split(',')]
            tweets = fetch_tweets_by_hashtags(hashtags)
            if tweets:
                transcript = "\n".join([tweet.text for tweet in tweets])
            else:
                st.warning("No tweets found for the specified hashtags.")
                return
    else:
        st.warning("Please select an input type.")
        return

    # Perform sentiment analysis
    sentiment, sentiment_score = perform_sentiment_analysis(transcript)

    st.subheader("Sentiment Analysis")
    st.write(f"Sentiment: {sentiment}, Sentiment Score: {sentiment_score:.2f}")

    # Highlight text based on sentiment
    highlight_text(transcript, sentiment)

    # Display the legend for highlighted colors
    display_legend()

# Function to perform sentiment analysis
def perform_sentiment_analysis(transcript):
    blob = TextBlob(transcript)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score < -0.2:
        sentiment = "Very Negative"
    elif -0.2 <= sentiment_score < 0:
        sentiment = "Negative"
    elif sentiment_score == 0:
        sentiment = "Neutral"
    elif 0 < sentiment_score <= 0.2:
        sentiment = "Positive"
    else:
        sentiment = "Very Positive"

    return sentiment, sentiment_score

# Function to highlight text based on sentiment
def highlight_text(text, sentiment):
    sentiment_colors = {
        "Very Negative": "red",
        "Negative": "orange",
        "Neutral": "gray",
        "Positive": "green",
        "Very Positive": "lime",
    }

    # Highlight text based on sentiment
    st.markdown(f"**Highlighted Text ({sentiment}):**")
    for sentence in TextBlob(text).sentences:
        sentence_sentiment = sentence.sentiment.polarity
        color = sentiment_colors.get(get_sentiment_label(sentence_sentiment), "gray")
        st.markdown(f"<span style='background-color:{color}'>{sentence}</span>", unsafe_allow_html=True)

# Helper function to get sentiment label
def get_sentiment_label(sentiment_score):
    if sentiment_score < -0.2:
        return "Very Negative"
    elif -0.2 <= sentiment_score < 0:
        return "Negative"
    elif sentiment_score == 0:
        return "Neutral"
    elif 0 < sentiment_score <= 0.2:
        return "Positive"
    else:
        return "Very Positive"

# Function to display the legend for highlighted colors
def display_legend():
    st.markdown("### Legend for Highlighted Colors:")
    st.markdown("- <span style='background-color:red'>Red</span>: Very Negative")
    st.markdown("- <span style='background-color:orange'>Orange</span>: Negative")
    st.markdown("- <span style='background-color:gray'>Gray</span>: Neutral")
    st.markdown("- <span style='background-color:green'>Green</span>: Positive")
    st.markdown("- <span style='background-color:lime'>Lime</span>: Very Positive")

# Define a function to fetch tweets based on hashtags using the Twitter API
def fetch_tweets_by_hashtags(hashtags):
    api = authenticate_twitter_api()
    
    tweets = []
    for hashtag in hashtags:
        hashtag_tweets = api.search(q=f"#{hashtag}", count=10)  # Adjust count as needed
        tweets.extend(hashtag_tweets)
    
    return tweets

if __name__ == "__main__":
    main()
