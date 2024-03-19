import re, unicodedata
from unidecode import unidecode


# Create a function to clean up the column names before sending to BigQuery
def clean_columns_for_bigquery(df):
    # This will clean the column names, BigQuery doesn't accept special characters in columns
    column_names = df.columns
    column_names_clean = [re.sub('\W+','_', column ) for column in column_names] #This will clean the column names, BigQuery doesn't accept special characters in columns
    # Now replace any accented characters with their non-accented equivalent, with the help of the unidecode library    
    column_names_clean = [unidecode(column) for column in column_names_clean]

    df.columns = column_names_clean
    return df


def text_to_id(text):
    """
    Convert input text to id.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    text = strip_accents(text.lower())
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-zA-Z_-]', '_', text)

    text = re.sub('\W+','_', text)

    return text

def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)