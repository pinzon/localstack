from localstack.utils.container_utils.container_client import ContainerClient


def create_podman_client():
    # from localstack.utils.container_utils.podman_sdk_client import SdkPodmanClient
    from localstack.utils.container_utils.podman_cmd_client import CmdPodmanClient

    return CmdPodmanClient()


PODMAN_CLIENT: ContainerClient = create_podman_client()
