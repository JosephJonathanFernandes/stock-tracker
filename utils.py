import pandas as pd
import streamlit as st

@st.cache_data
def load_data(nifty_path, metadata_path):
    """
    Loads and merges NIFTY 50 data and stock metadata.
    """
    try:
        # Load NIFTY 50 data
        df = pd.read_csv(nifty_path)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Load Metadata
        metadata = pd.read_csv(metadata_path)
        
        # Merge on Symbol (assuming Symbol is the common column)
        # Check if Symbol exists in both, if not try Company Name or similar
        # Based on file inspection, both have 'Symbol'
        merged_df = pd.merge(df, metadata, on='Symbol', how='left')
        
        return merged_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def filter_data(df, stock_symbol=None, start_date=None, end_date=None, industry=None):
    """
    Filters the dataframe based on user inputs.
    """
    filtered_df = df.copy()
    
    if stock_symbol:
        filtered_df = filtered_df[filtered_df['Symbol'] == stock_symbol]
    
    if industry:
        filtered_df = filtered_df[filtered_df['Industry'] == industry]
        
    if start_date and end_date:
        mask = (filtered_df['Date'] >= pd.to_datetime(start_date)) & (filtered_df['Date'] <= pd.to_datetime(end_date))
        filtered_df = filtered_df.loc[mask]
        
    return filtered_df

def get_stock_list(df):
    """Returns a list of unique stock symbols and company names."""
    if df is not None:
        return df[['Symbol', 'Company Name']].drop_duplicates().sort_values('Symbol')
    return pd.DataFrame()

def get_industry_list(df):
    """Returns a list of unique industries."""
    if df is not None:
        return sorted(df['Industry'].dropna().unique().tolist())
    return []
