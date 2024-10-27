import pandas as pd

def extension_stats(df):
    return df['extension'].value_counts().to_dict()

def top_files(df, top_n=10):
    return df.nlargest(top_n, 'file_size')[['file_name', 'file_size']].to_dict(orient='records')

def summary_stats(df):
    return {
        "total_files": len(df),
        "average_size": df['file_size'].mean(),
        "median_size": df['file_size'].median(),
        "total_size": df['file_size'].sum()
    }
