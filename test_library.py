"""
Test script for ds_helper library using a sample dataset.
"""

import pandas as pd
from ds_helper.column_detector import detect_column_types
from ds_helper.auto_visualizer import visualize
from ds_helper.text_cleaner import TextCleaner

# Create a sample dataset similar to Titanic/IMDB
data = {
    'age': [22, 38, 26, 35, 35, None, 54, 2, 27, 14],
    'fare': [7.25, 71.2833, 7.925, 53.1, 8.05, 8.4583, 51.8625, 21.075, 11.1333, 30.0708],
    'class': ['Third', 'First', 'Third', 'First', 'Third', 'Third', 'First', 'Third', 'Second', 'Third'],
    'survived': [0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
    'review': [
        "This movie was uh, amazing! I loved it so much.",
        "Average film, nothing special. Like, it was okay.",
        "Fantastic experience, highly recommend!",
        "Not satisfied with the plot, very disappointed.",
        "Good value for money, but could be better.",
        None,
        "Worst movie ever, terrible acting.",
        "Happy with the purchase, great quality.",
        "So, basically, it's a decent watch.",
        "Literally the best film I've seen!"
    ]
}

df = pd.DataFrame(data)

print("Sample Dataset:")
print(df.head())

# Detect column types
print("\n=== Column Type Detection ===")
types = detect_column_types(df)
for key, cols in types.items():
    print(f"{key.capitalize()}: {cols}")

# Visualize
print("\n=== Generating Visualizations ===")
visualize(df, save_plots=False)  # Set to True to save plots

# Text cleaning demo
print("\n=== Text Cleaning Demo ===")
cleaner = TextCleaner()
sample_reviews = df['review'].dropna().head(3)
print("Original reviews:")
for rev in sample_reviews:
    print(f"- {rev}")

print("\nCleaned reviews:")
for rev in sample_reviews:
    cleaned = cleaner.clean(rev)
    print(f"- {cleaned}")

print("\nLibrary test completed successfully!")
