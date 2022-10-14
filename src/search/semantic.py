import os
import pathlib

from common import HaystackHelper


_haystack = HaystackHelper(index="semantic")

documents = [{"content": "This is document 1"}, {"content": "This is document 2"}]

_haystack.write_documents(documents=pathlib.Path(os.getcwd(), "src", "search", "data"))
print(_haystack.document_store.get_all_documents(index="semantic"))
