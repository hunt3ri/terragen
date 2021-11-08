import pytest
from providers.aws.models.terragen_models import TerraformS3Backend, TerraformAWSProvider, TerraformDataSource


class TestTerragenModels:
    def test_terraform_s3_backend(self):
        s3_backend = TerraformS3Backend(
            bucket="test-bucket", region="us-east-1", profile="hunter-labs", key="/shared/test"
        )

        assert s3_backend.bucket == "test-bucket"

    def test_terraform_aws_provider(self):
        aws_provider = TerraformAWSProvider(region="us-east-1", profile="hunter-labs")
        assert aws_provider.profile == "hunter-labs"

    def test_get_lookup_values_raises_error_for_missing_outputs(self):
        with pytest.raises(ValueError):
            TerraformDataSource.from_lookup("lookup: shared.vpc.simple_vpc")
