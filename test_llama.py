from ollama import chat
LLM_MODEL = "gemma3:4b"

def generate_answer(query: str) -> str:
    response = chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": "তুমি একজন সহজ ভাষায় উত্তর দেওয়া বাংলা ভয়েস অ্যাসিস্ট্যান্ট। সংক্ষেপে উত্তর দাও।"
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )
    return response["message"]["content"]

llm_response = generate_answer("তো তোমার নাম কি তোমার বয়স কত")
print(llm_response) 