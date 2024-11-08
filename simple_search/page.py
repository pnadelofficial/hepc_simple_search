import streamlit as st
from string import punctuation
import re
from datetime import datetime

class Page:
    def __init__(self, results, data, searches, doc_search, display_date=True) -> None:
        self.results = results
        self.data = data
        self.searches = searches
        self.doc_search = doc_search
        self.display_date = display_date

    def escape_markdown(self, text):
        '''Removes characters which have specific meanings in markdown'''
        MD_SPECIAL_CHARS = "\`*_{}#+"
        for char in MD_SPECIAL_CHARS:
            text = text.replace(char, '').replace('\t', '')
        return text
    
    def no_punct(self, word):
        '''Util for below to remove punctuation'''
        return ''.join([letter for letter in word if letter not in punctuation.replace('-', '') + '’' + '‘' + '“' + '”' + '—' + '…' + '–'])
    
    def no_digits(self, word):
        '''Util for below to remove digits'''
        return ''.join([letter for letter in word if not letter.isdigit()])

    def remove_tilde(self, word):
        return re.sub('~\d+', '', word)

    def inject_highlights(self, text, searches):
        '''Highlights words from the search query''' 
        searches = [self.remove_tilde(s).replace('"', '') for s in searches if s != '']
        esc = punctuation + '."' + '..."'
        inject = f"""
            <p>
            {' '.join([f"<span style='background-color:#fdd835'>{word}</span>" if (self.no_digits(self.no_punct(word.lower())) in searches) and (word not in esc) else word for word in text.split()])}
            </p>
            """ 
        return inject 

    def add_context(self, data, r, amount=1):
        sents = []
        res_idx = int(data.loc[data.chunks.str.contains(r['chunks'].strip(), regex=False, na=False)].index[0])
        sents += list(data.iloc[res_idx-amount:res_idx].chunks)
        sents += list(data.iloc[res_idx:res_idx+(amount+1)].chunks)
        return '\n'.join(sents)

    def check_metadata(self, r, data, display_date):
        keys = list(r.keys())
        # title
        st.markdown(f"<small><b>Document title: {r['title']}</b></small>", unsafe_allow_html=True)
        
        # date
        if display_date and ('date' in keys) and (re.match('\d', str(r['date']))): 
            st.markdown(f"<small><b>Date: {datetime.strftime(r['date'], '%B %-d, %Y')}</b></small>", unsafe_allow_html=True)
        elif display_date and ('date' in keys) and (not re.match('\d', str(r['date']))):
            st.markdown("<small><b>Date: No date found</b></small>", unsafe_allow_html=True)
        elif display_date and ('date_possible' in keys) and (re.match('\d', r['date_possible'])):
            st.markdown(f"<small><b>Date: {r['date_possible']}</b></small>", unsafe_allow_html=True)
        elif display_date and ('date_possible' in keys) and (not re.match('\d', r['date_possible'])):
            st.markdown("<small><b>Possible Date: No date found</b></small>", unsafe_allow_html=True)
        else:
            st.markdown("<small><b>Date: No date found</b></small>", unsafe_allow_html=True)
        
        # author
        if 'author' in keys:
            st.markdown(f"<small><b>Author: {r['author']}</b></small>", unsafe_allow_html=True)
        else:
            st.markdown("<small><b>Author: No author found</b></small>", unsafe_allow_html=True)

        # newspaper
        if 'newspaper' in keys:
            st.markdown(f"<small><b>Newspaper: {r['newspaper']}</b></small>", unsafe_allow_html=True)
        else:
            st.markdown("<small><b>Newspaper: No newspaper found</b></small>", unsafe_allow_html=True)

    def display_results(self, i, r, data, searches, display_date=True, text_return=True):
        self.check_metadata(r, data, display_date)
        full = r['chunks']
        amount = st.number_input('Choose context length', key=f'num_{i}', value=1, step=1, help='This number represents the amount of sentences to be added before and after the result.')
        if st.button('Add context', key=f'con_{i}'):
            full = self.add_context(data, r, amount)
            if (st.session_state['additional_context'][i] == '') or (len(st.session_state['additional_context'][i]) < len(full)):
                st.session_state['additional_context'][i] = full
        st.markdown(self.inject_highlights(self.escape_markdown(full.replace('\n --', ' --')), searches), unsafe_allow_html=True) 
        st.markdown("<hr style='width: 75%;margin: auto;'>", unsafe_allow_html=True)
        if text_return:
            return full, r 

    def __call__(self):
        for i, r in enumerate(self.results):
            if r['title'] in self.doc_search:
                self.display_results(i, r, self.data, self.searches, display_date=self.display_date)