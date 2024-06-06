from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_ecs as ecs,
    aws_ec2 as ec2,
)
from constructs import Construct
from dotenv import load_dotenv


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Load environment variables from .env file
        load_dotenv()

        # Use the default VPC
        vpc = ec2.Vpc(self, "Vpc", max_azs=2)

        # Create a cluster
        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        # Define the Docker image from the Dockerfile
        docker_image = ecs.ContainerImage.from_asset("../")

        # Create a Fargate task definition
        task_definition = ecs.FargateTaskDefinition(self, "TaskDef")

        # Add container to the task definition
        container = task_definition.add_container(
            "Container", image=docker_image, memory_limit_mib=1024
        )

        # # Set environment variables from the .env file
        # for key, value in os.environ.items():
        #     if key.startswith("ENV_VAR_"):  # You can filter the env vars if needed
        #         container.add_environment(key, value)

        fargate_service = ecs.FargateService(
            self,
            "Service",
            cluster=cluster,
            task_definition=task_definition,
            # instances
            desired_count=1,
        )
