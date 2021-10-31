from mongoInjection import InjectToMongodb
from kafka import KafkaConsumer
from json import loads
consumer = KafkaConsumer('newsarticles', bootstrap_servers=['kafka:29092'], auto_offset_reset='earliest', enable_auto_commit=True, group_id='my-group', value_deserializer=lambda x: loads(x.decode('utf-8')))
for message in consumer:
    InjectToMongodb(message.value)
    # print(len(message.value), type(message.value))