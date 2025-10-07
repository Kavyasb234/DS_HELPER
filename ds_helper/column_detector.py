import pandas as pd

def detect_column_types(df):
    
    column_types = {
        "numerical": [],
        "categorical": [],
        "text": []
    }
    
    for col in df.columns:
        col_type = df[col].dtype
        
        # Case 1: Numeric columns (int/float) - always numerical
        if col_type in ["int64", "float64"]:
            column_types["numerical"].append(col)
        
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
