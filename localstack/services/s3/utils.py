import datetime
import re

from moto.s3.models import FakeKey

from localstack.aws.api import ServiceException
from localstack.aws.api.s3 import ChecksumAlgorithm, PutObjectRequest
from localstack.utils.strings import checksum_crc32, checksum_crc32c, hash_sha1, hash_sha256

checksum_keys = ["ChecksumSHA1", "ChecksumSHA256", "ChecksumCRC32", "ChecksumCRC32C"]

BUCKET_NAME_REGEX = (
    r"(?=^.{3,63}$)(?!^(\d+\.)+\d+$)"
    + r"(^(([a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])\.)*([a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])$)"
)


class InvalidRequest(ServiceException):
    """The lifecycle configuration does not exist."""

    code: str = "InvalidRequest"
    sender_fault: bool = False
    status_code: int = 400


def verify_checksum(checksum_algorithm: str, data: bytes, request: PutObjectRequest):
    key = f"Checksum{checksum_algorithm.upper()}"
    checksum = request.get(key)  # noqa
    # TODO: is there a message if the header is missing?
    match checksum_algorithm:
        case ChecksumAlgorithm.CRC32:
            calculated_checksum = checksum_crc32(data)

        case ChecksumAlgorithm.CRC32C:
            calculated_checksum = checksum_crc32c(data)

        case ChecksumAlgorithm.SHA1:
            calculated_checksum = hash_sha1(data)

        case ChecksumAlgorithm.SHA256:
            calculated_checksum = hash_sha256(data)

        case _:
            # TODO: check proper error? for now validated client side, need to check server response
            raise InvalidRequest("The value specified in the x-amz-trailer header is not supported")

    if calculated_checksum != checksum:
        raise InvalidRequest(
            f"Value for x-amz-checksum-{checksum_algorithm.lower()} header is invalid."
        )


def is_key_expired(key_object: FakeKey) -> bool:
    if not key_object or not key_object._expiry:
        return False
    return key_object._expiry <= datetime.datetime.now(key_object._expiry.tzinfo)


def is_bucket_name_valid(bucket_name: str) -> bool:
    """
    ref. https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html
    """
    return bucket_name.islower() and re.match(BUCKET_NAME_REGEX, bucket_name)
