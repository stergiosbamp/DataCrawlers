import os
import json
import datetime
from kafka import KafkaConsumer
from elastic import ElasticSearchClient
from dotenv import load_dotenv
from constants import *


# AQHub measures pollutants values as strings instead of float
def pollutants_to_int(msg: dict) -> dict:
    for pollutant in ('CO', 'NO2', 'O3', 'PM10', 'PM25', 'SO2'):
        msg[pollutant] = float(msg[pollutant]) if msg[pollutant] is not None else None

    return msg


load_dotenv()

es = ElasticSearchClient(os.getenv('ES_HOST'), os.getenv('ES_PORT'),
                         use_ssl=os.getenv('ES_USE_SSL', False),
                         verify_certs=os.getenv('ES_VERIFY_CERTS', False),
                         http_auth=(os.getenv('ES_USER'), os.getenv('ES_PASSWORD')) if os.getenv('ES_USER') else None,
                         ca_certs=os.getenv('ES_CA_CERTS', None))

geo_point_mapping = es.define_geo_point_mapping()

es.create_index(ELASTICSEARCH_INDEX, geo_point_mapping)

kafka_consumer = KafkaConsumer(KAFKA_TOPIC,
                               bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                               # auto_offset_reset='earliest',
                               security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                               ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                               ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                               ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                               group_id='group_' + KAFKA_TOPIC,
                               value_deserializer=lambda m: json.loads(m.decode('utf8')))

for msg in kafka_consumer:
    # Data are ready to be inserted to ES from producer.

    # Insert documents, with id's Station+Date+Parameter eg. "Malakopi2020-03-18 10:30:02PM10"
    # in order to avoid duplicate records
    doc = msg.value

    time = doc['Date']
    station = doc['station_name']
    parameter = doc['Parameter']
    id = station+time+parameter

    """
    NOTE: 
        There is a bug in AQHub which fetches some duplicates measurements. 
        Until it's fixed it's totally reasonable if the result of insertion in ES
        is "updated". That's what it should do, at first place.
    """
    result = es.insert_doc(doc_=doc, id_=id)
    print(result)
