# Improve Your Results

Five tuning knobs to get better answers from your RAG pipeline, each with
a "try this" experiment you can run in under 5 minutes.

## Chunk size

TODO: Explain the trade-off (larger = more context, smaller = more precise).
Experiment: try 200, 500, and 1000 on the same query.

## Chunk overlap

TODO: Explain why overlap matters at boundaries.
Experiment: try 0, 50, and 100 overlap.

## Top-k retrieval

TODO: Explain noise vs. coverage trade-off.
Experiment: try top_k=1, 5, and 15.

## Prompt template

TODO: Show how to modify RAG_PROMPT_TEMPLATE in generator.py.
Experiment: add "Be concise" or "Cite sources" instructions.

## Embedding model

TODO: Compare nomic-embed-text vs. mxbai-embed-large.
Experiment: re-index with a different model and compare results.
