# Wafer-Fault-Detection

### Problem - 
Semiconductor manufacturing is a highly complex process that consists of hundreds of steps. Any fault leads to lower yields. The earlier a fault is identified, the better it is to avoid an increase in manufacturing cost. The state-of-the-art manufacturing equipment is equipped with sensors for real-time manufacturing process monitoring. The data from the sensors provides an opportunity to detect any fault.

### Dataset Information - 
The data consists of 2 files the dataset file SECOM consisting of 1567 examples each with 591 features (data from various sensors) a 1567 x 591 matrix and a labels file containing the classifications and date time stamp for each example.

https://archive.ics.uci.edu/ml/datasets/SECOM

I have divided the dataset into various training batch files which will be used for training the model.
Apart from training file, I have also created "schema" file that contains all the information about training batch files such as - 
Name of the files, Length of Date value in FileName, Length of Time value in FileName, Number of Columns, Name of the Columns, and their datatype.

### Architecture - 
Application flow during training - 
![image](https://user-images.githubusercontent.com/43309301/218892593-a34567a3-ebad-439c-8237-b79722f3d341.png)

Application flow during prediction - 
![image](https://user-images.githubusercontent.com/43309301/218892831-e2f7a0dc-dbb0-4e67-8a1e-2a36b47c07f7.png)

### Data Validation-
In this step, we perform different sets of validation on the given set of training files.  
1.	 Name Validation- We validate the name of the files based on the given name in the schema file. We have created a regex pattern as per the name given in the schema file to use for validation. After validating the pattern in the name, we check for the length of date in the file name as well as the length of time in the file name. If all the values are as per requirement, we move such files to "Good_Data_Folder" else we move such files to "Bad_Data_Folder."

2.	 Number of Columns - We validate the number of columns present in the files, and if it doesn't match with the value given in the schema file, then the file is moved to "Bad_Data_Folder."


3.	 Name of Columns - The name of the columns is validated and should be the same as given in the schema file. If not, then the file is moved to "Bad_Data_Folder".

4.	 The datatype of columns - The datatype of columns is given in the schema file. This is validated when we insert the files into Database. If the datatype is wrong, then the file is moved to "Bad_Data_Folder".


5.	Null values in columns - If any of the columns in a file have all the values as NULL or missing, we discard such a file and move it to "Bad_Data_Folder".

### Insert in Database - 
1) Database Creation and connection - Create a database with the given name passed. If the database is already created, open the connection to the database. 
2) Table creation and insertion in the database - Table with name - "Good_Data", is created in the database for inserting the files in the "Good_Data_Folder" based on given column names and datatype in the schema file. If the table is already present, then the new table is not created and new files are inserted in the already present table as we want training to be done on new as well as old training files.

### Model Training -
1) Data Export from Db - The data in a stored database is exported as a CSV file to be used for model training.
2) Data Preprocessing   
   a) Check for null values in the columns. If present, impute the null values using the KNN imputer.
   
   b) Check if any column has zero standard deviation, remove such columns as they don't give any information during model training.
3) Clustering - KMeans algorithm is used to create clusters in the preprocessed data. The optimum number of clusters is selected by plotting the elbow plot, and for the dynamic selection of the number of clusters, we are using "KneeLocator" function. The idea behind clustering is to implement different algorithms
   To train data in different clusters. The Kmeans model is trained over preprocessed data and the model is saved for further use in prediction.
4) Model Selection - After clusters are created, we find the best model for each cluster. We are using two algorithms, "Random Forest" and "XGBoost". For each cluster, both the algorithms are passed with the best parameters derived from GridSearch. We calculate the AUC scores for both models and select the model with the best score. Similarly, the model is selected for each cluster. All the models for every cluster are saved for use in prediction.

### Prediction - 
KMeans model created during training is loaded, and clusters for the preprocessed prediction data is predicted. Based on the cluster number, the respective model is loaded and is used to predict the data for that cluster.

### How to run - 

1. Clone the repository using the following command - 
```
git clone https://github.com/harsh1399/Flipkart-review-scrapper.git
```

2. Create a virtual environment and install the required libraries -
```
pip install -r requirements.txt
```

3. To run the flask app - 
```
flask --app main run
```

