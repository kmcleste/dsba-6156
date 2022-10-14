from common import DocumentStore


class FAQ:
    def __init__(self):
        self.doc_store = DocumentStore(index="FAQ", database_name="faq")

    def get_docs(self):
        self.doc_store.index_documents(
            documents=[{"content": "This is a document"}], index="FAQ"
        )
        return self.doc_store.get_documents(index="FAQ")


def main():
    print(FAQ().get_docs())


if __name__ == "__main__":
    main()
