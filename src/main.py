from src.retriever import retrieve
from src.generator import generate_answer
from src.utils import print_boxed

def main():
    print("\n🔎 GDPR RAG (Terminal)")
    print("Type 'exit' to quit.\n")

    while True:
        q = input("Ask a GDPR question: ").strip()
        if q.lower() in {"exit", "quit"}:
            print("👋 Bye!")
            break

        print("\nRetrieving relevant context...")
        pairs = retrieve(q)
        if not pairs:
            print_boxed("I couldn't find relevant passages in the indexed GDPR text.")
            continue

        # Show which titles we matched (first few)
        print("Matched sources:")
        for _, meta in pairs[:5]:
            t = meta.get("title", "Untitled")
            nid = meta.get("node_id", "")
            print(f" - {t}  [{nid}]")

        context_chunks = [doc for doc, _ in pairs]
        print("\nGenerating answer...\n")
        answer = generate_answer(context_chunks, q)
        print_boxed(answer)

if __name__ == "__main__":
    main()
