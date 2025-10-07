"""
auto_visualizer.py

Usage:
    from auto_visualizer import visualize
    visualize(df, save_plots=False, out_dir="plots", text_len_thresh=25)

This module:
 - Detects numeric, categorical, and text-like columns (heuristic)
 - Generates appropriate plots:
     Numeric -> histogram, boxplot, scatter (vs another numeric if exists)
     Categorical -> countplot (bar chart), percentage table
     Text -> word cloud, top-k frequency bar
 - Optionally saves plots to disk

Author: (you can put your name)
"""
import os
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter

# optional helper for simple tokenization
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    _NLTK_AVAILABLE = True
    try:
        stopwords.words('english')
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
except Exception:
    _NLTK_AVAILABLE = False

sns.set(style="whitegrid", context="notebook")


def ensure_dir(path):
    if path and not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def is_text_series(s: pd.Series, text_len_thresh=25, pct_non_null_thresh=0.5):
    """
    Heuristic to decide if object series is 'text' (long free text) vs categorical labels.
    - if dtype is object and average length > text_len_thresh => text
    - or fraction of non-null values must exceed pct_non_null_thresh
    """
    if s.dtype.name.startswith("category"):
        return False
    if s.dtype == object:
        non_null = s.dropna().astype(str)
        if len(non_null) == 0:
            return False
        avg_len = non_null.map(len).mean()
        unique_frac = non_null.nunique() / len(non_null) if len(non_null) > 0 else 0
        # long average length OR many unique values and long-ish entries => text
        return (avg_len >= text_len_thresh) or (unique_frac > 0.5 and avg_len >= (text_len_thresh/2))
    return False


def plot_numerical(df: pd.DataFrame, col: str, save_plots=False, out_dir="plots"):
    ensure_dir(out_dir)
    data = df[col].dropna()
    if data.empty:
        return

    # Figure with histogram + boxplot
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    sns.histplot(data, kde=True)
    plt.title(f"Histogram of {col}")

    plt.subplot(1, 2, 2)
    sns.boxplot(x=data)
    plt.title(f"Boxplot of {col}")

    plt.tight_layout()
    if save_plots:
        plt.savefig(os.path.join(out_dir, f"{col}_num_hist_box.png"))
    plt.show()

    # Scatter: if there's another numeric column, plot vs that (first one)
    other_nums = df.select_dtypes(include=['number']).columns.tolist()
    other_nums = [c for c in other_nums if c != col]
    if other_nums:
        other = other_nums[0]
        plt.figure(figsize=(6, 4))
        sns.scatterplot(x=df[other], y=df[col])
        plt.xlabel(other); plt.ylabel(col)
        plt.title(f"Scatter: {col} vs {other}")
        plt.tight_layout()
        if save_plots:
            plt.savefig(os.path.join(out_dir, f"{col}_vs_{other}_scatter.png"))
        plt.show()


def plot_categorical(df: pd.DataFrame, col: str, top_n=20, save_plots=False, out_dir="plots"):
    ensure_dir(out_dir)
    data = df[col].dropna().astype(str)
    if data.empty:
        return

    counts = data.value_counts()
    top = counts.iloc[:top_n]

    plt.figure(figsize=(8, max(4, 0.25*len(top))))
    sns.barplot(x=top.values, y=top.index)
    plt.title(f"Top {len(top)} categories in {col}")
    plt.xlabel("Count")
    plt.tight_layout()
    if save_plots:
        plt.savefig(os.path.join(out_dir, f"{col}_cat_count.png"))
    plt.show()

    # print percentages (useful summary)
    pct = (counts / counts.sum() * 100).round(2)
    summary_df = pd.DataFrame({'count': counts, 'percentage': pct})
    print(f"\n=== Category summary for '{col}' ===")
    print(summary_df.head(top_n))
    print("====================================\n")


def tokenize_text(s: str):
    if _NLTK_AVAILABLE:
        tokens = [t.lower() for t in word_tokenize(s) if t.isalpha()]
        sw = set(stopwords.words('english'))
        tokens = [t for t in tokens if t not in sw and len(t) > 1]
        return tokens
    else:
        # fallback simple split + basic cleanup
        tokens = [w.lower().strip(".,!?;:()[]\"'") for w in s.split()]
        tokens = [t for t in tokens if t.isalpha() and len(t) > 1]
        return tokens


def plot_text(df: pd.DataFrame, col: str, top_k=30, save_plots=False, out_dir="plots"):
    ensure_dir(out_dir)
    text_series = df[col].dropna().astype(str)
    if text_series.empty:
        return

    full_text = " ".join(text_series.values)
    if not full_text.strip():
        return

    # WordCloud
    wc = WordCloud(width=800, height=400, background_color="white").generate(full_text)
    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Word Cloud for {col}")
    if save_plots:
        plt.savefig(os.path.join(out_dir, f"{col}_wordcloud.png"))
    plt.show()

    # Frequency plot of top_k tokens
    tokens = []
    for s in text_series:
        tokens.extend(tokenize_text(s))
    if not tokens:
        return
    freq = Counter(tokens).most_common(top_k)
    words, counts = zip(*freq)
    plt.figure(figsize=(8, max(4, 0.25*len(words))))
    sns.barplot(x=list(counts), y=list(words))
    plt.title(f"Top {len(words)} words in {col}")
    plt.xlabel("Count")
    plt.tight_layout()
    if save_plots:
        plt.savefig(os.path.join(out_dir, f"{col}_top_words.png"))
    plt.show()

    print(f"\nTop words for '{col}':")
    for w, c in freq[:20]:
        print(f"{w}: {c}")
    print()


def visualize(df: pd.DataFrame, save_plots=False, out_dir="plots", text_len_thresh=25):
    """
    Main entrypoint.
    - df: pandas DataFrame
    - save_plots: if True, save generated plots into out_dir
    - out_dir: folder path to save plots
    - text_len_thresh: threshold (avg char length) to consider an 'object' col as text
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("visualize expects a pandas DataFrame")

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    object_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    print(f"Detected numeric columns: {numeric_cols}")
    print(f"Detected object/category columns: {object_cols}")

    # first handle numeric
    for col in numeric_cols:
        try:
            print(f"\n-- Numeric column: {col} --")
            plot_numerical(df, col, save_plots=save_plots, out_dir=out_dir)
        except Exception as e:
            print(f"Error plotting numeric {col}: {e}")

    # handle object/category: decide categorical vs text
    for col in object_cols:
        try:
            is_text = is_text_series(df[col], text_len_thresh=text_len_thresh)
            if is_text:
                print(f"\n-- Text column (heuristic): {col} --")
                plot_text(df, col, save_plots=save_plots, out_dir=out_dir)
            else:
                print(f"\n-- Categorical column: {col} --")
                plot_categorical(df, col, save_plots=save_plots, out_dir=out_dir)
        except Exception as e:
            print(f"Error plotting object column {col}: {e}")


# quick demo when running this module directly
if __name__ == "__main__":
    # small demo DataFrame
    data = {
        "age": [23, 45, 31, 22, 40, 36, 28, None, 50, 29],
        "salary": [50000, 80000, 62000, 48000, 90000, 70000, None, 52000, 110000, 60000],
        "department": ["sales", "hr", "it", "sales", "it", "hr", "it", "sales", "management", "hr"],
        "review": [
            "Good product, excellent quality",
            "Average service, could be better",
            "Loved it! Will recommend to friends",
            "Not satisfied with the delivery time",
            "Fantastic experience overall",
            None,
            "Okay product",
            "Good value for money",
            "Worst service ever, very disappointed",
            "Happy with purchase"
        ]
    }
    demo_df = pd.DataFrame(data)
    print("Running demo visualize on a small sample DataFrame...")
    visualize(demo_df, save_plots=False, out_dir="demo_plots", text_len_thresh=20)
    
