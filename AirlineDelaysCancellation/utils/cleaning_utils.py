import re
import pandas as pd

def to_snake_case(name: str) -> str:
    """Convert any column name to snake_case"""
    name = name.strip()
    name = re.sub(r'[\s/]+','_',name)
    # name = re.sub(r'(?<!^)(?=[A-Z])','_',name)
    return name.lower()

def standerdize_column_names(df: pd.DataFrame, inplace: bool = True) -> pd.DataFrame:
    """
    Converts all column names of a DataFrame to snake_case.
    
    Args:
        df: pandas DataFrame
        inplace: modify the DataFrame in place (default True)
    
    Returns:
        Updated DataFrame with standardized column names
    """
    cols = [to_snake_case(col) for col in df.columns]
    if inplace:
        df.columns = cols
        return df
    else:
        new_df = df.copy()
        new_df.columns = cols
        return new_df

def normalize_text_columns(df, case='title', exclude_cols=None):
    """
    Normalizes capitalization across all object/category columns.
    Args:
        df: DataFrame
        case: 'lower', 'upper', or 'title'
        exclude_cols: list of columns to skip (optional)
    Returns:
        DataFrame with consistent text formatting
    """

    df = df.copy()
    exclude_cols = exclude_cols or []

    for col in df.select_dtypes(include=['object', 'category']).columns:
        if col in exclude_cols:
            continue

        if case == 'lower':
            df[col] = df[col].astype(str).str.strip().str.lower()
        elif case == 'upper':
            df[col] = df[col].astype(str).str.strip().str.upper()
        elif case == 'title':
            df[col] = df[col].astype(str).str.strip().str.title()
        else:
            raise ValueError("Invalid case argument: choose from ['lower', 'upper', 'title']")

    return df
