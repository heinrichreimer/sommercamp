
# Hier importieren wir die benötigten Softwarebibliotheken.
from os.path import abspath, exists
from sys import argv
from streamlit import (text_input, header, title, subheader, 
    container, markdown, link_button, divider, set_page_config)
from pyterrier import started, init
# Die PyTerrier-Bibliothek muss zuerst gestartet werden,
# um alle seine Bestandteile importieren zu können.
if not started():
    init()
from pyterrier import IndexFactory
from pyterrier.batchretrieve import BatchRetrieve
from pyterrier.text import get_text


def app(index_dir):
    set_page_config(
        page_title="Braunschweig Suchmaschine",
        layout="centered",
    )

    title("Braunschweig Suchmaschine")
    markdown("Willkommen bei der Suchmaschine für die Stadt Braunschweig.")

    query = text_input(
        label="Suche",
        placeholder="Geben Sie hier Ihren Suchbegriff ein.",
        value="test",
    )

    if query == "":
        markdown("Bitte geben Sie einen Suchbegriff ein.")
        return

    index = IndexFactory.of(abspath(index_dir))

    searcher = BatchRetrieve(
        index,
        wmodel="BM25",
        num_results=10,
    )
    text_getter = get_text(
        index, metadata=["url", "title", "text"]
    )

    pipeline = searcher >> text_getter

    results = pipeline.search(query)

    divider()
    header("Suchergebnisse")

    if len(results) == 0:
        markdown("Keine Ergebnisse gefunden.")
        return

    markdown(f"Es wurden {len(results)} Ergebnisse gefunden.")

    for _, row in results.iterrows():
        with container(border=True):
            subheader(row["title"])

            text = row["text"]
            text = text[:500]
            text = text.replace("\n", " ")
            markdown(text)

            link_button("Öffnen", row["url"])


def main():
    index_dir = argv[1]

    if not exists(index_dir):
        exit(1)

    app(index_dir)


if __name__ == "__main__":
    main()
