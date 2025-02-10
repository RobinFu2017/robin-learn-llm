

import re
from openai import OpenAI
from pypdf import PdfReader

client = OpenAI()
def pdf_to_embeddings(pdf_path: str, chunk_length: int = 1000):
    # Read data from pdf file and split it into chunks
    print('start to read pdf')
    reader = PdfReader(pdf_path)
    chunks = []
    page_num = 1
    for page in reader.pages:
        text_page = page.extract_text()
        # 把前面不带句号的换行全部干掉，只保留。\n这样的
        text_segmented = re.sub(r'(?<!\。)\n', '', text_page)
        text_splited = text_segmented.split('\n')
        chunks.extend(text_splited)
        print(f"read page {page_num} done")
        page_num+=1
        if(page_num>=30):
            break
    print(f'pdf read success. there is {page_num} page, {len(chunks)} paragraph')
    # 按照10个一组的步长，拆分数组，调用open-ai的嵌入api。不拆的话太大会卡死
    print("start to call openai's embedding api.")
    result_embedding = []
    for i in range(0, len(chunks), 10):
        slice_of_chunk = chunks[i:i+10]
        response = client.embeddings.create(model='text-embedding-ada-002', input = slice_of_chunk)
        result_embedding.extend([{'id': value.index, 'vector':value.embedding, 'text':slice_of_chunk[value.index]} for value in response.data])
        print(f'process {i} of {len(chunks)} done')
    print('call open-ai embedding done')
    return result_embedding