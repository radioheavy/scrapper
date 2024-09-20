from transformers import pipeline
import spacy
import torch

class ContentAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        
    def analyze(self, text):
        doc = self.nlp(text)
        
        # Named Entity Recognition
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        # Summarization
        summary = self.summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
        
        # Sentiment Analysis
        sentiment = self.classifier(text)[0]
        
        # Keyword Extraction
        keywords = [token.text for token in doc if token.is_stop != True and token.is_punct != True]
        
        return {
            "entities": entities,
            "summary": summary,
            "sentiment": sentiment,
            "keywords": keywords[:10]  # Top 10 keywords
        }