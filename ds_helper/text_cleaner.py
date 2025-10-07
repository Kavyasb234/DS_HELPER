"""
text_cleaner.py

A module for preprocessing text data in the ds_helper library.

Features:
- Remove punctuations
- Remove filler words (e.g., "uh", "um", "like")
- Remove stopwords
- Lowercasing
- Lemmatization (optional)

Usage:
    from ds_helper.text_cleaner import TextCleaner
    cleaner = TextCleaner()
    cleaned_text = cleaner.clean(text)
"""

import re
import string
from typing import List, Optional

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    _NLTK_AVAILABLE = True
    try:
        stopwords.words('english')
        WordNetLemmatizer()
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
except ImportError:
    _NLTK_AVAILABLE = False


class TextCleaner:
    def __init__(self, remove_punct: bool = True, remove_fillers: bool = True,
                 remove_stopwords: bool = True, lowercase: bool = True,
                 lemmatize: bool = False, custom_fillers: Optional[List[str]] = None):
        """
        Initialize the TextCleaner.

        Args:
            remove_punct: Whether to remove punctuation.
            remove_fillers: Whether to remove filler words.
            remove_stopwords: Whether to remove stopwords.
            lowercase: Whether to convert to lowercase.
            lemmatize: Whether to apply lemmatization.
            custom_fillers: Additional filler words to remove.
        """
        self.remove_punct = remove_punct
        self.remove_fillers = remove_fillers
        self.remove_stopwords = remove_stopwords
        self.lowercase = lowercase
        self.lemmatize = lemmatize

        # Filler words
        self.fillers = {"uh", "um", "like", "you know", "so", "well", "actually", "basically", "literally"}
        if custom_fillers:
            self.fillers.update(custom_fillers)

        # Stopwords and lemmatizer
        if _NLTK_AVAILABLE:
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer() if lemmatize else None
        else:
            self.stop_words = set()
            self.lemmatizer = None
            if remove_stopwords or lemmatize:
                raise ImportError("NLTK is required for stopwords removal and lemmatization. Install with: pip install nltk")

    def clean(self, text: str) -> str:
        """
        Clean the input text based on the initialized options.

        Args:
            text: The input text to clean.

        Returns:
            The cleaned text.
        """
        if not isinstance(text, str):
            return ""

        # Lowercase
        if self.lowercase:
            text = text.lower()

        # Remove punctuation
        if self.remove_punct:
            text = text.translate(str.maketrans('', '', string.punctuation))

        # Tokenize (simple split for now)
        tokens = text.split()

        # Remove fillers
        if self.remove_fillers:
            tokens = [token for token in tokens if token not in self.fillers]

        # Remove stopwords
        if self.remove_stopwords:
            tokens = [token for token in tokens if token not in self.stop_words]

        # Lemmatize
        if self.lemmatize and self.lemmatizer:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]

        # Join back
        cleaned_text = ' '.join(tokens)

        return cleaned_text

    def clean_series(self, series) -> List[str]:
        """
        Clean a pandas Series of text.

        Args:
            series: Pandas Series containing text.

        Returns:
            List of cleaned texts.
        """
        try:
            import pandas as pd
            if isinstance(series, pd.Series):
                return [self.clean(str(text)) for text in series]
        except ImportError:
            pass
        # Fallback for list
        return [self.clean(str(text)) for text in series]


# Convenience function
def clean_text(text: str, **kwargs) -> str:
    """
    Convenience function to clean text with default or custom options.

    Args:
        text: The input text.
        **kwargs: Options for TextCleaner.

    Returns:
        Cleaned text.
    """
    cleaner = TextCleaner(**kwargs)
    return cleaner.clean(text)


# Demo
if __name__ == "__main__":
    sample_text = "Hello, uh, this is a sample text! It's like, you know, full of fillers and stuff. Basically, we need to clean it."
    cleaner = TextCleaner()
    cleaned = cleaner.clean(sample_text)
    print("Original:", sample_text)
    print("Cleaned:", cleaned)
