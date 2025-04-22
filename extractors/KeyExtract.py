from extractors.BaseExtractor import BaseExtractor
from typing import List
from langchain_ollama import OllamaLLM



class KeyExtractor(BaseExtractor):
    def __init__(self):
        BaseExtractor.__init__(self)
        self.llm = OllamaLLM(model="llama3:8b")
        self.prompt_prereq = '''You are given an extracted "prerequisites" section from the syllabus. Your task is to:
        1. Extract keyphrases that represent clear and relevant educational concepts or disciplines (they can be found on Wikipedia). This could include specific theories, methodologies, techniques, or subject areas.
        2. If necessary, correct any misspelled or ambiguous parts to improve accuracy. Additionally, standardize terms to ensure consistency (e.g., "machine learning" instead of "ML").
        3. Consider only educational concepts explicitly mentioned within the provided "prerequisites" section.
        4. Don't provide the level of comprehension of certain concepts (like 'fundamentals' or 'basics'), provide the concepts alone.

        Output Format:
        Please provide a comma-separated list of unique educational concepts or disciplines WITHOUT ANY ADDITIONAL CONCEPTS OR EXPLANATIONS.
        If there are no prerequisites, output an empty string.

        Prerequisites section: ```<prerequisites>```.
        Don't provide ANY ADDITIONAL CONCEPTS OR EXPLANATIONS.
        '''

        self.prompt_coveres = '''You are an expert tasked with extracting educational concepts from the course syllabi. 
        Your goal is to identify and output SPECIFIC, WELL-DEFINED EDUCATIONAL CONCEPTS from a provided course description.
        1. Identify keyphrases that represent UNAMBIGUOUS, SPECIFIC, WELL-DEFINED EDUCATIONAL CONCEPTS (e.g., theories, methodologies, techniques, or subject areas). 
        The concept must be EDUCATIONAL, RELEVANT to the course, and DEFINABLE (e.g., it should be possible to look it up in a reliable reference such as Wikipedia).
        2. Exclude general activities (e.g., "debugging", "implementation") or overly broad terms (e.g., "structured data files", "transformations", "complex data structures").
        3. Correct any misspelled or ambiguous keyphrases. Standardize terms for clarity (e.g., use "machine learning" instead of "ML").
        4. If a phrase cannot be reliably verified as a VALID concept, exclude it. Exclude phrases that do not correspond to standard or well-defined educational concepts (e.g., "mapping matrix").

        Output Format: 
        Provide a comma-separated list of unique and specific educational concepts. DO NOT INCLUDE ANY COMMENTS OR EXPLANATIONS.

        Program content for the course: "Introduction to computer science":
        "Introduction to the scope and subject of computer science, development of computer science, selected computer models. Algorithm and basic concepts, computational complexity of an algorithm, basic, classes of computational complexity, taxonomy and meaning. Formal languages, formal grammar, Chomsky classification, grammatical parsing, compilers, structure and operation of a compiler, review of compilation algorithms. Paradigms of programming languages ​​- meaning and review. Introduction to information theory, information measures. Uncertainty, the concept of entropy. Compression. Shannon, Fano and Huffman coding. Message transmission, channel capacity. Kolmogorov information complexity. Computer networks. Types and topologies of networks. Wired and wireless networks: Ethernet, WiFi, Bluetooth. ISO-OSI model. Selected network protocols. Selected applications of computers. Application programming, modeling and simulations, large-scale computing, embedded systems, ubiquitous computing."

        '''
    
    def create_prompt(self, prerequisites: str):
        return self.prompt_prereq.replace("<prerequisites>", prerequisites)

    def extractKeyWords(self, doc:str, top_k:int=20) -> List[str]:
        return self.llm.invoke(self.create_prompt(doc)).strip().split(",")

    # def extractKeyWords(self, doc:str, top_k:int) -> List[str]:
    #     extracted_concepts = sefextract_concepts(llm_llama, create_prompt(prerequisite_text))
    #     sentence_list = self.split_into_sentences(doc)
    #     phrase_list = self.generate_candidate_keywords(sentence_list)
    #     word_scores = self.calculate_word_scores(phrase_list)
    #     keyword_candidates = self.generate_candidate_keyword_scores(phrase_list, word_scores)

    #     sorted_keywords = sorted(keyword_candidates.items(), key=lambda item: item[1], reverse=True)[:top_k]
    #     return list(map(lambda x: x[0], sorted_keywords))
    
    