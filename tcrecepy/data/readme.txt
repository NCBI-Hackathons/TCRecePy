## Information for team members:

We aim to design a machine learning method to distinguish two types of T cell receptor hypervariable CDR3 sequences. This particular region is of high interest in immunology because it is binding to antigens that are presented on the surface of human cells. This interaction will eventually trigger adaptive immune responses which eliminates the pathogens, such as virus infection, or sometimes cancer cells. 

In order to understand which CDR3 sequences may bind to cancer antigens, we have prioritized 20,000 cancer-specific CDR3s, which may possess distinct biochemical features from the non-cancer CDR3s. Your task is to develop a predictor that is able to distinguish the cancer-specific CDR3s from non-cancer CDR3s. I have provided an amino acid index matrix, which contains 544 features for each of the 20 amino acid. This matrix may help you to convert the amino acid characters into continuous values, which will be much more straightforward to design predictors.

Please train your classifer on the training data, and then test it using the test data. If there is a continuous threshold in your predictor, please report an ROC curve, and the related AUC values. 

Have fun!

Bo
