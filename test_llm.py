from config import llm

response = llm.invoke("Say hello.")

print(response.content)