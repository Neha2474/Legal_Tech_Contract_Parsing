import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


# Download required NLTK data
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("tokenizers/punkt_tab/english")
except LookupError:
    nltk.download("punkt_tab")


def summarize_text(text, sentence_count=10):

    if not text or not text.strip():
        return "No text available for summarization."

    # Clean PDF text
    text = re.sub(r"\s+", " ", text).strip()

    # Split document into sentences
    sentences = sent_tokenize(text)

    if len(sentences) <= sentence_count:
        return " ".join(sentences)

    stop_words = set(stopwords.words("english"))

    # Calculate word frequency
    words = word_tokenize(text.lower())

    frequency = {}

    for word in words:
        if word.isalpha() and word not in stop_words:
            frequency[word] = frequency.get(word, 0) + 1

    # Score each sentence
    sentence_scores = {}

    for sentence in sentences:

        sentence_words = word_tokenize(sentence.lower())

        score = 0

        for word in sentence_words:
            if word in frequency:
                score += frequency[word]

        # Avoid selecting extremely long sentences
        if len(sentence_words) <= 50:
            sentence_scores[sentence] = score

    # Select the highest-scoring sentences
    top_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:sentence_count]

    # Keep original document order
    summary_sentences = [
        sentence for sentence in sentences
        if sentence in top_sentences
    ]

    return " ".join(summary_sentences)