import streamlit as st
from textblob import TextBlob

# Streamlit App
def main():
    st.title("Sentiment Analysis App")
    
    # Add a textarea for manual text input
    text_input = st.text_area("Enter text for sentiment analysis:")
    
    uploaded_file = st.file_uploader("Upload a text file (txt)", type=["txt"])

    if text_input:
        transcript = text_input

    elif uploaded_file is not None:
        transcript = uploaded_file.read().decode("utf-8")
    else:
        st.warning("Please provide text or upload a file for analysis.")
        return

    # Perform sentiment analysis
    sentiment, sentiment_score = perform_sentiment_analysis(transcript)

    st.subheader("Sentiment Analysis")
    st.write(f"Overall sentiment: {sentiment}, Sentiment score: {sentiment_score}")

# Function to perform sentiment analysis
def perform_sentiment_analysis(transcript):
    blob = TextBlob(transcript)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score < 0:
        sentiment = "Negative"
    elif sentiment_score == 0:
        sentiment = "Neutral"
    else:
        sentiment = "Positive"

    return sentiment, sentiment_score

if __name__ == "__main__":
    main()
