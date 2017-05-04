from pyspark import SparkContext, SparkConf
from pyspark.ml.classification import LogisticRegression
from pyspark.sql import SparkSession
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.util import MLUtils
if __name__ == "__main__":
  def parsePoint(line):
    values = [float(x) for x in line.split(' ')]
    return LabeledPoint(values[0], values[1:])
  conf = SparkConf().setAppName("LG")
  sc = SparkContext(conf=conf)
  data = sc.textFile("hdfs://student83-x1:9000/sample_svm.txt")
  parsedData = data.map(parsePoint)
  MLUtils.saveAsLibSVMFile(
      parsedData, "hdfs://student83-x1:9000/sample_libsvm")
