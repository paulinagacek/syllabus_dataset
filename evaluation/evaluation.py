import re, json
from difflib import SequenceMatcher
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import Counter

# Initialize the Porter Stemmer
stemmer = PorterStemmer()

def read_json_from_file(filename):
  try:
    with open(filename, 'r') as file:
      data = json.load(file)
      return data
  except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    return []
  except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{filename}'.")
    return []

def preprocess_and_stem_phrases(phrases):
    """Preprocess phrases: lowercasing, removing extra spaces, and stemming."""
    stemmed_phrases = []
    for phrase in phrases:
        phrase = re.sub(r'\s+', ' ', phrase.strip().lower())
        stemmed_words = [stemmer.stem(word) for word in word_tokenize(phrase)]
        stemmed_phrases.append(' '.join(stemmed_words))
    return phrases

def calculate_match_score_at_O(gt_phrases, extracted_phrases, k, threshold=0.8):
    """Calculate F1@O, considering top k predictions."""
    matches = 0
    total_gt = len(gt_phrases)
    top_k_extracted = extracted_phrases[:k]
    matched_indices = set()

    for gt_phrase in gt_phrases:
        for i, extracted_phrase in enumerate(top_k_extracted):
            if i in matched_indices:
                continue
            # Check if phrases are similar or one contains the other
            similarity = SequenceMatcher(None, gt_phrase, extracted_phrase).ratio()
            if similarity >= threshold or gt_phrase in extracted_phrase or extracted_phrase in gt_phrase:
                matches += 1
                matched_indices.add(i)
                break

    precision = matches / len(top_k_extracted) if top_k_extracted else 0
    recall = matches / total_gt if total_gt else 0
    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1_score

def calculate_match_score(gt_phrases, extracted_phrases, threshold=0.8):
    """Calculate match score based on partial matching and containment."""
    matches = 0
    total_gt = len(gt_phrases)
    matched_indices = set()
    
    for gt_phrase in gt_phrases:
        for i, extracted_phrase in enumerate(extracted_phrases):
            if i in matched_indices:
                continue
            # Check if phrases are similar or one contains the other
            similarity = SequenceMatcher(None, gt_phrase, extracted_phrase).ratio()
            if similarity >= threshold or gt_phrase in extracted_phrase or extracted_phrase in gt_phrase:
                matches += 1
                matched_indices.add(i)
                break
    precision = matches / len(extracted_phrases) if extracted_phrases else 0
    recall = matches / total_gt if total_gt else 0
    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1_score

def evaluate_concepts(extractor_name: str, evaluation_data, threshold=0.8):
    """Evaluate the concept extraction results with F1@O."""
    overall_precision = []
    overall_recall = []
    overall_f1 = []
    overall_precision_at_O = []
    overall_recall_at_O = []
    overall_f1_at_O = []

    for gt_concepts, extracted_concepts in evaluation_data:
        # Preprocess the phrases with stemming
        gt_concepts = preprocess_and_stem_phrases(gt_concepts)
        if len(gt_concepts) == 0: continue
        extracted_concepts = preprocess_and_stem_phrases(
            [phrase for phrase in ','.join(extracted_concepts).split(',') if phrase.strip()]
        )

        k = len(gt_concepts)  # Top k is the number of ground-truth keyphrases
        precision, recall, f1_score = calculate_match_score(gt_concepts, extracted_concepts, threshold)
        precision_at_O, recall_at_O, f1_score_at_O = calculate_match_score_at_O(gt_concepts, extracted_concepts, k, threshold)
        overall_precision.append(precision)
        overall_recall.append(recall)
        overall_f1.append(f1_score)
        overall_precision_at_O.append(precision_at_O)
        overall_recall_at_O.append(recall_at_O)
        overall_f1_at_O.append(f1_score_at_O)
        
        # print(f"GT Concepts: {gt_concepts}")
        # print(f"Extracted Concepts: {extracted_concepts}")
        # print(f"Precision: {precision:.2f}, Recall: {recall:.2f}, F1: {f1_score:.2f}")
        # print(f"Precision@O: {precision_at_O:.2f}, Recall@O: {recall_at_O:.2f}, F1@O: {f1_score_at_O:.2f}\n")

    # Compute macro-averaged metrics
    avg_precision = sum(overall_precision) / len(overall_precision) if overall_precision else 0
    avg_recall = sum(overall_recall) / len(overall_recall) if overall_recall else 0
    avg_f1_score = sum(overall_f1) / len(overall_f1) if overall_f1 else 0
    avg_precision_at_O = sum(overall_precision_at_O) / len(overall_precision_at_O) if overall_precision_at_O else 0
    avg_recall_at_O = sum(overall_recall_at_O) / len(overall_recall_at_O) if overall_recall_at_O else 0
    avg_f1_score_at_O = sum(overall_f1_at_O) / len(overall_f1_at_O) if overall_f1_at_O else 0
    
    if extractor_name != "":
        print(f"### {extractor_name}")
    print(f"Precision: {avg_precision:.2f}")
    print(f"Recall: {avg_recall:.2f}")
    print(f"F1 Score: {avg_f1_score:.2f}")
    print(f"Precision@O: {avg_precision_at_O:.2f}")
    print(f"Recall@O: {avg_recall_at_O:.2f}")
    print(f"F1@O Score: {avg_f1_score_at_O:.2f}")
    print("\n")