#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

from aws_cdk import core

from is521_project_1.is521_project_1_stack import Is521Project1Stack


app = core.App()
Is521Project1Stack(app, "Is521Project1Stack",)

app.synth()
