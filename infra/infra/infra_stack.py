import os
import subprocess
from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct
from dotenv import load_dotenv


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Load environment variables from .env file
        load_dotenv()

        # Use the default VPC
        vpc = ec2.Vpc(self, "Vpc", max_azs=1)

        # Create a cluster
        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        # Define the Docker image from the Dockerfile
        docker_image = ecs.ContainerImage.from_asset("../")

        # Create a Fargate task definition
        task_definition = ecs.FargateTaskDefinition(self, "TaskDef", cpu=512, memory_limit_mib=1024)

        # TODO: Limit more
        task_definition.task_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBedrockFullAccess")
        )

        # TODO: Limit to the specific bucket
        task_definition.task_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )

        # Add container to the task definition
        container = task_definition.add_container(
            "Container", image=docker_image, memory_limit_mib=1024
        )

        for env_var in ["OPENAI_API_KEY", "SLACK_BOT_TOKEN", "SLACK_APP_TOKEN"]:
            container.add_environment(env_var, os.environ[env_var])

        # set the GIT SHA
        container.add_environment("GIT_SHA", subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip())

        fargate_service = ecs.FargateService(
            self,
            "Service",
            cluster=cluster,
            task_definition=task_definition,
            # instances
            desired_count=1,
        )
