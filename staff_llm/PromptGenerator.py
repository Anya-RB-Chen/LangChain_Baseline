"""
    PromptGenerator.py
    This file handles the .txt files as the dataset for embedding search.
    We first embed the text and then store them into '../embeddings'
    
    Available formats:
    1. txt
    2. json
    
    Available Embeddings:
    1. Instruct Embedding
"""

import os
import re
import fitz
import docx2txt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from InstructorEmbedding import INSTRUCTOR
import torch
from bs4 import BeautifulSoup

device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = INSTRUCTOR('../instructor-embedding/instructor-large')
model = INSTRUCTOR('../instructor-embedding/instructor-large')

class PromptGenerator:
    def __init__(self, knowledge_dir = 'documents', k = 5, chunk_length = 2048):
        self.knowledge_dir = knowledge_dir  # Path to the knowledge base
        self.k = k  # The number of most related paragraphs to be included in the prompt
        self.chunk_length = chunk_length  # Length of each chunk of text
        self._read_paragraphs()


    # Read all pdf, docx, txt and html files in the given directory and convert them into plain text
    def _read_files(self, directory):
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.pdf') or filename.endswith(
                        '.docx') or filename.endswith('.html') or filename.endswith('.txt'):
                    filepath = os.path.join(root, filename)

                    with open(filepath, 'rb') as f:
                        if filename.endswith('.pdf'):
                            text = ""
                            pdfdoc = fitz.open(stream=f.read(), filetype="pdf")

                            for page in pdfdoc:
                                text += page.get_text()

                        elif filename.endswith('.docx'):
                            text = docx2txt.process(f)
                        elif filename.endswith('.txt'):
                            # encode with utf-8 to avoid UnicodeDecodeError
                            text = f.read().decode('utf-8')
                        else:
                            soup = BeautifulSoup(f, 'html.parser')
                            text = soup.get_text()
                        if not filename.endswith('txt'):
                            text = text.replace('\n', '')
                        yield text


    # Split the text into chunks with a length of chunk_length and clean their format
    def _split_text(self, text, chunk_length):
        text_chunks = text.split('\n')

        return text_chunks
    
    # def _split_txt(self, text):
    #     # Used for chunk txt file
    #     text_chunks = text.split('\n')
    #     return text_chunks

    # Paragraph embedding
    def _embed_paragraphs(self, paragraphs, chunk_length):
        text_instruction_pairs = []
        
        if type(paragraphs) == str:
            text_instruction_pairs.append([" ", paragraphs])
        elif type(paragraphs) == list:
            for paragraph in paragraphs:
                text_instruction_pairs.append([" ", paragraph])
        else:
            raise TypeError("The type of paragraphs should be str or list.")
        # print(len(text_instruction_pairs))
        # print(text_instruction_pairs[0])
        customized_embeddings = model.encode(text_instruction_pairs)
        return customized_embeddings

    # Calculate the similarity between the question embedding and the embedding of each paragraph,
    # and find the k paragraphs with the highest similarity
    def _find_similar_paragraphs(self, embedded_paragraphs, embedded_question, k):
        
        similarity_scores = cosine_similarity(embedded_paragraphs, embedded_question)
        top_k_indices = np.argsort(similarity_scores, axis=0)[-k:].flatten()
        top_k_scores = similarity_scores[top_k_indices].flatten()
        return top_k_indices, top_k_scores


    # Prompt generation
    def _generate_prmopt(self, paragraphs, top_k_indices, question, log_text, top_k_scores):
        QA_PROMPT_STAFF = """You are PolyuGPT. You are an AI-based question answering virtual assistant. You act as a polite and considerate consultant. You are talking to a user who interests in the academic staff of Hong Kong Polytechnic University. You are capable to present the professional knowledge about the academic staff's name, department, graduate schools, degrees, and research interests.\nYou are given the following extracted parts of a long document and a question. Provide a conversational answer.\nIf the user is greeting you, you can answer it freely and energetically.\nIf the question is not about the information of PolyU, just chat with user casually.\nIf the question is about the information of PolyU, but you don't know the answer, just say "Sorry, I'm not sure about it. You are recommended to review the official website of PolyU for more information.\nQuestion: {question}\n=========\n{context}\n=========\nAnswer in Markdown:"""
        
        context = ''
        for i in range(len(top_k_indices)):
            context += paragraphs[top_k_indices[i]]
            context += '\n'
        input_text = QA_PROMPT_STAFF.format(question=question, context=context)
        
        # Display text: used to show the similarity score of each candidates
        _context = ''
        for i in range(len(top_k_indices)):
            # show 5 decimal places for each score
            _context += '- {:.5f}: {}\n'.format(top_k_scores[i], paragraphs[top_k_indices[i]])
            
        display_text = QA_PROMPT_STAFF.format(question=question, context=_context)
        
        # Show the prompt in a more readable format
        print("\n========== Prompt ==========")
        print(display_text)
        print("============================")
        
        log_text += "\n========== Prompt ==========\n"
        log_text += display_text
        log_text += "\n============================\n"
        
        return input_text, log_text
    

    def _read_paragraphs(self):
        self._text_data = list(self._read_files(self.knowledge_dir))
        self._paragraphs = []
        for text in self._text_data:
            self._paragraphs += self._split_text(text, self.chunk_length)
        # print(self._paragraphs)

        self._embedded_paragraphs = self._embed_paragraphs(self._paragraphs, self.chunk_length)
    

    def get_prompt(self, question, log_text):
        embedded_question = self._embed_paragraphs(question, self.chunk_length)
        top_k_indices, top_k_scores = self._find_similar_paragraphs(self._embedded_paragraphs,
                                                embedded_question, self.k)
        
        prompt, log = self._generate_prmopt(self._paragraphs, top_k_indices, question, log_text, top_k_scores)
        return prompt, log


if __name__ == '__main__':
    promptGenerator = PromptGenerator()
    prompt = promptGenerator.get_prompt(['Tell me about the Wei Lun Hall'])
    print(prompt)
