# Spacy Annoy

SpacyAnnoy is a Python class that integrates Spacy's natural language processing capabilities with Annoy's efficient similarity search to provide a powerful tool for analyzing and querying large text corpora based on semantic similarity.

## Features

- **Text Processing with Spacy**: Leverages Spacy's robust NLP features for text processing.
- **Efficient Similarity Search**: Uses Annoy (Approximate Nearest Neighbors Oh Yeah) for fast search of similar text chunks.
- **Contextual Window Chunking**: Splits text into chunks based on sentence context for more nuanced analysis.
- **Original Context Preservation**: Retains references to the original document spans, enabling access to all original Spacy properties.

## Installation

Before you begin, ensure you have Python installed on your machine. Then, install the required dependencies:

```bash
pip install spacy-annoy
```

## Usage

### Initialization

```python
from SpacyAnnoy import SpacyAnnoy

# Initialize with a Spacy model name
sa = SpacyAnnoy("en_core_web_sm")
```

### Loading and Processing Documents

```python
texts = ["Your text data.", "Another document."]
sa.load_docs(texts)
```

### Building the Index

```python
sa.build_index(n_trees=10, metric="euclidean")
```

### Querying

```python
# Query the index
results = sa.query_index("Query text", depth=5)

# Pretty print results
sa.pretty_print(results)
```

### Accessing Results

```python
# Accessing the Spacy span of the first result
first_result_span = results[0][0]
```