from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "sentence-transformers/all-mpnet-base-v2"

REFERENCE = (
    "McGill University is an English-language public research university in Montreal, "
    "Quebec, Canada. Founded in 1821 by royal charter, the university bears the name "
    "of James McGill, a Scottish merchant, whose bequest in 1813 established the "
    "University of McGill College."
)

EXAMPLES = {
    "Example 1": (
        "The University of Toronto is a public research university in Toronto, Ontario, Canada "
        "located on the grounds that surround Queen's Park. It was founded by royal charter "
        "in 1827 as King's College, the first institution of higher learning in the colony of Upper Canada."
    ),
    "Example 2": (
        "Education in Canada is for the most part provided publicly, funded and overseen by"
        "federal, provincial, and local governments. Education is within provincial jurisdiction "
        "and the curriculum is overseen by the province rather than a national ministry."
    ),
    "Example 3": (
        "The mitochondrion is a double-membrane-bound organelle found in most eukaryotic organisms. "
        "Some cells in some multicellular organisms may, however, lack mitochondria. "
        "The most prominent roles of mitochondria are to produce the energy currency of the cell, ATP."
    ),
}


def main() -> int:
    model = SentenceTransformer(DEFAULT_MODEL)
    ref_embedding = model.encode(REFERENCE, normalize_embeddings=True)

    print(f"Model: {DEFAULT_MODEL}")
    print("Reference-only similarity scores:")

    for name, text in EXAMPLES.items():
        example_embedding = model.encode(text, normalize_embeddings=True)
        similarity = float(ref_embedding @ example_embedding)
        print(f"- {name}: {similarity:.4f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
