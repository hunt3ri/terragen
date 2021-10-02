from providers.aws.terragen.models.terragen_models import TerraformS3Backend, TerraformAWSProvider


def test_terraform_s3_backend():
    s3_backend = TerraformS3Backend(bucket="test-bucket",
                                    region="us-east-1",
                                    profile="hunter-labs",
                                    key="/shared/test")

    iain = str(s3_backend)
    ab = iain


def test_terraform_aws_provider():
    aws_provider = TerraformAWSProvider(region="us-east-1",
                                        profile="hunter-labs")
    print(aws_provider)