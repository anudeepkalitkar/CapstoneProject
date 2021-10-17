from mongoRetreive import retriveData
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer, StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.classification import RandomForestClassifier
import pickle

sc = SparkContext('local')
spark = SparkSession(sc)

df = retriveData()
train_df = spark.createDataFrame(df)
print(train_df.columns)

regexTokenizer = RegexTokenizer(inputCol="summary", outputCol="words", pattern="\\W")
stoppingWords = ["http","https","amp","rt","t","c","the"] 
stoppingWordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(stoppingWords)
countVectors = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=10000, minDF=5)
stringIndexing = StringIndexer(inputCol = "topic", outputCol = "label")

pipeline = Pipeline(stages=[regexTokenizer, stoppingWordsRemover, countVectors, stringIndexing])
pipelineFit = pipeline.fit(train_df)
dataSet = pipelineFit.transform(train_df)
(trainingData, testData) = dataSet.randomSplit([0.7, 0.3], seed = 100)

logisticRegression = LogisticRegression(maxIter=15, regParam=0.3, elasticNetParam=0)
LRModel = logisticRegression.fit(trainingData)
LRPredictions = LRModel.transform(testData)
LRPredictions.filter(LRPredictions['prediction'] == 0) \
    .select("summary","topic","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30)

evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
print(evaluator.evaluate(LRPredictions))
pickle.dump(LRModel, open('LRModel.pkl','w'))

# randomForest = RandomForestClassifier(labelCol="label",featuresCol="features", numTrees = 100, maxDepth = 4, maxBins = 32)
# RFModel = randomForest.fit(trainingData)
# RFPredictions = RFModel.transform(testData)
# RFPredictions.filter(RFPredictions['prediction'] == 0) \
#     .select("summary","topic","probability","label","prediction") \
#     .orderBy("probability", ascending=False) \
#     .show(n = 10, truncate = 30)
# print(evaluator.evaluate(RFPredictions))


