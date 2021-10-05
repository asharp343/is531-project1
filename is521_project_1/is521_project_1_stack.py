from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_autoscaling as asg
)

from aws_cdk import core


class Is521Project1Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self,
            'custom-vpc',
            cidr = '10.0.0.0/16'
        )

        my_asg = asg.AutoScalingGroup(
            self,
            'my-asg',
            instance_type=ec2.InstanceType('t2.micro'),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc

        )
