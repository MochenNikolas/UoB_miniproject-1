#!/bin/bash
nohup python3 features_extraction/extract_features.py --start_index 0 --end_index 10 \
--subpath_s3bucket b_02 --batch_size 100000


