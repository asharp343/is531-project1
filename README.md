
# IS 531 Project 1 README

1. Clone repo

2. Create virtual env

3. Once the virtualenv is activated, you can install the required dependencies.
```
$ pip install -r requirements.txt
```

4. Deploy CDK stakc
```
cdk deploy
```
NOTE: You must have an IAM user access key and secret access key with programatic admin permissions

5. Populate the db
    * Go to cloud formation and access the lambda function called "write_to_db"
    * Invoke the function
        * Click "Test"
        * Name the test
        * Click "Test" again
        Note: the JSON test body doesnt matter

6. Access the website
    * Go to EC2 and grab the instance public DNS name

7. Cleanup 
```
cdk destroy
```



## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

