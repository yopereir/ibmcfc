
# coding: utf-8

# In[3]:


# @hidden_cell
# The project token is an authorization token that is used to access project resources like data sources, connections, and used by platform APIs.
from project_lib import Project
project = Project(project_id='bfbd6c91-b53c-4671-9bee-1e6b8a38e6bb', project_access_token='p-c7576e216cb5709accd40e8296a727978829c86d')
pc = project.project_context


# In[21]:



# @hidden_cell
# The following code contains the credentials for a bucket in your IBM Cloud Object Storage.
# You might want to remove those credentials before you share your notebook.
credentials_1 = {
    'BUCKET': 'matthewb',
    'URL': 'https://s3.us.cloud-object-storage.appdomain.cloud',
    'SECRET_KEY': '6953284e134def0db057ec38d35eb11eb96fa9a37b6ab6b0',
    'API_KEY': 'lm6U2ZcNh_bRhHJv_yx6bmmY9jcvPC9jzHLfaHWjzgza{',
    'RESOURCE_INSTANCE_ID': 'crn:v1:bluemix:public:cloud-object-storage:global:a/649ecce0c55043b6906bca8be71345d3:f8862bce-fb51-43cf-9aba-f491477297e9::',
    'ACCESS_KEY': '7f00fbe39f3e48719bcdaac6105d1199'
}


import ibm_boto3
from ibm_botocore.client import Config, ClientError

# Constants for IBM COS values
COS_ENDPOINT = credentials_1['URL'] # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = credentials_1['API_KEY'] # eg "W00YiRnLW4a3fTjMB-oiB-2ySfTrFBIQQWanc--P3byk"
COS_AUTH_ENDPOINT = "https://iam.ng.bluemix.net/oidc/token"
COS_RESOURCE_CRN = credentials_1['RESOURCE_INSTANCE_ID'] # eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003abfb5d29761c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"

# Create resource
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_auth_endpoint=COS_AUTH_ENDPOINT,
    ibm_service_instance_id=COS_RESOURCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)
def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        for file in files:
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))
get_bucket_contents('matthewb')



# In[4]:


health.tail()
health.describe()


# In[7]:


#Features
X = health[['Capacity', 'Medical_staff_present', 'No_of_Backup_Gens', 'Nearest_Hospital_miles', 'Avg_Expiry_of_Meds_in_months']]


# In[8]:


y = health['Food_stored_in_kg ']


# In[9]:


y1 = health['Water_in_l ']


# In[10]:


#Training model
from sklearn.model_selection import train_test_split


# In[11]:


#Training Testing split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 7)


# In[12]:


X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y1, test_size = 0.3, random_state = 7)


# In[13]:


#Model
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
prediction = model.predict(X_test)


# In[14]:


model2 = LinearRegression()
model2.fit(X_train2, y_train2)
prediction2 = model2.predict(X_test2)


# In[15]:


#Evaluation
from sklearn import metrics
import numpy as np
print('Predicted Food Stored', prediction)


# In[21]:


MSE = metrics.mean_squared_error(y_test, prediction)
RMSE = np.sqrt(MSE)
print('Error', RMSE)


# In[19]:


print('Predicted Water in l', prediction2)


# In[22]:


MSE2 = metrics.mean_squared_error(y_test2, prediction2)
RMSE2 = np.sqrt(MSE2)
print('Error', RMSE2)

