<<<<<<< HEAD
# ds_helper Library

ds_helper is a reusable Python library for data science tasks, including column type detection, automatic visualization, and text cleaning utilities.

## Installation

```bash
pip install .
=======
# ds_helper

A Python library for data science utilities, including column type detection, automatic visualization, and text cleaning.

## Installation

Clone the repository and install with pip:

```bash
git clone https://github.com/Kavyasb234/DS_HELPER.git
cd DS_HELPER
pip install -e .
>>>>>>> eea73810ad5b46d5129da19d7bf82d3c1420c57a
```

## Modules

<<<<<<< HEAD
### column_detector

Detects column types in a pandas DataFrame (numerical, categorical, text).

```python
from ds_helper import detect_column_types
import pandas as pd

df = pd.read_csv('data.csv')
types = detect_column_types(df)
print(types)
```

### auto_visualizer

Automatically generates plots based on column types.

```python
from ds_helper import visualize
visualize(df)
```

### text_cleaner

Text preprocessing utilities for cleaning unstructured text data.

```python
from ds_helper import TextCleaner

cleaner = TextCleaner(lemmatize=True)
clean_text = cleaner.clean_text("Um, this is like an example sentence, you know.")
print(clean_text)
```

## Testing

Test the library on your dataset by importing the modules and running the functions as shown above.
=======
### 1. column_detector

Detects column types in a pandas DataFrame: numerical, categorical, or text.

#### Usage

```python
from ds_helper.column_detector import detect_column_types
import pandas as pd

df = pd.DataFrame({
    'age': [25, 30, 35],
    'category': ['A', 'B', 'A'],
    'description': ['This is a long text description.', 'Another text.']
})

types = detect_column_types(df)
print(types)
# Output: {'numerical': ['age'], 'categorical': ['category'], 'text': ['description']}
```

### 2. auto_visualizer

Automatically generates appropriate plots based on detected column types.

- Numerical: Histograms, boxplots, scatter plots
- Categorical: Bar charts, count plots
- Text: Word clouds, frequency plots

#### Usage

```python
from ds_helper.auto_visualizer import visualize
import pandas as pd

df = pd.DataFrame({
    'age': [23, 45, 31, 22],
    'salary': [50000, 80000, 62000, 48000],
    'department': ['sales', 'hr', 'it', 'sales'],
    'review': ['Good product', 'Average service', 'Loved it', 'Not satisfied']
})

visualize(df, save_plots=True, out_dir='plots')
```

### 3. text_cleaner

Preprocesses text data: removes punctuation, filler words, stopwords, applies lowercasing, and optional lemmatization.

#### Usage

```python
from ds_helper.text_cleaner import TextCleaner

cleaner = TextCleaner()
cleaned = cleaner.clean("Hello, uh, this is a sample text! It's like, you know, full of fillers.")
print(cleaned)
# Output: "hello sample text full fillers"

# Or use the convenience function
from ds_helper.text_cleaner import clean_text
cleaned = clean_text("Sample text.", remove_stopwords=True, lemmatize=True)
```

## Testing on a Real Dataset

Here's an example using the Titanic dataset (assuming you have it downloaded):

```python
import pandas as pd
from ds_helper.column_detector import detect_column_types
from ds_helper.auto_visualizer import visualize
from ds_helper.text_cleaner import TextCleaner

# Load dataset (replace with actual path)
df = pd.read_csv('titanic.csv')

# Detect types
types = detect_column_types(df)
print("Column types:", types)

# Visualize
visualize(df)

# Clean text column if exists (e.g., 'Name' or add a text column)
if 'text_column' in df.columns:
    cleaner = TextCleaner()
    df['cleaned_text'] = df['text_column'].apply(cleaner.clean)
```

## Dependencies

- pandas
- matplotlib
- seaborn
- wordcloud
- nltk

Install with: `pip install pandas matplotlib seaborn wordcloud nltk`
>>>>>>> eea73810ad5b46d5129da19d7bf82d3c1420c57a

## License

MIT License
