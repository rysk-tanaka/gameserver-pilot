"""AWS EC2 cloud provider implementation."""

import boto3
from botocore.exceptions import ClientError

from gameserver_pilot.cloud.base import CloudProvider


class EC2Provider(CloudProvider):
    """AWS EC2 implementation of CloudProvider."""

    def __init__(self, region: str = "ap-northeast-1") -> None:
        """Initialize EC2 provider.

        Args:
            region: AWS region name.
        """
        self.ec2 = boto3.client("ec2", region_name=region)

    async def start_server(self, server_id: str) -> bool:
        """Start an EC2 instance."""
        try:
            self.ec2.start_instances(InstanceIds=[server_id])
            return True
        except ClientError:
            return False

    async def stop_server(self, server_id: str) -> bool:
        """Stop an EC2 instance."""
        try:
            self.ec2.stop_instances(InstanceIds=[server_id])
            return True
        except ClientError:
            return False

    async def get_server_status(self, server_id: str) -> str:
        """Get EC2 instance status."""
        try:
            response = self.ec2.describe_instances(InstanceIds=[server_id])
            reservations = response.get("Reservations", [])
            if reservations:
                instances = reservations[0].get("Instances", [])
                if instances:
                    return instances[0].get("State", {}).get("Name", "unknown")
            return "unknown"
        except ClientError:
            return "error"

    async def get_server_ip(self, server_id: str) -> str | None:
        """Get EC2 instance public IP."""
        try:
            response = self.ec2.describe_instances(InstanceIds=[server_id])
            reservations = response.get("Reservations", [])
            if reservations:
                instances = reservations[0].get("Instances", [])
                if instances:
                    return instances[0].get("PublicIpAddress")
            return None
        except ClientError:
            return None
