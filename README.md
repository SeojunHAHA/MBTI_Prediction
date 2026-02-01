# MBTI Personality Classification from Text using RoBERTa with LoRA

This repository contains the code and notebooks for the project  
**“Myers–Briggs Personality Classification from Text Using RoBERTa with LoRA”**,  
conducted as part of NLP coursework at the University of Southern Denmark.

The project investigates whether transformer-based language models can infer
MBTI personality types from user-generated text by formulating the task as a
**16-class single-label classification problem**.

---

## Overview

Personality prediction from text is challenging due to:
- the abstract nature of personality traits,
- noisy and self-reported labels,
- and severe class imbalance across MBTI categories.

In this project, we:
- fine-tune a **RoBERTa-base** model using **Low-Rank Adaptation (LoRA)**,
- compare performance against an unfine-tuned baseline,
- analyze the impact of **data quality vs. data quantity**,
- and evaluate results at both **type-level** and **axis-level** (E/I, N/S, T/F, J/P).

The best-performing model achieves **30.77% accuracy**, significantly outperforming
the unfine-tuned baseline (3.01%).

---

## Dataset

This project uses large-scale Reddit-based MBTI datasets:

- **Reddit MBTI Dataset (Kaggle)**  
  https://www.kaggle.com/datasets/minhaozhang1/reddit-mbti-dataset

- **Kaggle MBTI Cleaned Dataset (Hugging Face)**  
  https://huggingface.co/datasets/Shunian/kaggle-mbti-cleaned

Notes:
- MBTI labels are **self-reported**, introducing label noise.
- The datasets are **highly imbalanced**, with types such as INFP, INTP, and INFJ dominating.

Due to licensing and size constraints, **datasets are not included in this repository**.  
After downloading, place the data under:

```text
Data/
```
---

## Preprocessing

Key preprocessing steps include:
- lowercasing and removal of URLs and non-English characters,
- filtering texts shorter than 20 characters or longer than 3,000 characters,
- removal of explicit MBTI mentions to prevent label leakage,
- discarding texts longer than 256 tokens instead of truncation.

To mitigate severe class imbalance, a **cluster-based downsampling** strategy is applied:
- sentence embeddings are generated using a MiniLM encoder,
- overrepresented classes are clustered using MiniBatch K-Means,
- semantically central samples are selected to preserve diversity.

---

## Method

- **Model**: RoBERTa-base
- **Task**: 16-class single-label classification
- **Fine-tuning**: Low-Rank Adaptation (LoRA)
- **Loss**: Categorical Cross-Entropy

LoRA enables efficient experimentation by freezing the pre-trained backbone and
training only low-rank adapter parameters, significantly reducing computational
cost and overfitting risk.

---

## Results

- Best accuracy: **30.77%**
- Data quality was more important than raw dataset size.
- Axis-level evaluation shows:
  - higher performance on **E/I** and **N/S** dimensions,
  - lower performance on **T/F** and **P/J**, which are harder to infer from text.

Despite accuracy improvements, **Macro-F1 scores remain low** due to extreme class
imbalance, indicating limited generalization across all MBTI types.

---

## Repository Structure

```text
MBTI_Prediction/
├── notebooks/              # Original EDA and preprocessing notebooks
├── Newnotebooks/           # Updated EDA and preprocessing notebooks
├── Data/                   # Dataset directory (not included)
├── Figures/                # Training curves and evaluation outputs (not included)
├── Model/                  # Trained models (not included)
├── .gitignore
└── README.md
```
---

## Environment

Python 3.10 is recommended.

Install dependencies with:
```bash
pip install -r requirements.txt
```