def context_precision(retrieved, relevant):
    retrieved_text = " ".join(retrieved).lower()
    relevant_text = " ".join(relevant).lower()
    
    overlap = sum(1 for word in relevant_text.split() if word in retrieved_text)
    
    return overlap / len(relevant_text.split()) if relevant_text else 0


def context_recall(retrieved, relevant):
    retrieved_text = " ".join(retrieved).lower()
    relevant_text = " ".join(relevant).lower()
    
    overlap = sum(1 for word in retrieved_text.split() if word in relevant_text)
    
    return overlap / len(retrieved_text.split()) if retrieved_text else 0

def routing_accuracy(predicted, actual):
    return 1 if predicted == actual else 0

def faithfulness(answer, context):
    answer_words = set(answer.lower().split())
    context_words = set(" ".join(context).lower().split())
    
    common = answer_words.intersection(context_words)
    
    return len(common) / len(answer_words) if answer_words else 0