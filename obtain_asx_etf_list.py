## The goal of this script is to obtain a list of all ethical ETFs listed on the ASX

# Import libraries
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

# Obtain dataframe for all ASX ETFs
def obtain_all_etf_df():
    url_list = "https://www.asx.com.au/products/etf/managed-funds-etp-product-list.htm"
    r = requests.get(url_list)

    # Use beautiful soup to extract relevant parts
    soup = BeautifulSoup(r.text, 'html.parser')
    tag = "9124-content"
    table_rows = soup.find(id=tag).find("table").find_all("tr")
    # Split each row into columns
    column_elements = ["th", "td"]
    table_rows = [row.find_all(column_elements) for row in table_rows]

    # Keep only rows which have the same number of columns
    max_cols = max(map(lambda row: len(row), table_rows))
    table_rows = list(filter(lambda x: len(x) == max_cols, table_rows))

    # Map these
    table_array = np.asarray([elem.text.strip() for row in table_rows for elem in row])
    table_array.resize((len(table_rows), max_cols))

    # Convert to dataframe (except first row)
    df = pd.DataFrame(table_array[1:])
    # Add the column names
    df.columns = table_array[0]

    return df