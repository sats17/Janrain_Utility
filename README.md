[![License](http://img.shields.io/:license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)
[![Generic badge](https://img.shields.io/badge/built_by-Sats17-indigo.svg)](https://GitHub.com/sats17/)
[![Generic badge](https://img.shields.io/badge/built_with-Python-informational.svg)](https://curl.haxx.se/)

## Janrain Utility
Simple script that will help you to perform bulk data operations on Janrain.


### Prerequisite
##### Language
* Python 3
##### Python Libraries
* Pandas
* Requests
* Json
##### Input Variables
* RecordsFilePath = CSV File that contains required records.
* CredentialsFilePath = CSV File that contain your Janrain Credentials and entity related informations. (Required)

##### Required fields for Credentials File. (Make sure your credentials CSV File header name should be same as mentioned below)
* url : Janrain API URL
* client_id : Janrain Client Id
* client_secret : Janrain Client Secret
* type_name : Janrain Entity name

