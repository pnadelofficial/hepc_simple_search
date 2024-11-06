import streamlit as st
from whoosh.qparser import QueryParser, query
from whoosh.lang.morph_en import variations
from whoosh.query import Term, And
from datetime import datetime
import gspread
from simple_search.exporter import Exporter
from simple_search.page import Page

@st.cache_resource
def load_google_sheet():
    CREDS = st.secrets['gsp_secrets']['my_project_settings']
    gc = gspread.service_account_from_dict(CREDS)
    return gc.open('simple-search-feedback').sheet1 # gmail account

class Searcher:
    def __init__(self, query_str, dataloader, stemmer, newspaper_type='All') -> None:
        self.query_str = query_str
        self.dataloader = dataloader
        self.data, self.ix, = self.dataloader.load()
        self.stemmer = stemmer
        self.newspaper_type = newspaper_type
    
    def parse_query(self):
        if self.stemmer: 
            parser = QueryParser("chunks", self.ix.schema, termclass=query.Variations)
        else:
            parser = QueryParser("chunks", self.ix.schema)    
        q = parser.parse(self.query_str)
        all_tokens = list(set(self.query_str.split(' ') + [item for sublist in [variations(t) for t in self.query_str.split(' ')] for item in sublist]))
        searches = [q.lower() for q in all_tokens if (q != 'AND') and (q != 'OR') and (q != 'NOT') and (q != 'TO')]
        
        if self.newspaper_type != 'All':
            type_query = Term('newspaper_type', self.newspaper_type)
            q = And([q, type_query])
        return q, searches

    def search(self, to_see):
        q, searches = self.parse_query()
        with self.ix.searcher() as searcher:
            results = searcher.search(q, limit=None)
            self.results = results
            default = 1
            
            doc_list = self.data.Title.unique().tolist()
            st.session_state['pages'] = [self.results[i:i + to_see] for i in range(0, len(self.results), to_see)]

            with st.sidebar:
                st.markdown("# Page Navigation")
                if st.button('See next page', key='next'):
                    st.session_state['page_count'] += 1
                if st.button('See previous page', key='prev'):
                    st.session_state['page_count'] -= 1   
                if (len(st.session_state['pages']) > 0):
                    page_swap = st.number_input('What page do you want to visit?', min_value=default, max_value=len(st.session_state['pages']), value=default)
                if st.button('Go to page'):
                    st.session_state['page_count'] = page_swap-1
                st.divider()
                st.markdown("# Export to PDF")
                if st.button('Export this page to PDF'):
                    e = Exporter(self.query_str)
                    e(self)
                if st.button('Export all results to PDF'):
                    e = Exporter(self.query_str, full=True)
                    e(self)
                st.divider()
                st.markdown("# Feedback")
                feedback = st.text_area('Give any feedback you may have here')
                fb = load_google_sheet()
                if st.button('Send feedback'):
                    fb.append_row([datetime.now().strftime("%m/%d/%Y"), feedback])
                
            st.write(f"There are **{len(self.results)}** results for this query.")
            st.divider()

            if (default == 0) or (len(self.results) == 0):
                pass
            else:
                if len(doc_list) > 0:
                    p = Page(st.session_state['pages'][st.session_state['page_count']], self.data, searches, doc_list)
                    p()

                    st.write(f"Page: {st.session_state['page_count']+1} out of {len(st.session_state['pages'])}")