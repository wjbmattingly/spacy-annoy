import spacy
import annoy


class SpacyAnnoy:
    def __init__(self, nlp, disable=[]):
        self.nlp_model = nlp
        self.disable = disable
        self.load_model()
    
    def load_model(self):
        """
        Loads the specified Spacy model. If the model is not available locally,
        it attempts to download and then load it.
        """
        try:
            self.nlp = spacy.load(self.nlp_model, disable=self.disable)
        except OSError:
            print(f"Downloading Spacy model '{self.nlp_model}'...")
            spacy.cli.download(self.nlp_model)
            self.nlp = spacy.load(self.nlp_model, disable=self.disable)

    def load_docs(self, texts):
        """
        Let's a user load text or texts into the pipeline.
        """
        self.docs = list(self.nlp.pipe(texts))
        self.chunk_docs()

    def chunk_docs(self, index_style="sent", context_window=3, overlap=1):
        """
        Chunks loaded docs based on the specified window size and overlap.
        Stores token indices for each window span in the original document.
        """
        self.index_style = index_style
        self.context_window = context_window
        self.overlap = overlap
        self.windows = []

        for doc_idx, doc in enumerate(self.docs):
            if self.index_style == "sent":
                sentences = list(doc.sents)
                i = 0
                while i < len(sentences):
                    start_sent = sentences[i]
                    end_sent = sentences[min(i + self.context_window - 1, len(sentences) - 1)]

                    # Using start of the first sentence and end of the last sentence for the window
                    start_idx = start_sent.start
                    end_idx = end_sent.end

                    self.windows.append((doc, start_idx, end_idx))

                    i += max(1, self.context_window - self.overlap)
                    if end_idx == doc[-1].idx:  # Checking if this is the last window
                        break


    def build_index(self, n_trees=10, metric="euclidean", distance=True):

        self.n_trees = n_trees
        self.metric = metric
        self.distance = distance
        """
        Builds the Annoy index using the chunked text data. Each item in the index
        is associated with its original document and sentence indices.
        """
        self.annoy_index = annoy.AnnoyIndex(len(self.nlp("test").vector), self.metric)

        for window_idx, (window, doc_idx, sent_idx) in enumerate(self.windows):
            window_vector = sum([sent.vector for sent in window]) / len(window)
            self.annoy_index.add_item(window_idx, window_vector)

        self.annoy_index.build(self.n_trees)

    def query_index(self, text, depth, verbose=True):
        """
        Queries the built Annoy index and returns results as references to the
        original documents' spans.
        """
        query_vector = self.nlp(text).vector
        annoy_indices = self.annoy_index.get_nns_by_vector(query_vector, depth, include_distances=self.distance)

        res = []
        for annoy_idx, distance in zip(*annoy_indices):
            doc, start_idx, end_idx = self.windows[annoy_idx]
            span = doc[start_idx:end_idx]
            res.append((span, annoy_idx, distance))

        if verbose:
            # self.pretty_print(res)
            pass

        return res

    def pretty_print(self, res):
        """
        Pretty prints the results from querying the Annoy index.
        For each result, it displays the concatenated text of the window as a Spacy Doc,
        its index in the Annoy index, and the distance from the query.
        """
        for window_doc, annoy_idx, distance in res:
            window_text = window_doc.text  # Using the text of the Spacy Doc
            print(f"Text: {window_text}\nIndex: {annoy_idx}, Distance: {distance}")
