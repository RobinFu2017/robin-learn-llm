


from intentservice import IntentService
from responseservice import ResponseService
from redisdataservice import RedisDataService
from csvdataservice import CsvDataService
from pdfservice import pdf_to_embeddings


# Example pdf
pdf = './open-ai/test_rag/files/三体.pdf'

DATA_USE_REDIS = 'data_use_redis'
DATA_USE_CSV = 'data_use_csv'
redis_data_service: RedisDataService = None
csv_data_service: CsvDataService = None
intent_service: IntentService = None
response_service: ResponseService = None

# 初始化数据
def initRedisData():
    ds = RedisDataService()
    # 清空旧的embedding数据
    ds.drop_data()

    # 从pdf里读取数据，处理embedding, 写入redis
    ds.load_data_from_pdf(pdf)


def answer_by_rag(question : str, use_data_type : str = DATA_USE_REDIS):
    global redis_data_service
    global csv_data_service
    global intent_service
    global response_service
    if(redis_data_service is None):
        redis_data_service = RedisDataService()        
        csv_data_service = CsvDataService()
        intent_service = IntentService()
        response_service = ResponseService()

    # 调用模型，把问题抽象成关键词
    intents = intent_service.get_intent(question)
    print(f"intents is:{intents}")

    # 基于关键词，到向量数据库里检索相关资料
    if(use_data_type == DATA_USE_REDIS):
        facts = redis_data_service.search_fact(user_query = intents, print_results = True)
    elif(use_data_type == DATA_USE_CSV):
        facts = csv_data_service.search_fact(user_query = intents, print_results = True)


    # 把检索到的资料放入上下文，并提问
    answer = response_service.generate_response(facts, question)
    print(f'\nthe answer is:{answer}')

# 调试用的
# pdf_to_embeddings(pdf)


# initRedisData()

# 提问
answer_by_rag(question = '红色联合是什么?', use_data_type = DATA_USE_CSV)

answer_by_rag(question = '叶文洁是什么人?', use_data_type = DATA_USE_CSV)

