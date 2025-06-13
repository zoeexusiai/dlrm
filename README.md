# dlrm
dlrm development code

my summer research

Task 1
Step 1  The occurrence frequency of classification features in the statistical data set


dataset：kaggle_challenge_dataset (small, about 12gb, including train.txt and test.txt) or criteo_dataset (large, about 1tb, only process the first 3 days data)



criteo_dataset format:
Full description:

This dataset contains 24 files, each one corresponding to one day of data.

Dataset construction:
The training dataset consists of a portion of Criteo’s traffic over a period
of 24 days. Each row corresponds to a display ad served by Criteo and the first
column is indicates whether this ad has been clicked or not.
The positive (clicked) and negatives (non-clicked) examples have both been
subsampled (but at different rates) in order to reduce the dataset size.

There are 13 features taking integer values (mostly count features) and 26
categorical features. The values of the categorical features have been hashed
onto 32 bits for anonymization purposes.
The semantic of these features is undisclosed. Some features may have missing values.

The rows are chronologically ordered.

Format:
The columns are tab separated with the following schema:
<label> <integer feature 1> … <integer feature 13> <categorical feature 1> … <categorical feature 26>

When a value is missing, the field is just empty.

Difference with the Kaggle challenge dataset:

– The dataset is not over the same time period;
– The subsampling ratios are different;
– The ordering of the features is not the same and the computation of some of them has changed;
– The hash function for categorical features is different.



kaggle_challenge_dataset format:
Full description:

This dataset contains 2 files:
  train.txt
  test.txt
corresponding to the training and test parts of the data. 

====================================================

Dataset construction:

The training dataset consists of a portion of Criteo's traffic over a period
of 7 days. Each row corresponds to a display ad served by Criteo and the first
column is indicates whether this ad has been clicked or not.
The positive (clicked) and negatives (non-clicked) examples have both been
subsampled (but at different rates) in order to reduce the dataset size.

There are 13 features taking integer values (mostly count features) and 26
categorical features. The values of the categorical features have been hashed
onto 32 bits for anonymization purposes. 
The semantic of these features is undisclosed. Some features may have missing values.

The rows are chronologically ordered.

The test set is computed in the same way as the training set but it 
corresponds to events on the day following the training period. 
The first column (label) has been removed.

====================================================

Format:

The columns are tab separeted with the following schema:
<label> <integer feature 1> ... <integer feature 13> <categorical feature 1> ... <categorical feature 26>

When a value is missing, the field is just empty.
There is no label field in the test set.




Code:

step1_train_v.py is for kaggle_challenge_dataset's train.txt, step1_test_v.py is for kaggle_challenge_dataset's test.txt, step1.py is for criteo_dataset


How to use:

two argument: --features <feature number> (to ensure the features you want to count you should use "," to split every feature number, or use "-" to specify feature range)
              e.g --features 1,4,7 or --features 1-11 or --features 1,3-7,11

              --output <path of output .csv file> (default filename: feature_frequencies.csv)

use example: python step1_test_v.py kaggle_dataset/test.txt --features 1-26 --output kaggle_testdata_C1-26.csv


