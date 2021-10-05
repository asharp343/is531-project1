from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_autoscaling as asg
)

from aws_cdk import core


class Is531Project1Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self,
            'custom-vpc',
            cidr = '10.0.0.0/16',
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name='public1',
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name='public2',
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name='private1',
                    subnet_type=ec2.SubnetType.PRIVATE,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name='private2',
                    subnet_type=ec2.SubnetType.PRIVATE,
                    cidr_mask=24
                )
            ]
        )

        my_asg = asg.AutoScalingGroup(
            self,
            'my-asg',
            instance_type=ec2.InstanceType('t2.micro'),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc

        )

        img_bucket = s3.Bucket(
            self,
            'img-bucket',
            public_read_access=False,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )