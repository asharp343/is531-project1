from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_autoscaling as asg,
    aws_rds as rds,
    aws_elasticloadbalancingv2 as elb
)

from aws_cdk import core


class Is531Project1Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self,'custom-vpc',
            cidr = '10.0.0.0/16',
        )

        web_target_group = elb.ApplicationTargetGroup(self,
            'web_instance_target_group',
            vpc=vpc
        )

        web_autoscaling_group = asg.AutoScalingGroup(self,
            'web_instance_autoscaling_group',
            instance_type=ec2.InstanceType('t2.micro'),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=vpc.public_subnets)
        )


        # FIXME add the autoscaling group to the target that the load balancer is pointing to
        # web_target_group.add_target(web_autoscaling_group)
        # web_autoscaling_group.attach_to_application_target_group(web_target_group)

        img_bucket = s3.Bucket(self, 'img-bucket',
            public_read_access=False,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        rds_instance = rds.DatabaseInstance(self, 'rds-instance',
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            vpc=vpc,
            allocated_storage=20,
            max_allocated_storage=25,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            instance_type=ec2.InstanceType('t3.micro'),
        )

        web_alb = elb.ApplicationLoadBalancer(self, "my-alb",
            vpc=vpc
        )

        web_alb.add_listener(
            'attach_web_asg',
            port=80,
            default_target_groups=[web_target_group]
        )


        # cdk.CfnOutput(self, 'private-subnet-ids',
        #     value=str(vpc.private_subnets)
        # )
        # cdk.CfnOutput(self, 'public-subnet-ids',
        #     value=str(vpc.public_subnets)
        # )