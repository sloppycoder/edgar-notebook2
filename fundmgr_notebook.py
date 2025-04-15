import marimo

__generated_with = "0.12.8"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    from utils import find_filing, load_pickle
    mo.md("""Initialization""")
    return find_filing, load_pickle, mo


@app.cell
def _(mo):
    accession_number_input = mo.ui.text(placeholder="enter accession number")
    mo.md(f"""
    {accession_number_input}
    """)
    return (accession_number_input,)


@app.cell(hide_code=True)
def _(accession_number_input, find_filing, load_pickle, mo):
    from edgar_funcs.rag.extract.fundmgr import _find_relevant_text
    filing = find_filing(accession_number_input.value)
    _selected_chunks = []
    if filing:
        queries = load_pickle(cik="0", accession_number="fundmgr_ownership_queries", chunk_algo_version="0")
        content = load_pickle(cik=filing["cik"],accession_number=filing["accession_number"])
        print(f"loaded filing with {len(content.texts)} chunks")
        _selected_chunks,_ = _find_relevant_text(queries, content, "top5")

    selected_chunk_dropdown_2 = mo.ui.dropdown(_selected_chunks)
    mo.md(f"""
    {selected_chunk_dropdown_2}
    """)
    return content, filing, queries, selected_chunk_dropdown_2


@app.cell(hide_code=True)
def _(content, mo, selected_chunk_dropdown_2):

    _chunk_text = ""
    if selected_chunk_dropdown_2.value:
        _chunk_text = content.texts[selected_chunk_dropdown_2.value]
        _chunk_text.replace("\n\n", "\n")
    mo.md(f"""
    {mo.ui.text_area(_chunk_text, rows=30)}
    """)
    return


if __name__ == "__main__":
    app.run()
