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
        Save the processed schema (tables, embeddings) to a file.
        """
        processed_data = {
            'tables': self.tables,
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
        processor.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        processor.table_embeddings = np.array(processed_data['table_embeddings'])
        return processor
# from rank_bm25 import BM25Okapi
# from sentence_transformers import SentenceTransformer
# import numpy as np
# import json

# class SchemaProcessor:
#     def __init__(self, schema_json):
#         """
#         Initialize with a JSON schema and process it.
#         """
#         self.schema_json = schema_json
#         self.tables = self._parse_schema()
#         self.tokenized_corpus = self._create_tokenized_corpus()
#         self.bm25_index = BM25Okapi(self.tokenized_corpus)
#         self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
#         self.table_embeddings = self._generate_table_embeddings()

#     def _parse_schema(self):
#         """
#         Extract tables and columns into a structured format.
#         """
#         tables = []
#         for table in self.schema_json['tables']:
#             table_info = {
#                 'name': table['name'],
#                 'columns': [col['name'] for col in table['columns']],
#                 'foreign_keys': table.get('foreign_keys', [])
#             }
#             tables.append(table_info)
#         return tables

#     def _create_tokenized_corpus(self):
#         """
#         Create a tokenized corpus for BM25 indexing.
#         """
#         corpus = [
#             ' '.join([table['name']] + table['columns'])
#             for table in self.tables
#         ]
#         return [doc.split() for doc in corpus]

#     def _generate_table_embeddings(self):
#         """
#         Generate embeddings for all tables.
#         """
#         corpus = [
#             ' '.join([table['name']] + table['columns'])
#             for table in self.tables
#         ]
#         return self.embedding_model.encode(corpus)

#     def select_tables(self, query, top_k=5, bm25_candidates=20):
#         """
#         Select the most relevant tables for a given query.
#         """
#         # Step 1: BM25 keyword filtering
#         tokenized_query = query.split()
#         bm25_scores = self.bm25_index.get_scores(tokenized_query)
#         top_bm25_indices = np.argsort(bm25_scores)[-bm25_candidates:]

#         # Step 2: Semantic re-ranking
#         query_embedding = self.embedding_model.encode(query)
#         table_embeddings = self.embedding_model.encode([
#             ' '.join([self.tables[i]['name']] + self.tables[i]['columns'])
#             for i in top_bm25_indices
#         ])

#         similarities = np.dot(query_embedding, table_embeddings.T)
#         final_indices = top_bm25_indices[np.argsort(similarities)[-top_k:]]

#         # Step 3: Foreign key expansion
#         selected_tables = [self.tables[i] for i in final_indices]
#         related_tables = self._get_related_tables(selected_tables)

#         return selected_tables + related_tables

#     def _get_related_tables(self, selected_tables):
#         """
#         Include tables connected via foreign keys.
#         """
#         related = []
#         for table in selected_tables:
#             for fk in table['foreign_keys']:
#                 ref_table = next(
#                     t for t in self.tables if t['name'] == fk['reference_table']
#                 )
#                 if ref_table not in selected_tables + related:
#                     related.append(ref_table)
#         return related

#     def save_processed_schema(self, file_path):
#         """
#         Save the processed schema (tables, tokenized corpus, embeddings) to a file.
#         """
#         processed_data = {
#             'tables': self.tables,
#             'tokenized_corpus': self.tokenized_corpus,
#             'table_embeddings': self.table_embeddings.tolist()
#         }
#         with open(file_path, 'w') as f:
#             json.dump(processed_data, f)

#     @classmethod
#     def load_processed_schema(cls, file_path):
#         """
#         Load the processed schema from a file.
#         """
#         with open(file_path) as f:
#             processed_data = json.load(f)
        
#         processor = cls.__new__(cls)
#         processor.tables = processed_data['tables']
#         processor.tokenized_corpus = processed_data['tokenized_corpus']
#         processor.bm25_index = BM25Okapi(processed_data['tokenized_corpus'])
#         processor.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
#         processor.table_embeddings = np.array(processed_data['table_embeddings'])
#         return processor
