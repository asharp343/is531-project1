from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_autoscaling as asg,
    aws_rds as rds,
    aws_elasticloadbalancingv2 as elb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_codecommit as codecommit,
    aws_codedeploy as codedeploy,
    aws_codepipeline as codepipeline
)

from aws_cdk import core


class Is531Project1Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ######################## VPC ############################
        #########################################################
        vpc = ec2.Vpc(self,'custom-vpc',
            cidr = '10.0.0.0/16',
        )


        ######################## EC2 ASG ########################
        #########################################################
        web_sg = ec2.SecurityGroup(self,
            'web-sg',
            vpc = vpc,
            allow_all_outbound=True,
        )
        web_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port(
                string_representation='web-sg-http',
                protocol=ec2.Protocol.TCP,
                from_port=80,
                to_port=80
            )
        )
        # #### Uncomment ingress rule below if you need to ssh into the web server
        # web_sg.add_ingress_rule(
        #     peer=ec2.Peer.any_ipv4(),
        #     connection=ec2.Port(
        #         string_representation='web-sg-ssh',
        #         protocol=ec2.Protocol.TCP,
        #         from_port=22,
        #         to_port=22
        #     )
        # )

        web_autoscaling_group = asg.AutoScalingGroup(self,
            'web_instance_autoscaling_group',
            instance_type=ec2.InstanceType('t2.micro'),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=vpc.public_subnets),
            key_name='is531-project1', # Uncomment key_name if you need to ssh into the web server. You'll also need to create a key called "is531-project1" if you dont have one
            # security_group = web_sg
        )

        webserver_bootstrap = open('scripts/ec2_webserver.txt', 'r').read()
        web_autoscaling_group.add_user_data(webserver_bootstrap)

        
        ########################### S3 ##########################
        #########################################################
        donut_img_bucket = s3.Bucket(self, 'donut-img-bucket',
            public_read_access=True,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )


        ########################## RDS ##########################
        #########################################################
        db_cluster = rds.ServerlessCluster(self, 'rds-cluster',
            engine=rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_10_11),
            vpc=vpc,
            default_database_name='donutdb',
            vpc_subnets=ec2.SubnetSelection(subnets=vpc.private_subnets),
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )


        ########################## ALB ##########################
        #########################################################
        web_target_group = elb.ApplicationTargetGroup(self,
            'web_instance_target_group',
            port=80,
            vpc=vpc,
        )

        web_target_group.add_target(web_autoscaling_group)

        web_alb = elb.ApplicationLoadBalancer(self, "my-alb",
            vpc=vpc,
            internet_facing=True
        )

        web_alb.add_listener(
            'attach_web_asg',
            port=80,
            default_target_groups=[web_target_group]
        )


        #################### Lambda #############################
        #########################################################
        query_db = _lambda.Function(self, 'query_db',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('static_assets/lambda/query_db'),
            handler='index.lambda_handler',
            vpc=vpc
        )

        query_db.add_environment(
            key='CLUSTER_ARN',
            value=db_cluster.cluster_arn
        )
        query_db.add_environment(
            key='SECRET_ARN',
            value=db_cluster.secret.secret_arn
        )

        write_to_db = _lambda.Function(self, 'write_to_db',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('static_assets/lambda/write_to_db'),
            handler='index.lambda_handler',
            vpc=vpc,
            timeout=cdk.Duration.seconds(300)
        )

        write_to_db.add_environment(
            key='CLUSTER_ARN',
            value=db_cluster.cluster_arn
        )
        write_to_db.add_environment(
            key='SECRET_ARN',
            value=db_cluster.secret.secret_arn
        )


        #################### API Gateway ########################
        #########################################################
        apiPolicy = iam.PolicyDocument()
        apiPolicy.add_statements(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=['execute-api:Invoke'],
                resources=["execute-api:/*"],
            )
        )

        db_cluster.grant_data_api_access(query_db)
        db_cluster.grant_data_api_access(write_to_db)

        apigateway.LambdaRestApi(
            self,
            'query_db_api',
            handler=query_db,
            policy=apiPolicy,
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=['*']

            )
        )


        #################### CodePipeline ########################
        #########################################################
        # repo = codecommit.Repository(self, 'code-commit-repo',
        #     repository_name='is531-project1'
        # )
        # repo.apply_removal_policy(cdk.RemovalPolicy.DESTROY)

        # code_deploy_app = codedeploy.ServerApplication(self, 'code_deploy_app')
        # code_deploy_app.apply_removal_policy(cdk.RemovalPolicy.DESTROY)

        # code_deployment_group = codedeploy.ServerDeploymentGroup(self, 'code_deployment_group',
        #     application=code_deploy_app,
        #     auto_scaling_groups=[web_autoscaling_group]
        # )

        # pipeline = codepipeline.Pipeline(self, 'pipeline')
        # # pipeline.add_stage(
        # #     stage_name="push-to-repo",
        # # )


        ####################### Output ##########################
        #########################################################
        cdk.CfnOutput(self, 'import-Rds-Data',
            value=f'aws lambda invoke --function-name {write_to_db.function_name} ~/Desktop/resoponse.json'
        )
        cdk.CfnOutput(self, 'website-Url',
            value=f'http://{str(web_alb.load_balancer_dns_name)}'
        )
        # cdk.CfnOutput(self, 'repo Remote',
        #     value=repo.repository_clone_url_http
        # )
        