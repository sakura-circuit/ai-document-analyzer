def build_prompt(question: str, context: str) -> str:

    return f"""
Answer the question using ONLY the provided context.

If the answer is not present, say:

"I could not find the answer in the document."

Context:

{context}

Question:

{question}

Answer:
"""
