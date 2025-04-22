# Educational Concept Extraction Benchmark

This project presents a comparison between a custom solution for extracting educational concepts, referred to as **Llama 3.1**, and several well-established keyphrase extraction methods.

The aim is to evaluate how well these systems identify key educational concepts from academic texts, using standard evaluation metrics: **Precision**, **Recall**, **F1 Score**, and their respective values at top output (denoted with @O).

## 📊 Results Summary

| Method        | Precision | Recall | F1 Score | Precision@O | Recall@O | F1@O Score |
|---------------|-----------|--------|----------|--------------|----------|------------|
| **Llama 3.1**      | 0.74      | 0.72   | 0.72     | 0.76         | 0.71     | 0.73       |
| Position Rank | 0.52      | 0.68   | 0.59     | 0.55         | 0.55     | 0.55       |
| YAKE          | 0.47      | 0.64   | 0.54     | 0.54         | 0.54     | 0.54       |
| TextRank      | 0.53      | 0.70   | 0.60     | 0.56         | 0.55     | 0.56       |
| RAKE          | 0.43      | 0.67   | 0.51     | 0.46         | 0.46     | 0.46       |

## 🧠 Dataset Description

To the best of our knowledge, no publicly available dataset exists specifically for mining educational concepts from syllabi. To address this gap, we created a new benchmark dataset by:

1. Collecting syllabi for **88 STEM courses** at AGH University of Krakow.
2. Automatically extracting "Prerequisite" and "Program Content" sections.
3. Manually annotating the data with educational concepts, with annotations reconciled by two domain experts.

## 🧪 Baselines and Evaluation

The following keyphrase extraction algorithms were used as baselines:

- **RAKE** (Rose et al., 2010)
- **YAKE** (Campos et al., 2020)
- **TextRank** (Mihalcea & Tarau, 2004)
- **PositionRank** (Florescu & Caragea, 2017)

Metrics include:
- **Precision**, **Recall**, **F1 Score**
- **F1@𝒪**: Evaluates performance when the number of predicted keyphrases is matched to the number of ground-truth keyphrases (Yuan et al., 2020)

We use **Porter stemming** [(Porter, 1980)] for text normalization and **macro-averaging** to compute aggregate scores.

## 📘 References
- Gacek, P. & Adrian, W.T. (2025). Automatic Curriculum Cohesion Analysis Based on Knowledge Graphs. In Hybrid Models for Coupling Deductive and Inductive Reasoning. Springer
- Yuan et al. (2020). One Size Does Not Fit All: Generating and Evaluating Variable Number of Keyphrases. ACL
- Porter (1980). An algorithm for suffix stripping. Program
- Rose et al. (2010). Automatic Keyword Extraction from Individual Documents. Text Mining: Applications and Theory
- Campos et al. (2020). YAKE! Keyword extraction from single documents using multiple local features. Information Sciences
- Mihalcea & Tarau (2004). TextRank: Bringing Order into Text. EMNLP
- Florescu & Caragea (2017). PositionRank: An Unsupervised Approach to Keyphrase Extraction from Scholarly Documents. ACL

## 📬 Contact

For questions or collaborations, feel free to reach out via paulina.gacek.pl@gmail.com.
