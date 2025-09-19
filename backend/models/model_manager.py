from transformers import pipeline


class ModelManager:
def __init__(self):
# extractive QA (fast and small)
self.qa = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')
# summarization (distilbart light model)
self.summarizer = pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')
# translator example (you can add MarianMT models)


def answer(self, question: str, context: str):
input = {"question": question, "context": context}
output = self.qa(input)
return output


def summarize(self, text: str, max_length: int = 150):
out = self.summarizer(text, max_length=max_length, min_length=40, do_sample=False)
return out[0]['summary_text']