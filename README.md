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
3. Student Database has been Created based on student_personal_details.csv and can be found here https://us-east-1.console.aws.amazon.com/dynamodbv2/home?region=us-east-1#table?name=Student_details . The appropriate Schema has been defined according to students_assessment_details.csv
4. To trigger the State Machine we upload the desired assessment file into the s3 bucket using AWS CLI
   
```bash
aws s3 cp "<Source-path>" s3://student-tracker-presigns3-jpcnxtpwieck/ 
```
5. Once Uploaded Check the DynamoDB table for the updated values including percentage and Grade.
   
## Test the API's of the Student-Tracker application
1. All the API Endpoints are present in the Output Section of the Cloudformation Stack.
2. They can be tested locally on Postman.
3. "authorizationToken" header must be passed as header to validate api requests. A placeholder value "abc-123" should be given.
4. The Parameters for the to test the API's are -
   - FetchAssessmentApiUrl : "ID" and "assessment"
   - FetchAllAssessmentApiUrl : "ID"
   - TeacherSESApiUrl : "class" and "teachers_email"
   - ParentSESApiUrl : "parents_email" and "ID"




## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
student-tracker$ sam build --use-container
```

The SAM CLI installs dependencies defined in `hello_world/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
student-tracker$ sam local invoke <FunctionName> --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
student-tracker$ sam local start-api
student-tracker$ curl http://localhost:3000/
```
