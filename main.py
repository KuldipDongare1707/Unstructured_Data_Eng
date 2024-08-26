from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace
from config.config import configuration
from pyspark.sql.types import StructType, StructField,StringType, DoubleType, DateType
from udf_utils import *



def define_udfs():
    return {
        'extract_file_name_udf': udf(extract_file_name, StringType()),
        'extract_position_udf': udf(extract_position, StringType()),
        'extract_salary_udf': udf(extract_salary, StructType([
            StructField('salary_start',DoubleType(), True),
            StructField('salary_end',DoubleType(), True)
            ])),
        'extract_date_udf': udf(extract_start_date, DateType()),
        'extract_enddate_udf': udf(extract_end_date, DateType()),
        'extract_classcode_udf': udf(extract_class_code, StringType()),
        'extract_requirements_udf': udf(extract_requirements, StringType()),
        'extract_notes_udf': udf(extract_notes, StringType()),
        'extract_duties_udf': udf(extract_duties, StringType()),
        'extract_selection_udf': udf(extract_selection, StringType()),
        'extract_experience_length_udf': udf(extract_experience_length, StringType()),
        'extract_education_length_udf': udf(extract_eduation_length, StringType()),
        'extract_appication_location_udf': udf(extract_appication_location, StringType()),


    }
if __name__ == "__main__":
    spark =(SparkSession.builder.appName('AWS_Spark_Unstructured_Data')
            #.config('spark.jars.packages',
             #       'org.apache.hadoop:hadoop-aws:3.3.1,'
              #      'com.amazonaws:aws-java-sdk:1.11.469')
                .config('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
                .config('spark.hadoop.fs.s3a.access.key',configuration.get('AWS_ACCESS_KEY') )
                .config('spark.hadoop.fs.s3a.secret.key',configuration.get('AWS_SECRET_KEY'))
                .config('spark.hadoop.fs.s3a.aws.credentials.provider',
                        'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
                .getOrCreate()

                    )
    
    text_input_dir = 'file:///Users/kuldeep/Unstructured_Data_Eng/input/input_text'
    json_input_dir = 'file:///Users/kuldeep/Unstructured_Data_Eng/input/input_json'
    csv_input_dir = 'file:///Users/kuldeep/Unstructured_Data_Eng/input/input_csv'
    pdf_input_dir = 'file:///Users/kuldeep/Unstructured_Data_Eng/input/input_pdf'
    video_input_dir = 'file:///Users/kuldeep/Unstructured_Data_Eng/input/input_video'
    img_input_dir = 'file:///Users/kuldeep/Unstructured_Data_Eng/input/input_img'

    data_schema = StructType([
        StructField('file_name', StringType(), True),
        StructField('position', StringType(), True),
        StructField('classcode', StringType(), True),
        StructField('salary_start', DoubleType(), True),
        StructField('salary_end', DoubleType(), True),
        StructField('start_date', DateType(), True),
        StructField('end_date', DateType(), True),
        StructField('req', StringType(), True),
        StructField('notes', StringType(), True),
        StructField('duties', StringType(), True),
        StructField('selection', StringType(), True),
        StructField('exp_type', StringType(), True),
        StructField('education_length', StringType(), True),
        StructField('school_type', StringType(), True),
        StructField('application_location', StringType(), True),
    ])

    udf = define_udfs()

    job_bulletine_df = (spark.readStream
                        .format('text')
                        .option('wholetext', 'true')
                        .load(text_input_dir)
                        )
    job_bulletins_df = job_bulletine_df.withColumn('file_name',
                                                   regexp_replace(udfs['extract_file_name_udf']('value'),'\r',' '))
    job_bulletins_df = job_bulletine_df.withColumn('value', regexp_replace('value',r'\n',''))
    job_bulletins_df = job_bulletine_df.withColumn('position', 
                                                   regexp_replace(udfs['extract_position_udf']('value'),r'\r',' '))
    job_bulletine_df = job_bulletine_df.withColumn('salary_start', 
                                                   udfs['extract_salary_udf']('value').getField('salary_start'))
    job_bulletine_df = job_bulletine_df.withColumn('salary_end', 
                                                   udfs['extract_salary_udf']('value').getField('salary_start'))
    job_bulletins_df = job_bulletine_df.withColumn('start_date', udfs['extract_date_udf']('value'))
    job_bulletins_df = job_bulletine_df.withColumn('enddate', udfs['extract_enddate_udf']('value'))
    
    j_df = job_bulletine_df.select('file_name', 'position', 'start_date', 'end_date','salary_start', 'salary_end')

    query = (job_bulletine_df
             .writeStream
             .output('append')
             .format('console')
             .option('truncate', False)
             .start()
             )
    
    query.awaitTermination()