# Quick Test Script
from langchain_community.llms import Ollama
llm = Ollama(model="llama3")
print(llm.invoke("Explain Return on Equity in one sentence."))