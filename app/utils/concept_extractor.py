from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
import os

class ConceptExtractor:
    def __init__(self):
        self.llm = OpenAI(temperature=0)
        self.concept_template = """
        Extract key educational concepts from the following text and their relationships:
        
        Text: {text}
        
        Format the output as:
        Concept: [concept name]
        Description: [brief description]
        Related to: [related concept names, comma separated]
        """
        
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template=self.concept_template
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
        
    def extract_concepts(self, text):
        # Split text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_text(text)
        
        concepts = []
        for chunk in chunks:
            result = self.chain.run(chunk)
            concepts.append(self.parse_concept_output(result))
        
        return concepts
    
    def parse_concept_output(self, output):
        # Parse the LLM output into structured format
        lines = output.strip().split('\n')
        concept_data = {}
        
        for line in lines:
            if line.startswith('Concept:'):
                concept_data['name'] = line.replace('Concept:', '').strip()
            elif line.startswith('Description:'):
                concept_data['content'] = line.replace('Description:', '').strip()
            elif line.startswith('Related to:'):
                concept_data['related'] = [
                    r.strip() 
                    for r in line.replace('Related to:', '').split(',')
                ]
        
        return concept_data