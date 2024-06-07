

# student-tracker

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- student_tracker - Code for the S3 Trigger and State Machine Lambda Functions.
- mail - API'S to send/notify recipients of the report card
- api - API fetch function to retireve marks 
- events - Invocation events that you can use to invoke the function.
- template.yaml - A template that defines the application's AWS resources.
  
## Deploy and Run the Student-Tracker application

1. Clone the repositry on your local machine using git.
2. To build and deploy the application, run the following in your shell:

```bash
sam build 
sam deploy --guided
```
3. Student Database has been Created based on student_personal_details.csv and can be found here https://us-east-1.console.aws.amazon.com/dynamodbv2/home?region=us-east-1#table?name=Student_details . The appropriate Schema has been defined according to students_assessment_details.csv. (student assesment details files are present in the TestCases folder).
4. To trigger the State Machine we upload the desired assessment file into the s3 bucket using AWS CLI
   
```bash
aws s3 cp "<Source-path>" s3://student-tracker-presigns3-jpcnxtpwieck/ 
```
5. Once Uploaded Check the DynamoDB table for the updated values including percentage and Grade.

Link to the Deployed Application: https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/stackinfo?filteringText=&filteringStatus=active&viewNested=true&stackId=arn%3Aaws%3Acloudformation%3Aus-east-1%3A960351580303%3Astack%2Fstudent-tracker%2F4a45c730-1d79-11ef-a743-129186f572e5


## Test the API's of the Student-Tracker application

1. All the API Endpoints are present in the Output Section of the Cloudformation Stack.
2. They can be tested locally on Postman.
3. "authorizationToken" header must be passed as header to validate api requests. A placeholder value "abc-123" should be given.
4. The Parameters for the to test the API's are -
   - FetchAssessmentApiUrl : "ID" and "assessment"
   - FetchAllAssessmentApiUrl : "ID"
   - TeacherSESApiUrl : "class" and "teachers_email"
   - ParentSESApiUrl : "parents_email" and "ID"







## Output
1. Email Report sent to mail ID
![Screenshot 2024-06-01 162025](https://github.com/gauthamprakashan/Student-Report-Antstack/assets/58351649/198b2797-9ecd-4bc6-9973-de07d5c8b8b3)

2. Fetching assessment details.
![output1](https://github.com/gauthamprakashan/Student-Report-Antstack/assets/58351649/84e45104-e37a-4d0d-963b-6f96ec12631f)




