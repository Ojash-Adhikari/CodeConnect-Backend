import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import re

# Setup device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model/tokenizer global cache
_model = None
_tokenizer = None

def load_model():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        model_name = "distilgpt2"
        _tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        _tokenizer.pad_token = _tokenizer.eos_token  # For padding safety
        _model = GPT2LMHeadModel.from_pretrained(model_name).to(device)

def generate_question(difficulty: str) -> str:
    load_model()

    few_shot_prompt = f"""
Easy:
Write a function that adds two numbers and returns the result.
Write a program to find the maximum number in a list.
Write a function that checks if a string is a palindrome.

Medium:
Implement a binary search algorithm.
Write a function that returns the nth Fibonacci number using recursion.
Implement a queue using two stacks.

Hard:
Design an LRU cache with O(1) get and put operations.
Write a program that solves the N-Queens problem using backtracking.
Implement a concurrent hash map with support for locking.

{difficulty}:
"""

    inputs = _tokenizer(few_shot_prompt, return_tensors="pt", max_length=256, truncation=True).to(device)

    outputs = _model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_new_tokens=150,
        num_return_sequences=1,
        temperature=0.5,
        top_p=0.9,
        top_k=50,
        no_repeat_ngram_size=3,
        do_sample=True,
        early_stopping=True
    )

    decoded = _tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Post-processing
    generated = decoded.replace(few_shot_prompt, "").strip()
    question = re.split(r'\n\n|\nExample|\nInput', generated)[0]
    question = question.split('?')[0] + '?' if '?' in question else question + '?'
    return question

def refine_question(question: str) -> str:
    if not question:
        return question

    # Capitalize first letter and ensure it ends with '?'
    question = question[0].upper() + question[1:]
    question = question.rstrip('?.') + '?'

    fixes = [
        (r'\bimplement a\b', 'implement'),
        (r'\bwrite a\b', 'write'),
        (r'\bthat that\b', 'that'),
        (r'\bwhich which\b', 'which'),
    ]
    for pattern, replacement in fixes:
        question = re.sub(pattern, replacement, question, flags=re.IGNORECASE)
    return question

def is_coherent_question(question: str) -> bool:
    if not question or len(question.split()) < 8:
        return False

    if not question.lower().startswith(('write', 'implement', 'create', 'develop')):
        return False

    tech_terms = {'function', 'algorithm', 'array', 'string', 'class', 'tree', 'graph', 'sort', 'search', 'matrix'}
    words = set(word.lower() for word in re.findall(r'\w+', question))

    if not tech_terms.intersection(words):
        return False

    if not any(punct in question for punct in ('.', '?', '!')):
        return False

    return True

def generate_high_quality_question(difficulty: str, max_attempts: int = 5) -> str:
    for _ in range(max_attempts):
        question = generate_question(difficulty)
        question = refine_question(question)
        if is_coherent_question(question):
            return question

    fallbacks = {
        'Easy': "Write a function that reverses a given string.",
        'Medium': "Implement an algorithm to find the longest substring without repeating characters.",
        'Hard': "Design a concurrent data structure that implements a thread-safe cache with LRU eviction policy."
    }
    return fallbacks.get(difficulty, "Write a function that solves a programming problem.")
