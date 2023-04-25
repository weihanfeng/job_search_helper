from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS


class GetTopSimilar:
    def __init__(self, data_folder=None, strings=None):
        self.data_folder = data_folder
        self.strings = strings

    def get_top_similar(self, query, k=2):
        # data_folder = os.path.join(os.getcwd(), "../../data")

        embeddings = self._generate_embeddings()
        if self.data_folder:
            docs = self._load_data_docs(self.data_folder, file_prefix="jd")
            vector_store = self._generate_vectorstore(embeddings, docs=docs)
        elif self.strings:
            vector_store = self._generate_vectorstore(embeddings, strings=self.strings)
        else:
            raise ValueError("Must provide either data_folder or strings")

        result = vector_store.similarity_search_with_score(query, k=k)

        return result

    def _load_data_docs(self, data_folder, file_prefix="jd"):
        loader = DirectoryLoader(data_folder, glob=f"{file_prefix}*.txt")
        docs = loader.load()

        return docs

    def _generate_embeddings(
        self, model_name="sentence-transformers/all-mpnet-base-v2", model_kwargs={}
    ):
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name, model_kwargs=model_kwargs
        )

        return embeddings

    def _generate_vectorstore(self, embeddings, docs=None, strings=None):
        if docs:
            db = FAISS.from_documents(docs, embeddings)
        elif strings:
            db = FAISS.from_texts(strings, embeddings)
        else:
            raise ValueError("Must provide either docs or strings")

        return db
