from pyspark import SparkContext,SparkConf
from pyspark.ml.classification import LogisticRegression
from pyspark.sql import SparkSession
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.util import MLUtils
if __name__ == "__main__":

  spark = SparkSession \
        .builder \
        .appName("MulticlassLogisticRegressionWithElasticNet") \
        .getOrCreate()
  data = spark \
    .read \
    .format("libsvm") \
    .load("hdfs://student83-x1:9000//libsvmData/training_data/part-00000")
  (trainData, testData) = data.randomSplit([0.7, 0.3])
  lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)

  # Fit the model
  lrModel = lr.fit(trainData)
  lrModel.write.overwrite("hdfs://student83-x1:9000/trainedModel/LGModel.model")
  # Print the coefficients and intercept for multinomial logistic regression
  print("Coefficients: \n" + str(lrModel.coefficientMatrix))
  print("Intercept: " + str(lrModel.interceptVector))

  #Print the accuracy of trainedData
  predictions = lrModel.transform(trainData)
  print("first 5 accuracy of trainingData",predictions.show(5))

  #Print the accuracy of testData
  predictions = lrModel.transform(testData)
  print("first 5 accuracy of testData", predictions.show(5))
  # $example off$

  spark.stop()
