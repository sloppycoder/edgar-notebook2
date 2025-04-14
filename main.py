import os
from dotenv import load_dotenv
from edgar_funcs.rag.vectorize import TextChunksWithEmbedding

load_dotenv()


def load_pickle(
    cik: str,
    accession_number: str,
    embedding_model: str = "text-embedding-3-small",
    embedding_dimension: int = 1536,
    chunk_algo_version: str = "4",
):
    local_base_path = os.path.abspath(
        os.environ.get("STORAGE_PREFIX", "cache/embeddings")
    )
    remote_base_path = os.environ.get(
        "REMOTE_STORAGE_PREFIX", "gs://edgar_666/edgar-funcs"
    )

    meta = {
        "cik": cik,
        "accession_number": accession_number,
        "model": embedding_model,
        "dimension": embedding_dimension,
        "chunk_algo_version": chunk_algo_version,
        "storage_base_path": local_base_path,
    }
    try:
        return TextChunksWithEmbedding.load(**meta)
    except ValueError as e:
        if "Cannot load chunk" in str(e):
            # load from remote storage then save locally
            try:
                meta["storage_base_path"] = remote_base_path
                obj = TextChunksWithEmbedding.load(**meta)
                obj.save(storage_base_path=local_base_path)
                return obj
            except ValueError:
                pass

    return None


if __name__ == "__main__":
    obj = load_pickle(cik="1927972", accession_number="0001193125-04-182006")
    assert obj and obj.is_ready()
