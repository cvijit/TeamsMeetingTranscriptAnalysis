import streamlit as st
from textblob import TextBlob
import nltk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Download NLTK corpora for sentence tokenization
nltk.download("punkt")

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
    fig, ax = plt.subplots(figsize=(6, 1))
    colors = ["red", "orange", "gray", "green", "lime"]
    labels = ["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"]
    patches = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(len(colors))]
    ax.legend(handles=patches, loc='center', frameon=False)
    ax.axis('off')
    st.pyplot(fig)

if __name__ == "__main__":
    main()
