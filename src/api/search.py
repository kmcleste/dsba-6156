import json
import os
import pathlib
import sys
from typing import Optional, Union, Dict, Any

import aiofiles
import faiss
from fastapi import UploadFile
from haystack import Document
from haystack.document_stores import FAISSDocumentStore, BaseDocumentStore
from haystack.nodes import (
    BaseSummarizer,
    TransformersSummarizer,
    DensePassageRetriever,
    BaseRetriever,
    BaseReader,
    FARMReader,
    BaseGenerator,
    QuestionGenerator,
    PreProcessor,
    BasePreProcessor,
)
from haystack.pipelines import (
    ExtractiveQAPipeline,
    BaseStandardPipeline,
    DocumentSearchPipeline,
    MostSimilarDocumentsPipeline,
    SearchSummarizationPipeline,
    QuestionGenerationPipeline,
    QuestionAnswerGenerationPipeline,
)
from haystack.utils import (
    convert_files_to_docs,
    print_answers,
    print_documents,
    print_questions,
)
import torch

from utils.logger import logger


# TODO: Update documentation - at least need docs for class
class HaystackHelper:
    def __init__(self, index: str):
        self.index: str = index
        self.document_store: BaseDocumentStore = self.create_document_store()
        self.retriever: BaseRetriever = self.create_retriever()
        self.reader: BaseReader = self.create_reader()
        self.question_generator: BaseGenerator = self.create_question_generator()
        self.summarizer: BaseSummarizer = self.create_summarizer()
        self.data_path = pathlib.Path(os.getcwd(), "src", "api", "data")

        if not self.data_path.exists():
            os.mkdir(self.data_path)

    def create_document_store(
        self,
        sql_url: str = "sqlite:///faiss_document_store.db",
        embedding_dim: int = 768,
        faiss_index_factory_str: str = "Flat",
        faiss_index: Optional[faiss.swigfaiss.Index] = None,
        return_embedding: bool = False,
        similarity: str = "dot_product",
        embedding_field: str = "embedding",
        progress_bar: bool = True,
        duplicate_documents: str = "skip",
        faiss_index_path: Union[str, pathlib.Path] = None,
        faiss_config_path: Union[str, pathlib.Path] = None,
        isolation_level: str = None,
        n_links: int = 64,
        ef_search: int = 20,
        ef_construction: int = 80,
        validate_index_sync: bool = True,
    ) -> BaseDocumentStore:
        """Initialize an empty document store"""
        try:
            if (
                pathlib.Path(os.getcwd(), "faiss_document_store.db").exists()
                and pathlib.Path(os.getcwd(), "faiss_document_store.json").exists()
            ):
                document_store: BaseDocumentStore = FAISSDocumentStore.load(
                    index_path="faiss_document_store"
                )
                logger.debug("Loaded existing FAISS Document Store")
                return document_store
            else:
                document_store: BaseDocumentStore = FAISSDocumentStore(
                    sql_url=sql_url,
                    embedding_dim=embedding_dim,
                    faiss_index_factory_str=faiss_index_factory_str,
                    faiss_index=faiss_index,
                    return_embedding=return_embedding,
                    index=self.index,
                    similarity=similarity,
                    embedding_field=embedding_field,
                    progress_bar=progress_bar,
                    duplicate_documents=duplicate_documents,
                    faiss_index_path=faiss_index_path,
                    faiss_config_path=faiss_config_path,
                    isolation_level=isolation_level,
                    n_links=n_links,
                    ef_search=ef_search,
                    ef_construction=ef_construction,
                    validate_index_sync=validate_index_sync,
                )
                logger.debug("Created FAISS Document Store")
                return document_store

        except Exception as exc:
            logger.critical(f"Unable to create/load FAISS Document Store: {exc}")
            sys.exit(1)

    def create_retriever(
        self,
        query_embedding_model: Union[
            pathlib.Path, str
        ] = "facebook/dpr-question_encoder-single-nq-base",
        passage_embedding_model: Union[
            pathlib.Path, str
        ] = "facebook/dpr-ctx_encoder-single-nq-base",
        model_version: Optional[str] = None,
        max_seq_len_query: int = 64,
        max_seq_len_passage: int = 256,
        top_k: int = 10,
        use_gpu: bool = False,
        batch_size: int = 16,
        embed_title: bool = True,
        use_fast_tokenizers: bool = True,
        similarity_function: str = "dot_product",
        global_loss_buffer_size: int = 150_000,
        progress_bar: bool = True,
        devices: Optional[list[Union[str, torch.device]]] = None,
        use_auth_token: Optional[Union[str, bool]] = None,
        scale_score: bool = True,
    ) -> BaseRetriever:
        try:
            retriever = DensePassageRetriever(
                document_store=self.document_store,
                query_embedding_model=query_embedding_model,
                passage_embedding_model=passage_embedding_model,
                model_version=model_version,
                max_seq_len_query=max_seq_len_query,
                max_seq_len_passage=max_seq_len_passage,
                top_k=top_k,
                use_gpu=use_gpu,
                batch_size=batch_size,
                embed_title=embed_title,
                use_fast_tokenizers=use_fast_tokenizers,
                similarity_function=similarity_function,
                global_loss_buffer_size=global_loss_buffer_size,
                progress_bar=progress_bar,
                devices=devices,
                use_auth_token=use_auth_token,
                scale_score=scale_score,
            )
            logger.debug("Created DensePassageRetriever")
            return retriever
        except Exception as exc:
            logger.critical(f"Unable to create DensePassageRetriever: {exc}")
            sys.exit(1)

    def create_summarizer(
        self,
        model_name_or_path: str = "facebook/bart-large-cnn",
        model_version: Optional[str] = None,
        tokenizer: Optional[str] = None,
        max_length: int = 200,
        min_length: int = 5,
        use_gpu: bool = True,
        clean_up_tokenization_spaces: bool = True,
        separator_for_single_summary: str = " ",
        generate_single_summary: bool = False,
        batch_size: int = 16,
        progress_bar: bool = True,
        use_auth_token: Optional[Union[str, bool]] = None,
        devices: Optional[list[Union[str, torch.device]]] = None,
    ) -> BaseSummarizer:
        try:
            summarizer = TransformersSummarizer(
                model_name_or_path=model_name_or_path,
                model_version=model_version,
                tokenizer=tokenizer,
                max_length=max_length,
                min_length=min_length,
                use_gpu=use_gpu,
                clean_up_tokenization_spaces=clean_up_tokenization_spaces,
                separator_for_single_summary=separator_for_single_summary,
                generate_single_summary=generate_single_summary,
                batch_size=batch_size,
                progress_bar=progress_bar,
                use_auth_token=use_auth_token,
                devices=devices,
            )
            logger.debug("Created Summarizer")
            return summarizer
        except Exception as exc:
            logger.critical(f"Unable to create Summarizer: {exc}")
            sys.exit(1)

    def create_reader(
        self,
        model_name_or_path: str = "deepset/roberta-base-squad2",
        model_version: Optional[str] = None,
        context_window_size: int = 150,
        batch_size: int = 50,
        use_gpu: bool = False,
        devices: Optional[list[Union[str, torch.device]]] = None,
        no_ans_boost: float = 0.0,
        return_no_answer: bool = False,
        top_k: int = 10,
        top_k_per_candidate: int = 3,
        top_k_per_sample: int = 1,
        num_processes: Optional[int] = None,
        max_seq_len: int = 256,
        doc_stride: int = 128,
        progress_bar: bool = True,
        duplicate_filtering: int = 0,
        use_confidence_scores: bool = True,
        confidence_threshold: Optional[float] = None,
        proxies: Optional[Dict[str, str]] = None,
        local_files_only=False,
        force_download=False,
        use_auth_token: Optional[Union[str, bool]] = None,
    ) -> BaseReader:
        try:
            reader = FARMReader(
                model_name_or_path=model_name_or_path,
                model_version=model_version,
                context_window_size=context_window_size,
                batch_size=batch_size,
                use_gpu=use_gpu,
                devices=devices,
                no_ans_boost=no_ans_boost,
                return_no_answer=return_no_answer,
                top_k=top_k,
                top_k_per_candidate=top_k_per_candidate,
                top_k_per_sample=top_k_per_sample,
                num_processes=num_processes,
                max_seq_len=max_seq_len,
                doc_stride=doc_stride,
                progress_bar=progress_bar,
                duplicate_filtering=duplicate_filtering,
                use_confidence_scores=use_confidence_scores,
                confidence_threshold=confidence_threshold,
                proxies=proxies,
                local_files_only=local_files_only,
                force_download=force_download,
                use_auth_token=use_auth_token,
            )
            logger.debug("Created FARMReader")
            return reader
        except Exception as exc:
            logger.critical(f"Unable to create FARMReader: {exc}")
            sys.exit(1)

    def create_question_generator(
        self, model_name_or_path: str = "valhalla/t5-base-e2e-qg", use_gpu: bool = False
    ) -> BaseGenerator:
        try:
            generator: BaseGenerator = QuestionGenerator(
                model_name_or_path=model_name_or_path, use_gpu=use_gpu
            )
            logger.debug("Created Question Generator")
            return generator
        except Exception as e:
            logger.critical(f"Unable to create Question Generator: {e}")
            sys.exit(1)

    def extractive_qa(
        self, query: str, params: Optional[dict] = None, debug: Optional[bool] = None
    ) -> dict:
        try:
            pipeline: BaseStandardPipeline = ExtractiveQAPipeline(
                reader=self.reader, retriever=self.retriever
            )
            answer: dict = pipeline.run(query=query, params=params, debug=debug)
            return answer
        except Exception as e:
            logger.error(f"Unable to perform extractive search: {e}")
            return {
                "message": "Something went wrong. Unable to perform extractive search."
            }

    def document_search(
        self, query: str, params: Optional[dict] = None, debug: Optional[bool] = None
    ) -> dict:
        try:
            pipeline: BaseStandardPipeline = DocumentSearchPipeline(self.retriever)
            answer: dict = pipeline.run(query=query, params=params, debug=debug)
            return answer
        except Exception as e:
            logger.error(f"Unable to perform document search: {e}")
            return {
                "message": "Something went wrong. Unable to perform document search."
            }

    def search_summarization(
        self, query: str, params: Optional[dict] = None, debug: Optional[bool] = None
    ) -> dict:
        try:
            pipeline: BaseStandardPipeline = SearchSummarizationPipeline(
                summarizer=self.summarizer,
                retriever=self.retriever,
                generate_single_summary=True,
            )
            answer: dict = pipeline.run(query=query, params=params, debug=debug)
            return answer
        except Exception as e:
            logger.error(f"Unable to perform search summarization: {e}")
            return {
                "message": "Something went wrong. Unable to perform search summarization."
            }

    def question_generation(
        self,
        ids: list[str],
        params: Optional[dict] = None,
        debug: Optional[bool] = None,
    ) -> dict:
        try:
            documents: list[Document] = self.document_store.get_documents_by_id(
                ids=ids, index=self.index
            )
            pipeline: BaseStandardPipeline = QuestionGenerationPipeline(
                question_generator=self.question_generator
            )
            answer: dict = pipeline.run(documents=documents, params=params, debug=debug)
            return answer
        except Exception as e:
            logger.error(f"Unable to perform question generation: {e}")
            return {
                "message": "Something went wrong. Unable to perform question generation."
            }

    def question_answer_generation(
        self,
        ids: list[str],
        params: Optional[dict] = None,
        debug: Optional[bool] = None,
    ) -> dict:
        try:
            documents: list[Document] = self.document_store.get_documents_by_id(
                ids=ids, index=self.index
            )
            pipeline: BaseStandardPipeline = QuestionAnswerGenerationPipeline(
                question_generator=self.question_generator, reader=self.reader
            )
            answer: dict = pipeline.run(documents=documents, params=params, debug=debug)
            return answer
        except Exception as e:
            logger.error(f"Unable to perform question:answer generation: {e}")
            return {
                "message": "Something went wrong. Unable to perform question:answer generation."
            }

    def most_similar_docs(self, ids: list[str], top_k: int = 5):
        try:
            pipeline: BaseStandardPipeline = MostSimilarDocumentsPipeline(
                self.document_store
            )
            answer: list[Document] = pipeline.run(
                document_ids=ids, index=self.index, top_k=top_k
            )
            return answer
        except Exception as e:
            logger.error(f"Unable to find most similar documents: {e}")
            return {
                "message": "Something went wrong. Unable to find most similar documents."
            }

    async def write_files(self, files: list[UploadFile]) -> dict:
        if self.data_path.exists():
            for file in files:
                try:
                    contents = file.file.read()
                    async with aiofiles.open(
                        f"{self.data_path}/{file.filename}", "wb"
                    ) as f:
                        await f.write(contents)
                except Exception as exc:
                    logger.error(f"Unable to upload {file.filename}: {exc}")
                    return {"message": f"Unable to upload {file.filename}"}
                finally:
                    file.file.close()

            logger.debug("Successfully uploaded file(s)!")
            return {"message": "Successfully uploaded file(s)!"}
        else:
            logger.error(f"Selected path does not exist: {self.data_path}")
            return {"message": "Selected path does not exist"}

    def write_documents(
        self,
        documents: Union[list[dict], list[Document], pathlib.Path],
        batch_size: int = 10_000,
        duplicate_documents: Optional[str] = "skip",
        headers: Optional[Dict[str, str]] = None,
        update_existing_embeddings: bool = False,
        filters: Optional[Dict[str, Any]] = None,
    ) -> dict:
        try:
            if isinstance(documents, pathlib.Path):
                try:
                    # convert multiple filetypes to dicts using helper function
                    documents = convert_files_to_docs(
                        dir_path=documents, split_paragraphs=True
                    )
                    # further process documents by breaking into smaller chunks
                    processor: BasePreProcessor = PreProcessor(
                        clean_empty_lines=True,
                        clean_whitespace=True,
                        clean_header_footer=True,
                        split_by="word",
                        split_length=500,
                        split_respect_sentence_boundary=True,
                        split_overlap=0,
                    )
                    documents = processor.process(documents)
                except Exception as exc:
                    logger.error(f"Unable to convert files to proper format: {exc}")
                    return {"message": "Unable to convert files to proper format"}
            self.document_store.write_documents(
                documents=documents,
                index=self.index,
                batch_size=batch_size,
                duplicate_documents=duplicate_documents,
                headers=headers,
            )
            self.document_store.update_embeddings(
                retriever=self.retriever,
                index=self.index,
                update_existing_embeddings=update_existing_embeddings,
                filters=filters,
                batch_size=batch_size,
            )
            try:
                self.document_store.save(index_path="faiss_document_store")
            except Exception as exc:
                logger.error(f"Unable to save FAISS Document Store: {exc}")
                return {"message": "Unable to save FAISS Document Store"}

            # removes source files from "data" directory to reduce storage usage
            [pathlib.Path.unlink(f) for f in self.data_path.iterdir() if f.is_file()]

            return {"message": "Successfully uploaded file(s)!"}

        except Exception as exc:
            logger.error(f"Unable to write documents: {exc}")
            return {"message": "Unable to write documents"}

    def delete_documents(
        self,
        ids: Union[list[str], None] = None,
        batch_size: int = 10_000,
        headers: Optional[Dict[str, str]] = None,
        update_existing_embeddings: bool = False,
        filters: Optional[Dict[str, Any]] = None,
    ) -> dict:
        try:
            self.document_store.delete_documents(
                index=self.index, ids=ids, headers=headers, filters=filters
            )
            self.document_store.update_embeddings(
                retriever=self.retriever,
                index=self.index,
                update_existing_embeddings=update_existing_embeddings,
                filters=filters,
                batch_size=batch_size,
            )

            try:
                self.document_store.save(index_path="faiss_document_store")
            except Exception as exc:
                logger.error(f"Unable to save FAISS Document Store: {exc}")
                return {"message": "Unable to save FAISS Document Store"}

            return {"message": f"Successfully deleted {'all' if ids is None else ids}"}

        except Exception:
            return {"message": f"Unable to delete {'all' if ids is None else ids}"}

    def describe_documents(self):
        try:
            return self.document_store.describe_documents(index=self.index)
        except Exception:
            return {"message": "There was an error retrieving index information"}
