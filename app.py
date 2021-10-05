#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

from aws_cdk import core

from is531_project_1.is531_project_1_stack import Is531Project1Stack


app = core.App()
Is531Project1Stack(app, "Is531Project1Stack",)

app.synth()
