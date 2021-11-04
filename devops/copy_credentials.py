"""
Workaround for using aws sso login command with serverless. Retrieves aws session token and stores it in .aws/credentials
"""
import argparse
import json
import os
import boto3
from dataclasses import dataclass
from configparser import ConfigParser


@dataclass()
class Credentials:
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    expiration: int

    @staticmethod
    def from_role_credentials(role_credentials: dict):
        return Credentials(
            aws_access_key_id=role_credentials["accessKeyId"],
            aws_secret_access_key=role_credentials["secretAccessKey"],
            aws_session_token=role_credentials["sessionToken"],
            expiration=role_credentials["expiration"],
        )


@dataclass()
class AwsProfileConfig:
    sso_region: str
    sso_account_id: str
    sso_role_name: str

    @staticmethod
    def from_profile_config(aws_profile: str, aws_config: ConfigParser):
        profile_config = aws_config[f"profile {aws_profile}"]
        return AwsProfileConfig(
            sso_region=profile_config["sso_region"],
            sso_account_id=profile_config["sso_account_id"],
            sso_role_name=profile_config["sso_role_name"],
        )


def copy_credentials(aws_profile):
    home_dir = os.environ["HOME"]
    aws_path = f"{home_dir}/.aws"
    sso_path = f"{aws_path}/sso/cache"

    aws_config = ConfigParser()
    aws_config.read(f"{aws_path}/config")
    profile_config = AwsProfileConfig.from_profile_config(aws_profile, aws_config)

    sso_cache_file_names = os.listdir(f"{home_dir}/.aws/sso/cache")
    sso_cache = {}
    for file_name in sso_cache_file_names:
        file_path = f"{sso_path}/{file_name}"
        with open(file_path, "r") as file:
            sso_cache.update(json.loads(file.read()))

    sso_client = boto3.client("sso", region_name=profile_config.sso_region)
    role_credentials_response = sso_client.get_role_credentials(
        roleName=profile_config.sso_role_name,
        accountId=profile_config.sso_account_id,
        accessToken=sso_cache["accessToken"],
    )
    credentials = Credentials.from_role_credentials(
        role_credentials_response["roleCredentials"]
    )

    aws_credentials_path = f"{aws_path}/credentials"
    credentials_config_object = ConfigParser()
    credentials_config_object.read(aws_credentials_path)
    credentials_config_object[aws_profile] = credentials.__dict__

    with open(aws_credentials_path, "w") as conf:
        credentials_config_object.write(conf)

    print(f"Copied credentials to {aws_credentials_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--aws-profile", required=False)
    args = parser.parse_args()
    aws_profile = args.aws_profile or os.environ["AWS_PROFILE"]
    copy_credentials(aws_profile)
