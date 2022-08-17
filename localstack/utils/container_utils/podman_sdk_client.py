from abc import ABC
from typing import Dict, List, Optional, Tuple, Union

import podman
from podman import PodmanClient
from podman.errors import APIError, ContainerError, DockerException, ImageNotFound, NotFound

from localstack.utils.container_utils.container_client import (
    AccessDenied,
    CancellableStream,
    ContainerClient,
    ContainerException,
    DockerContainerStatus,
    NoSuchContainer,
    NoSuchImage,
    NoSuchNetwork,
    PortMappings,
    RegistryConnectionError,
    SimpleVolumeBind,
    Util,
)

uri = "unix:///run/user/1000/podman/podman.sock"


class SdkPodmanClient(ContainerClient):
    podman_client: Optional[PodmanClient]

    def __init__(self):
        self.podman_client = PodmanClient()

    def get_container_status(self, container_name: str) -> DockerContainerStatus:
        pass

    def stop_container(self, container_name: str, timeout: int = None):
        pass

    def restart_container(self, container_name: str, timeout: int = 10):
        pass

    def pause_container(self, container_name: str):
        pass

    def unpause_container(self, container_name: str):
        pass

    def remove_container(self, container_name: str, force=True, check_existence=False) -> None:
        pass

    def remove_image(self, image: str, force: bool = True) -> None:
        pass

    def list_containers(self, filter: Union[List[str], str, None] = None, all=True) -> List[dict]:
        container_list = self.podman_client.containers.list()
        result = []
        try:
            for container in container_list:
                result.append(
                    {
                        "id": container.id,
                        "image": container.image,
                        "name": container.name,
                        "status": container.status,
                        "labels": container.labels,
                    }
                )

            return result

        except APIError as e:
            raise ContainerException() from e

    def copy_into_container(
        self, container_name: str, local_path: str, container_path: str
    ) -> None:
        pass

    def copy_from_container(
        self, container_name: str, local_path: str, container_path: str
    ) -> None:
        pass

    def pull_image(self, docker_image: str) -> None:
        pass

    def push_image(self, docker_image: str) -> None:
        pass

    def build_image(self, dockerfile_path: str, image_name: str, context_path: str = None) -> None:
        pass

    def tag_image(self, source_ref: str, target_name: str) -> None:
        pass

    def get_docker_image_names(self, strip_latest=True, include_tags=True) -> List[str]:
        pass

    def get_container_logs(self, container_name_or_id: str, safe=False) -> str:
        pass

    def stream_container_logs(self, container_name_or_id: str) -> CancellableStream:
        pass

    def inspect_container(self, container_name_or_id: str) -> Dict[str, Union[Dict, str]]:
        pass

    def inspect_image(self, image_name: str, pull: bool = True) -> Dict[str, Union[Dict, str]]:
        pass

    def inspect_network(self, network_name: str) -> Dict[str, Union[Dict, str]]:
        pass

    def connect_container_to_network(
        self, network_name: str, container_name_or_id: str, aliases: Optional[List] = None
    ) -> None:
        pass

    def disconnect_container_from_network(
        self, network_name: str, container_name_or_id: str
    ) -> None:
        pass

    def get_container_ip(self, container_name_or_id: str) -> str:
        pass

    def has_docker(self) -> bool:
        pass

    def commit(self, container_name_or_id: str, image_name: str, image_tag: str):
        pass

    def create_container(
        self,
        image_name: str,
        *,
        name: Optional[str] = None,
        entrypoint: Optional[str] = None,
        remove: bool = False,
        interactive: bool = False,
        tty: bool = False,
        detach: bool = False,
        command: Optional[Union[List[str], str]] = None,
        mount_volumes: Optional[List[SimpleVolumeBind]] = None,
        ports: Optional[PortMappings] = None,
        env_vars: Optional[Dict[str, str]] = None,
        user: Optional[str] = None,
        cap_add: Optional[List[str]] = None,
        cap_drop: Optional[List[str]] = None,
        security_opt: Optional[List[str]] = None,
        network: Optional[str] = None,
        dns: Optional[str] = None,
        additional_flags: Optional[str] = None,
        workdir: Optional[str] = None
    ) -> str:
        print("here")

    def run_container(
        self,
        image_name: str,
        stdin: bytes = None,
        *,
        name: Optional[str] = None,
        entrypoint: Optional[str] = None,
        remove: bool = False,
        interactive: bool = False,
        tty: bool = False,
        detach: bool = False,
        command: Optional[Union[List[str], str]] = None,
        mount_volumes: Optional[List[SimpleVolumeBind]] = None,
        ports: Optional[PortMappings] = None,
        env_vars: Optional[Dict[str, str]] = None,
        user: Optional[str] = None,
        cap_add: Optional[List[str]] = None,
        cap_drop: Optional[List[str]] = None,
        security_opt: Optional[List[str]] = None,
        network: Optional[str] = None,
        dns: Optional[str] = None,
        additional_flags: Optional[str] = None,
        workdir: Optional[str] = None
    ) -> Tuple[bytes, bytes]:
        pass

    def exec_in_container(
        self,
        container_name_or_id: str,
        command: Union[List[str], str],
        interactive: bool = False,
        detach: bool = False,
        env_vars: Optional[Dict[str, Optional[str]]] = None,
        stdin: Optional[bytes] = None,
        user: Optional[str] = None,
        workdir: Optional[str] = None,
    ) -> Tuple[bytes, bytes]:
        pass

    def start_container(
        self,
        container_name_or_id: str,
        stdin: bytes = None,
        interactive: bool = False,
        attach: bool = False,
        flags: Optional[str] = None,
    ) -> Tuple[bytes, bytes]:
        pass
