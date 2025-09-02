"""
cv_trainer.py: Train a custom spaCy NER model for Spanish CV entity extraction using Doccano-annotated data.
"""
import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
from pathlib import Path
import random
import json
from typing import List, Dict, Any

def load_doccano_data(json_path: str) -> List[Dict[str, Any]]:
    """
    Load Doccano JSONL export (list of dicts with 'text' and 'labels').
    Each label: [start, end, label].
    """
    data = []
    with open(json_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            data.append(item)
    return data

def convert_to_spacy_format(doccano_data: List[Dict[str, Any]]) -> List:
    """
    Convert Doccano data to spaCy training format: (text, {'entities': [(start, end, label)]})
    """
    spacy_data = []
    for item in doccano_data:
        entities = [(start, end, label) for start, end, label in item.get('labels', [])]
        spacy_data.append((item['text'], {'entities': entities}))
    return spacy_data

def train_spacy_ner(train_data: List, output_dir: str = "./custom_cv_model", n_iter: int = 20) -> str:
    """
    Train a spaCy NER model on provided data. Returns output directory path.
    """
    nlp = spacy.blank("es")
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")
    else:
        ner = nlp.get_pipe("ner")
    # Add labels
    for _, annotations in train_data:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])
    # Training loop
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        random.shuffle(train_data)
        losses = {}
        batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            examples = []
            for text, annots in batch:
                examples.append(Example.from_dict(nlp.make_doc(text), annots))
            nlp.update(examples, drop=0.3, losses=losses)
        print(f"Iteration {itn+1}, Losses: {losses}")
    # Save model
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    nlp.to_disk(output_dir)
    return output_dir
