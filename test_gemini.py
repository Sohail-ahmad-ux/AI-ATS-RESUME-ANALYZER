from config import llm

response = llm.invoke(
    "Say 'Gemini is working' in one sentence."
)

print(response.content)