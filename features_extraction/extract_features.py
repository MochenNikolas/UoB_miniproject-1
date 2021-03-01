import pandas as pd
import numpy as np
from c_features import lob, lobs
from tqdm import tqdm
import json
import time

if __name__ == "__main__":
    
    with open('/Users/charleshjpearce/Desktop/UoB/UoB_miniproject/data/TstB02_2022-01-04LOBs.json') as json_file:
        j_son = json.load(json_file)
    
    # Define featuers for matrix, no k prev lobs
    features = ['time','microprice','total_quantity_all_quotes','average_midprice_financial_duration']
    k = 10
    # Init feature matrix
    feature_matrix = np.zeros((len(j_son), len(features)))
    lob_list = []
    tik = time.time()
    
    print('Creating LOBjects')
    for _, x in enumerate(tqdm(j_son)):
        lob_list.append(lob(x))
    
    print('Creating grouped lobs and feature matrix')
    for i, this_lob in enumerate(tqdm(lob_list)):
        # Get groups of json given k
        if i >= k-1:
            group_lobs = lobs(lob_list[(i-(k-1)):(i+1)])
        else:
            group_lobs = lobs(lob_list[:i+1])
        
        # Calculate vals, this could be done in parallel
        feature_row = []
        feature_matrix[i][0] = this_lob.time
        feature_matrix[i][1] = this_lob.microprice()
        feature_matrix[i][2] = this_lob.total_quantity_all_quotes()
        feature_matrix[i][3] = group_lobs.average_midprice_financial_duration()
        
    tok = time.time()
    print(f'time taken for processing {tok-tik}')

    # Add to df, print head
    df = pd.DataFrame(feature_matrix,columns=features).dropna(axis=0)
    print(df.head())
    df.to_csv('day_test.csv', index=False)
