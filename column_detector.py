import pandas as pd

def detect_column_types(df, cat_threshold=20):
    
    column_types = {
        "numerical": [],
        "categorical": [],
        "text": []
    }
    
    for col in df.columns:
        col_type = df[col].dtype
        
        # Case 1: Numeric columns (int/float)
        if col_type == "int64" or col_type == "float64":
            unique_vals = df[col].nunique()
            
            if unique_vals <= cat_threshold:
                column_types["categorical"].append(col)  # treat as categorical
            else:
                column_types["numerical"].append(col)    # treat as numerical
        
        # Case 2: Object/string columns
        elif col_type == "object":
            avg_len = df[col].astype(str).str.len().mean()
            
            if avg_len > 30:  # if average string length is large, call it text
                column_types["text"].append(col)
            else:
                column_types["categorical"].append(col)
        
        # Case 3: Other data types (bool, datetime, etc.)
        else:
            column_types["categorical"].append(col)
    
    return column_types