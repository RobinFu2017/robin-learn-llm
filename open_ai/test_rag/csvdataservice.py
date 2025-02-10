

from openai import OpenAI
from scipy import spatial
from pdfservice import pdf_to_embeddings
import ast
import pandas as pd

client = OpenAI()

CSV_FILE_PATH = './open-ai/test_rag/files/my_reg_test_data.csv'
PDF_FILE_PATH = './open-ai/test_rag/files/三体.pdf'

class CsvDataService():

    def __init__(self, model: str = "text-embedding-ada-002") -> None:
        self.reg_data_df : pd.DataFrame = None
        self.embedding_model : str = model
        self.load_data_from_pdf()
    

    def load_data_from_pdf(self, csv_path : str = CSV_FILE_PATH, pdf_path : str = PDF_FILE_PATH):
        try:
            print('load data from csv')
            df = pd.read_csv(csv_path)
            df['vector'] = df['vector'].apply(ast.literal_eval)
            print('load data success')
        except Exception as e:
            print('load data failed，try to load from pdf and embedding')
            embeddings = pdf_to_embeddings(pdf_path = pdf_path)
            print('embedding success. start to save to csv file')
            df = pd.DataFrame(embeddings)
            df.to_csv(csv_path, index=False)
            print('save csv success')
        print(df)
        self.reg_data_df = df

    def search_fact(self,
                     user_query: str,
                     vector_field: str = "vector",
                     return_fields: list = ["text", "vector_score"],
                     k: int = 5,
                     print_results: bool = False
                     ):
        # 调用open-ai，获得查询字符串的嵌入向量
        embedded_query_resopnse = client.embeddings.create(input=user_query,  model = self.embedding_model)
        embedded_query = embedded_query_resopnse.data[0].embedding
        # 定义向量的距离判定方法，采用余弦相似度算法
        # 余弦相似度（Cosine similarity）是一种衡量两个非零向量在多维空间中的相似度的方法。
        # 它通过测量这两个向量的夹角的余弦值来计算相似度。其范围从-1到1，
        # 余弦值为1时表示两个向量方向完全相同，为0时表示两个向量正交，方向无关，为-1时表示两个向量方向完全相反。
        # relatedness_fn = lambda x, y: 1 - spatial.distance.cosine(x, y)

        relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y)
        strings_and_relatednesses = [
            (row["text"], relatedness_fn(embedded_query, row["vector"])) for i, row in self.reg_data_df.iterrows()
        ]
        strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
        strings, relatednesses = zip(*strings_and_relatednesses)
        if(print_results):
            print(f'{strings_and_relatednesses[:5]},')
        return strings[:5]