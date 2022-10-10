from haystack.document_stores import FAISSDocumentStore, BaseDocumentStore
from haystack.nodes import BaseRetriever, DensePassageRetriever
from typing import Optional, List
from haystack import Document


class DocumentStore:
    def __init__(self, index: Optional[str] = "document"):
        self.document_store: BaseDocumentStore = FAISSDocumentStore(
            vector_dim=None,
            embedding_dim=768,
            faiss_index_factory_str="Flat",
            faiss_index=None,
            return_embedding=False,
            index=index,
            similarity="dot_product",
            embedding_field="embedding",
            progress_bar=True,
            duplicate_documents="overwrite",
            faiss_index_path=None,
            faiss_config_path=None,
            isolation_level=None,
            n_links=64,
            ef_search=20,
            ef_construction=80,
            validate_index_sync=True,
        )
        self.retriver: BaseRetriever = DensePassageRetriever(
            document_store=self.document_store,
            query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
            passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
            max_seq_len_query=64,
            max_seq_len_passage=256,
            top_k=10,
            use_gpu=False,
            batch_size=16,
            embed_title=True,
            use_fast_tokenizers=True,
            similarity_function="dot_product",
            global_loss_buffer_size=150000,
            progress_bar=True,
            devices=None,
            use_auth_token=None,
            scale_score=True,
        )

    def save_document_store(self, name: str) -> None:
        self.document_store.save(name)

    @classmethod
    def load_document_store(cls, path: str) -> None:
        return FAISSDocumentStore.load(path)

    def index_documents(
        self, documents: List[dict] | List[Document], index: str = "document"
    ):
        self.document_store.write_documents(
            documents=documents,
            index=index,
            batch_size=10_000,
            duplicate_documents=None,
            headers=None,
        )
        self.document_store.update_embeddings(
            retriever=self.retriver,
            index=index,
            update_existing_embeddings=True,
            filters=None,
            batch_size=10_000,
        )

    def get_documents(self, index: Optional[str] = "document"):
        return [
            x.content
            for x in self.document_store.get_all_documents_generator(index=index)
        ]
