# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 10:15:24 2021

@author: eliza
"""

import requests
import zipfile
import io


# Setting user Parameters
apiToken = "9v4BIGKcII9oXrBqZvsFutUu4umNzA4IfJYXTBzH" #I will replace this
surveyId = "SV_1TtM2yPc7fupIma" #I will replace this
fileFormat = "csv"
dataCenter = "sjc1" #I will replace this
mypath = "c:/Users/eliza/Downloads"



# Setting static parameters
requestCheckProgress = int(0)
progressStatus = "in progress"
baseUrl = "https://{0}.qualtrics.com/API/v3/responseexports/".format(dataCenter)
headers = {
    "content-type": "application/json",
    "x-api-token": apiToken,
    }

# Step 1: Creating Data Export
downloadRequestUrl = baseUrl
downloadRequestPayload = '{"format":"' + fileFormat + '","surveyId":"' + surveyId + '"}'
downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
progressId = downloadRequestResponse.json()["result"]["id"]
print(downloadRequestResponse.text)

# Step 2: Checking on Data Export Progress and waiting until export is ready
while requestCheckProgress < 100 and progressStatus != "complete":
    requestCheckUrl = baseUrl + progressId
    requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
    requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
    print("Download is " + str(round(requestCheckProgress)) + " complete")

# Step 3: Downloading file
requestDownloadUrl = baseUrl + progressId + '/file'
requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

# Step 4: Unzipping the file
zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall(mypath + "/MyQualtricsDownload")
print('Complete')
