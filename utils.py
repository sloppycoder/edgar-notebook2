import os
from dotenv import load_dotenv
from edgar_funcs.rag.vectorize import TextChunksWithEmbedding
from edgar_funcs.edgar import load_filing_catalog

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


def find_filing(accession_number: str):
    df_filings = load_filing_catalog("2000-01-01", "2024-12-31")
    df_filtered = df_filings[df_filings["accession_number"] == accession_number]
    if len(df_filtered) > 0:
        return df_filtered.to_dict(orient="records")[0]
    return None
