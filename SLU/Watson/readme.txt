This directory contains the implementation of a dialog module based on IBM's Watson Dialog Service.

IBM Bluemix is a cloud platform which provides diverse IT services, the one we're using is the dialog service under Watson catelog.
To use the service, a Bluemix account is necessary and detail about the service could be found from:
http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/dialog/

Another IBM Bluemix service worth to mention is the DevOps service, which supports the whole development process. The application for dialog service can be considered as a project, and the codes can be managed, build and deploy online with this service. It also provides interface for project planning and tracking.

Demo applications based on the dialog service are open-sourced and available from Watson Developer Cloud on GitHub:
https://github.com/watson-developer-cloud/dialog-nodejs
https://github.com/watson-developer-cloud/movieapp-dialog

A cloud foundry CLI and dialog tool can be used to create, manage and interact with dialogs for the service, although RESTful method seems to exist with limited functionality, detail can be found from API reference page:
Dialog Tool: https://github.com/watson-developer-cloud/dialog-tool
API Reference: http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/dialog/api/v1/#update-dialog

Applications are actual execution units that access the service, it can be deployed with the cloud foundry CLI tool. After deploying an application, RESTful request can now be sent to he application and get dialog response, and that's our goal! Note that to access the application, use credentials for the service rather than environment variables for the application.

For this project, the dialog application is based on one of the open-source samples and saved in 'Watson/dialog-nodejs/' directory. the actual dialog configurations are XML files in the 'Watson/dialog-nodejs//dialogs/' directory. Tutorial can be found from:
http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/dialog/tutorial_advanced.shtml

