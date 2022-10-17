import os
import pathlib

from common import HaystackHelper


_haystack = HaystackHelper(index="semantic")

# docs = _haystack.load_json(path="src/search/data/us-500.json")
# docs_converted = _haystack.json2document(documents=docs)

docs_converted = pathlib.Path(os.getcwd(), "src", "search", "data")

_haystack.write_documents(documents=docs_converted)

query = input("Enter a search query: ")

answer = _haystack.extractive_search(query=query)["answers"][0]

print(f"answer: {answer.answer}\nscore: {answer.score}\ncontext: {answer.context}")
