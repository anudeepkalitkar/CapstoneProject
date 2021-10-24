from mongoRetreive import retriveData
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer, StringIndexer
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from mlflow.pyspark.ml import autolog
import pandas as pd
import numpy as np
autolog(log_models=True, disable=False, exclusive=False, disable_for_unsupported_versions=False, silent=False, log_post_training_metrics=True)
sc = SparkContext('local')
spark = SparkSession(sc)

def getData():
    df = retriveData()
    # df.drop('published_date')
    # df.drop('link')
    # df.drop('media')
    # df.drop('title')
    # df.drop('clean_url')d
    return spark.createDataFrame(df)

def dataPipeline():
    regexTokenizer = RegexTokenizer(inputCol="summary", outputCol="words", pattern="\\W")
    stoppingWords = ["http","https","amp","rt","t","c","the"] 
    stoppingWordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(stoppingWords)
    countVectors = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=10000, minDF=0)
    stringIndexing = StringIndexer(inputCol = "topic", outputCol = "label")
    pipeline = Pipeline(stages=[regexTokenizer, stoppingWordsRemover, countVectors, stringIndexing])
    return pipeline

def trainModel():
    dataFrame = getData()
    pipeline = dataPipeline()
    pipelineFit = pipeline.fit(dataFrame)
    dataSet = pipelineFit.transform(dataFrame)
    mappedLabels = mapLabelandTopics(dataSet)
    (trainingData, testData) = dataSet.randomSplit([0.7, 0.3], seed = 100)
    logisticRegression = LogisticRegression(featuresCol = 'features', labelCol = 'label', maxIter=15, regParam=0.3, elasticNetParam=0)
    LRModel = logisticRegression.fit(trainingData)
    evaluate(LRModel, testData)
    return LRModel, pipelineFit, mappedLabels

def evaluate(LRModel, testData):
    LRPredictions = LRModel.transform(testData)
    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
    print(evaluator.evaluate(LRPredictions))
    
def predictTopic(Model, pipelineFit, params):
    params = spark.createDataFrame(params)
    testData = pipelineFit.transform(params)
    LRPredictions = Model.transform(testData)
    return LRPredictions.collect()[-1]['prediction']

def validate(LRModel, trainingData, testData):
    paramGrid = (ParamGridBuilder()
             .addGrid(LRModel.regParam, [0.1, 0.3, 0.5]) # regularization parameter
             .addGrid(LRModel.elasticNetParam, [0.0, 0.1, 0.2]) # Elastic Net Parameter (Ridge = 0)
             .build())

    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
    cv = CrossValidator(estimator=LRModel, \
                        estimatorParamMaps=paramGrid, \
                        evaluator=evaluator, \
                        numFolds=5)
    cvModel = cv.fit(trainingData)
    predictions = cvModel.transform(testData)
    evaluator.evaluate(predictions)

def mapLabelandTopics(dataSet):
    labels = []
    Mappedlabels = {}
    for data in dataSet.collect():
        if(data['label'] not in labels):
            labels.append(data['label'])
            Mappedlabels[int(data['label'])]= data['topic']
    return Mappedlabels

# LRModel, pipelineFit, mappedLabels = trainModel()
# data = [["Elon Musk: The THREE questions investors should ask as Tesla CEO prompts SHIB surge",
# "2021-10-08 23:09:15",
# "https://www.express.co.uk/finance/city/1503278/Elon-musk-dogecoin-shiba-inu-coin-price-Tesla-CEO-evg",
# "express.co.uk",
# "https://cdn.images.express.co.uk/img/dynamic/22/750x445/1503278.jpg","news"]]
# DataFields=["title","published_date","link","clean_url","summary","media","topic"]
# data = np.array(data)
# data = pd.DataFrame(data = data,columns=DataFields)
# prediction = predictTopic(LRModel,pipelineFit,data)
# print(mappedLabels[int(prediction)])
