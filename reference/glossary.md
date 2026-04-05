# Glossary

Twenty-five terms you will encounter when working with RAG pipelines, vector
search, and large language models. Each definition is one sentence, followed by
a concrete analogy.

---

**Chunk** — A short segment of text (typically 200-1000 characters) created by
splitting a larger document so it can be embedded and searched independently.
*Analogy: a single index card in a recipe box -- small enough to find quickly,
but containing one complete idea.*

**Chunking** — The process of splitting a long document into smaller, overlapping
pieces that each fit within the embedding model's input size. *Analogy: cutting a
long roll of wrapping paper into sheets -- you need pieces small enough to work
with, but you don't want to cut mid-sentence.*

**ChromaDB** — An open-source vector database (a storage system optimized for
lists of numbers) that runs locally with no server setup and stores data on disk.
*Analogy: a SQLite database, but for vectors instead of rows and columns.*

**Context Window** — The maximum amount of text a language model can read and
generate in a single conversation, measured in tokens. *Analogy: the size of
the model's desk -- everything it needs to read and write must fit on it at once.*

**Cosine Similarity** — A mathematical measure of how similar two vectors
(lists of numbers) are, ranging from -1 (opposite) to 1 (identical). *Analogy:
comparing the direction two arrows point -- arrows pointing the same way score
near 1, arrows at right angles score 0.*

**Document** — A single file (PDF, markdown, or text) loaded into the pipeline,
represented as its text content plus metadata like the filename and page number.
*Analogy: a physical folder in a filing cabinet -- it holds the content and has
a label on the tab.*

**Embedding** — A list of numbers (typically 768) that represents the meaning of
a piece of text. *Analogy: GPS coordinates for ideas -- similar meanings get
nearby coordinates.*

**Fine-tuning** — The process of further training an existing model on your own
data so it learns domain-specific patterns and terminology. *Analogy: hiring a
general contractor, then spending a month teaching them the quirks of your
building before they start work.*

**Generation** — The step where a language model produces a natural-language
answer based on a prompt that includes the user's question and retrieved context.
*Analogy: a student writing an essay answer after being given the relevant
textbook pages.*

**Hallucination** — When a language model generates a confident-sounding answer
that is factually wrong or entirely made up. *Analogy: a tour guide who, when
they don't know the answer, invents a plausible-sounding story instead of saying
"I don't know."*

**Inference** — The act of sending input to a trained model and receiving its
output, as opposed to training the model. *Analogy: using a calculator to get an
answer vs. building the calculator in the first place.*

**LLM** — A Large Language Model: a neural network trained on vast amounts of
text that can understand and generate human language. *Analogy: a well-read
research assistant who has read billions of pages but has no memory of your
private documents.*

**Metadata** — Descriptive information attached to a chunk or document, such as
the source filename, page number, or creation date. *Analogy: the label on a
file folder -- it tells you where the contents came from without reading them.*

**Model** — A trained neural network that takes input (text, images, etc.) and
produces output (text, numbers, classifications). *Analogy: a recipe -- it was
"written" during training and "followed" during inference to produce results.*

**Ollama** — A free, open-source tool that lets you download and run large
language models locally on your own computer with a single command. *Analogy:
a personal jukebox for AI models -- you pick the model, it plays locally, no
internet required.*

**Overlap** — The number of characters shared between the end of one chunk and
the beginning of the next, ensuring sentences split across chunks aren't lost.
*Analogy: overlapping tiles on a roof -- the overlap prevents gaps where rain
(or meaning) could slip through.*

**Pipeline** — A sequence of processing steps (load, chunk, embed, store,
retrieve, generate) wired together so data flows from input to output
automatically. *Analogy: a factory assembly line -- each station does one job
and passes the result to the next.*

**Prompt** — The text you send to a language model as input, including
instructions, context, and the user's question. *Analogy: the brief you hand
to a freelancer -- the better the brief, the better the output.*

**Prompt Template** — A reusable string with placeholder variables (like
`{question}` and `{context}`) that gets filled in at runtime to form the final
prompt. *Analogy: a form letter with blanks -- you fill in the name and details
each time, but the structure stays the same.*

**RAG** — Retrieval-Augmented Generation: a technique where you first retrieve
relevant documents from a knowledge base, then feed them to a language model so
it answers grounded in your data. *Analogy: an open-book exam -- the student
(LLM) can look up the answer in the provided material instead of relying solely
on memory.*

**Retrieval** — The step where the system searches the vector database for chunks
whose embeddings are closest to the user's question embedding. *Analogy: a
librarian who reads your question, walks to the right shelf, and pulls the most
relevant pages.*

**Token** — The smallest unit of text a language model processes, roughly
equivalent to three-quarters of a word in English. *Analogy: syllables for
an AI -- the word "understanding" is about four tokens, just as it is about
five syllables.*

**Top-k** — A parameter that controls how many of the most similar chunks are
returned from the vector database for a given query. *Analogy: telling the
librarian "bring me the 5 most relevant pages" instead of the entire shelf.*

**Vector** — An ordered list of numbers (e.g., 768 floats) that represents a
data point in multi-dimensional space. *Analogy: a set of coordinates -- just
as (latitude, longitude) locates a point on Earth, a vector locates a piece
of text in "meaning space."*

**Vector Database** — A storage system designed to save, index, and search
vectors efficiently using similarity measures like cosine similarity. *Analogy:
a library catalogue that organizes books by topic similarity rather than
alphabetically by title.*
