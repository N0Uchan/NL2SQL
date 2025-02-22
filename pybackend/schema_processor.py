from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
import numpy as np
import json

class SchemaProcessor:
    def __init__(self, schema_json):
        """
        Initialize with a JSON schema and process it.
        """
        self.schema_json = schema_json
        self.tables = self._parse_schema()
        self.bm25_index = self._create_bm25_index()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.table_embeddings = self._generate_table_embeddings()

    def _parse_schema(self):
        """
        Extract tables and columns into a structured format.
        """
        tables = []
        for table in self.schema_json['tables']:
            table_info = {
                'name': table['name'],
                'columns': [col['name'] for col in table['columns']],
                'foreign_keys': table.get('foreign_keys', [])
            }
            tables.append(table_info)
        return tables

    def _create_bm25_index(self):
        """
        Create a BM25 index for fast keyword-based search.
        """
        corpus = [
            ' '.join([table['name']] + table['columns'])
            for table in self.tables
        ]
        tokenized_corpus = [doc.split() for doc in corpus]
        return BM25Okapi(tokenized_corpus)

    def _generate_table_embeddings(self):
        """
        Generate embeddings for all tables.
        """
        corpus = [
            ' '.join([table['name']] + table['columns'])
            for table in self.tables
        ]
        return self.embedding_model.encode(corpus)

    def save_processed_schema(self, file_path):
        """
        Save the processed schema (BM25 index, embeddings, etc.) to a file.
        """
        processed_data = {
            'tables': self.tables,
            'bm25_index': {
                'corpus': self.bm25_index.corpus,
                'idf': self.bm25_index.idf,
                'doc_len': self.bm25_index.doc_len,
                'avgdl': self.bm25_index.avgdl
            },
            'table_embeddings': self.table_embeddings.tolist()
        }
        with open(file_path, 'w') as f:
            json.dump(processed_data, f)

    @classmethod
    def load_processed_schema(cls, file_path):
        """
        Load the processed schema from a file.
        """
        with open(file_path) as f:
            processed_data = json.load(f)
        
        processor = cls.__new__(cls)
        processor.tables = processed_data['tables']
        processor.bm25_index = BM25Okapi(
            processed_data['bm25_index']['corpus'],
            idf=processed_data['bm25_index']['idf'],
            doc_len=processed_data['bm25_index']['doc_len'],
            avgdl=processed_data['bm25_index']['avgdl']
        )
        processor.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        processor.table_embeddings = np.array(processed_data['table_embeddings'])
        return processor