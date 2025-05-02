import streamlit as st
import collections 

from simple_search.searcher import Searcher
from simple_search.dataloader import DataLoader
from simple_search.utils import reset_pages, get_data

st.title('Hepatitis Press Review Simple Search')

get_data()

if 'page_count' not in st.session_state:
    st.session_state['page_count'] = 0
if 'to_see' not in st.session_state:
    st.session_state['to_see'] = 10
if 'additional_context' not in st.session_state:
    st.session_state['additional_context'] = collections.defaultdict(str)

with st.expander('Click for further information on how to construct a query.'):
    st.markdown("""
    * If you'd like to search for just a single term, you can enter it in the box above. 
    * If you'd like to search for a phrase, you can enclose it in quotations, such as "Macfarlane Trust".
    * A query like "Macfarlane Trust"~5 would return results where "Marcfarlane" and "Trust" are at most 5 words away from each other.
    * AND can be used as a boolean operator and will return results where two terms are both in a passage. AND is automatically placed in a query of two words, so Macfarlane Trust is internally represented as Macfarlane AND Trust.
    * OR can be used as a boolean operator and will return results where either one of two terms are in a passage.
    * NOT can be used as a boolean operator and will return results which do not include the term following the NOT.
    * From these boolean operators, one can construct complex queries like: HIV AND Haemophilia NOT "Hepatitis C". This query would return results that have both HIV and Haemophilia in them, but do not have Hepatitis C.
    * Parentheses can be used to group boolean statements. For example, the query Haemophilia AND ("Hepatitis C" OR  HIV) would return results that have Haemophilia and either Hepatitis C or HIV in them. 
    * If you'd like to search in a specific date range, you can specify it with the date: field. For example, date:[20210101 TO 20220101] HIV would return results between January 1st, 2021 and January 1st, 2022 that have HIV in them.
    """)

newspaper_type = st.radio('Choose a newspaper type', ['All', 'Tabloids', 'Broadsheets'], on_change=reset_pages)

dataloader = DataLoader()

data, _ = dataloader.load()
all_newspapers = data['Newspaper'].unique().tolist()
newspapers = st.multiselect('Choose newspapers to restrict search to', all_newspapers, default=[], on_change=reset_pages)
default_context = st.number_input('How many sentences of context would you like to see by default?', min_value=0, max_value=10, value=0, step=1, help='This number represents the amount of sentences to be added before and after the result.', on_change=reset_pages)
query_str = st.text_input('Search for a word or phrase', on_change=reset_pages)
to_see = st.number_input('How many results would you like to see per page?', min_value=1, max_value=100, value=10, step=1)
stemmer = st.toggle('Use stemming', help='If selected, the search will use stemming to find words with the same root. For example, "running" will match "run" and "ran".', on_change=reset_pages)

if query_str != '':
    if newspaper_type == 'Tabloids':
        newspaper_type = 'tabloid'
    elif newspaper_type == 'Broadsheets':
        newspaper_type = 'broadsheet'

    searcher = Searcher(query_str, dataloader, stemmer, newspaper_type=newspaper_type, newspapers=newspapers, added_default_context=default_context)
    searcher.search(to_see)