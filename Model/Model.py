from mongoRetreive import retriveData
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer, StringIndexer
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from mlflow.pyspark.ml import autolog
import pickle
autolog(log_models=True, disable=False, exclusive=False, disable_for_unsupported_versions=False, silent=False, log_post_training_metrics=True)
sc = SparkContext('local')
spark = SparkSession(sc)

def getData():
    df = retriveData()
    df.drop('published_date')
    df.drop('link')
    df.drop('media')
    df.drop('title')
    df.drop('clean_url')
    return spark.createDataFrame(df)

def buildPipeline():
    regexTokenizer = RegexTokenizer(inputCol="summary", outputCol="words", pattern="\\W")
    stoppingWords = ["http","https","amp","rt","t","c","the"] 
    stoppingWordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(stoppingWords)
    countVectors = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=10000, minDF=5)
    stringIndexing = StringIndexer(inputCol = "topic", outputCol = "label")
    pipeline = Pipeline(stages=[regexTokenizer, stoppingWordsRemover, countVectors, stringIndexing])
    return pipeline

def trainModel():
    dataFrame = getData()
    pipeline = buildPipeline()
    pipelineFit = pipeline.fit(dataFrame)
    dataSet = pipelineFit.transform(dataFrame)
    (trainingData, testData) = dataSet.randomSplit([0.7, 0.3], seed = 100)
    logisticRegression = LogisticRegression(maxIter=15, regParam=0.3, elasticNetParam=0)
    LRModel = logisticRegression.fit(trainingData)
    evaluate(LRModel, testData)
    try:
        pickle.dump(LRModel, open("LRModel.pkl", "wb"))
    except:
        pass
    return LRModel, trainingData, testData

def evaluate(LRModel, testData):
    LRPredictions = LRModel.transform(testData)
    LRPredictions.filter(LRPredictions['prediction'] == 0) \
    .select("summary","topic","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30)

    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
    print(evaluator.evaluate(LRPredictions))

def predictTopic(query_data, Model):
    x = list(query_data.dict().values())
    prediction = Model.predict([x])
    return prediction

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