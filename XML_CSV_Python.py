import boto3
import xml.etree.ElementTree as ET 
import copy
import pandas as pd


def reading_data_from_S3(bucket_name,item_name):

    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name,item_name)
    body = obj.get()['Body'].read()
    return body
    
def parsing_content(data):
    state= ET.fromstring(data)
    content_of_xml=[]
    
    for resident in state:
        resident_info={}
        
        if len(resident)==0:
            Resident_info.append(resident.text)
            
        elif len(resident)>0:
            for item in resident:
                if len(item)==0:
                    resident_info[item.tag]=item.text
                elif len(item)>0:
                    for address in item:
                        resident_info[address.tag]=address.text
                    new_resident_info=resident_info.copy()
                    content_of_xml.append(new_resident_info)
                    
    return content_of_xml
    
def transforming_to_s3_write_csv(content_of_xml):

    pandas_df = pd.DataFrame.from_dict(content_of_xml)
    pandas_df.to_csv('s3://glue-demo-bucket-ekta/write/resident_data.csv', index=False)


def main():
    bucket_name="glue-demo-bucket-ekta"
    item_name= "read/resident_data.XML"
    data = reading_data_from_S3(bucket_name,item_name)
    content_of_xml = parsing_content(data)
    transforming_to_s3_write_csv(content_of_xml)

if __name__ == "__main__": 
  
    # calling main function 
    main()