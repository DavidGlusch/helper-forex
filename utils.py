from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_chunks(data: dict) -> list:
    """
    Extracts question alternatives from the data.

    Args:
        data (dict): The data.

    Returns:
        list: The list of question alternatives.
    """
    chunks = []
    for faq_item in data:
        question_alternatives = faq_item["Question_original_alternatives"]
        chunks.extend(question_alternatives)

        question_short_alternatives = faq_item["Question_short_alternatives"]
        chunks.extend(question_short_alternatives)
    return chunks


def get_similar_questions(chunks: list, question: str) -> list:
    """
    Calculates the similarity between the user's question and the question alternatives.

    Args:
        chunks (list): The list of question alternatives.
        question (str): The user's question.

    Returns:
        list: The list of similarity scores.
    """
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(chunks)

    question_vector = tfidf_vectorizer.transform([question])
    similarities = cosine_similarity(question_vector, tfidf_matrix).flatten()
    return similarities


def get_best_fitting_question(similarities: list, chunks: list) -> str:
    """
    Finds the best fitting question based on similarity scores.

    Args:
        similarities (list): The list of similarity scores.
        chunks (list): The list of question alternatives.

    Returns:
        str: The best fitting question.
    """
    sorted_indices = similarities.argsort()[::-1]
    sorted_chunks = [chunks[i] for i in sorted_indices]
    best_fitting_question = sorted_chunks[0]
    return best_fitting_question
