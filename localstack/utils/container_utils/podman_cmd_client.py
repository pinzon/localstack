import itertools
import json
import logging
import shlex
import subprocess
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
from localstack.utils.run import run, to_str

LOG = logging.getLogger(__name__)


class CmdPodmanClient(ContainerClient):

    default_run_outfile: Optional[str] = None

    def _podman_cmd(self) -> List[str]:
        return "podman".split()

    def get_container_status(self, container_name: str) -> DockerContainerStatus:
        pass

    def stop_container(self, container_name: str, timeout: int = None):
        if timeout is None:
            timeout = self.STOP_TIMEOUT
        cmd = self._podman_cmd()
        cmd += ["stop", "--time", str(timeout), container_name]
        LOG.debug("Stopping container with cmd %s", cmd)
        try:
            run(cmd)
        except subprocess.CalledProcessError as e:
            if "No such container" in to_str(e.stdout):
                raise NoSuchContainer(container_name, stdout=e.stdout, stderr=e.stderr)
            else:
                raise ContainerException(
                    "Podman process returned with errorcode %s" % e.returncode, e.stdout, e.stderr
                ) from e

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
        cmd = self._podman_cmd()
        cmd.append("ps")
        if all:
            cmd.append("-a")

        cmd.append("--format")
        cmd.append("{{json .}}")

        try:
            cmd_result = run(cmd).strip()

        except subprocess.CalledProcessError as e:
            raise ContainerException(
                "Podman process returned with errorcode %s" % e.returncode, e.stdout, e.stderr
            ) from e

        container_list = []
        if cmd_result:
            if cmd_result[0] == "[":
                container_list = json.loads(cmd_result)
            else:
                container_list = [json.loads(line) for line in cmd_result.splitlines()]
        result = []
        for container in container_list:
            result.append(
                {
                    "id": container["Id"],
                    "image": container["Image"],
                    "name": container["Names"],
                    "status": container["State"],
                    "labels": container["Labels"],
                }
            )
        return result

    def copy_into_container(
        self, container_name: str, local_path: str, container_path: str
    ) -> None:
        print("Not implemented")

    def copy_from_container(
        self, container_name: str, local_path: str, container_path: str
    ) -> None:
        print("Not implemented")
        pass

    def pull_image(self, docker_image: str) -> None:
        print("Not implemented")
        pass

    def push_image(self, docker_image: str) -> None:
        print("Not implemented")
        pass

    def build_image(self, dockerfile_path: str, image_name: str, context_path: str = None) -> None:
        print("Not implemented")
        pass

    def tag_image(self, source_ref: str, target_name: str) -> None:
        print("Not implemented")
        pass

    def get_docker_image_names(self, strip_latest=True, include_tags=True) -> List[str]:
        print("Not implemented")
        pass

    def get_container_logs(self, container_name_or_id: str, safe=False) -> str:
        print("Not implemented")
        pass

    def stream_container_logs(self, container_name_or_id: str) -> CancellableStream:
        print("Not implemented")
        pass

    def inspect_container(self, container_name_or_id: str) -> Dict[str, Union[Dict, str]]:
        print("Not implemented")
        pass

    def inspect_image(self, image_name: str, pull: bool = True) -> Dict[str, Union[Dict, str]]:
        print("Not implemented")
        pass

    def inspect_network(self, network_name: str) -> Dict[str, Union[Dict, str]]:
        print("Not implemented")
        pass

    def connect_container_to_network(
        self, network_name: str, container_name_or_id: str, aliases: Optional[List] = None
    ) -> None:
        print("Not implemented")
        pass

    def disconnect_container_from_network(
        self, network_name: str, container_name_or_id: str
    ) -> None:
        print("Not implemented")
        pass

    def get_container_ip(self, container_name_or_id: str) -> str:
        print("Not implemented")
        pass

    def has_docker(self) -> bool:
        print("Not implemented")
        pass

    def commit(self, container_name_or_id: str, image_name: str, image_tag: str):
        print("Not implemented")
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
        workdir: Optional[str] = None,
    ) -> str:
        print("here")

    def run_container(self, image_name: str, stdin: bytes = None, **kwargs) -> Tuple[bytes, bytes]:
        cmd, env_file = self._build_run_create_cmd("run", image_name, **kwargs)
        LOG.debug("Run container with cmd: %s", cmd)
        result = self._run_async_cmd(cmd, stdin, kwargs.get("name") or "", image_name)
        Util.rm_env_vars_file(env_file)
        return result

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
        print("Not implemented2")
        pass

    def start_container(
        self,
        container_name_or_id: str,
        stdin: bytes = None,
        interactive: bool = False,
        attach: bool = False,
        flags: Optional[str] = None,
    ) -> Tuple[bytes, bytes]:
        print("Not implemented1")
        pass

    def _run_async_cmd(
        self, cmd: List[str], stdin: bytes, container_name: str, image_name=None
    ) -> Tuple[bytes, bytes]:
        kwargs = {
            "inherit_env": True,
            "asynchronous": True,
            "stderr": subprocess.PIPE,
            "outfile": self.default_run_outfile or subprocess.PIPE,
        }
        if stdin:
            kwargs["stdin"] = True
        try:
            process = run(cmd, **kwargs)
            stdout, stderr = process.communicate(input=stdin)
            if process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode,
                    cmd,
                    stdout,
                    stderr,
                )
            else:
                return stdout, stderr
        except subprocess.CalledProcessError as e:
            stderr_str = to_str(e.stderr)
            if "Unable to find image" in stderr_str:
                raise NoSuchImage(image_name or "", stdout=e.stdout, stderr=e.stderr)
            if "No such container" in stderr_str:
                raise NoSuchContainer(container_name, stdout=e.stdout, stderr=e.stderr)
            raise ContainerException(
                "Podman process returned with errorcode %s" % e.returncode, e.stdout, e.stderr
            ) from e

    def _build_run_create_cmd(
        self,
        action: str,
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
        workdir: Optional[str] = None,
    ) -> Tuple[List[str], str]:
        env_file = None
        cmd = self._podman_cmd() + [action]
        if remove:
            cmd.append("--rm")
        if name:
            cmd += ["--name", name]
        if entrypoint is not None:  # empty string entrypoint can be intentional
            cmd += ["--entrypoint", entrypoint]

        # if mount_volumes:
        #     cmd += [
        #         volume
        #         for host_path, docker_path in dict(mount_volumes).items()
        #         for volume in ["-v", f"{host_path}:{docker_path}"]
        #     ]
        if interactive:
            cmd.append("--interactive")
        if tty:
            cmd.append("--tty")
        if detach:
            cmd.append("--detach")
        if ports:
            cmd += ports.to_list()
        if env_vars:
            env_flags, env_file = Util.create_env_vars_file_flag(env_vars)
            cmd += env_flags
        if user:
            cmd += ["--user", user]
        if cap_add:
            cmd += list(itertools.chain.from_iterable(["--cap-add", cap] for cap in cap_add))
        if cap_drop:
            cmd += list(itertools.chain.from_iterable(["--cap-drop", cap] for cap in cap_drop))
        if security_opt:
            cmd += list(
                itertools.chain.from_iterable(["--security-opt", opt] for opt in security_opt)
            )
        if network:
            cmd += ["--network", network]
        if dns:
            cmd += ["--dns", dns]
        if workdir:
            cmd += ["--workdir", workdir]
        if additional_flags:
            cmd += shlex.split(additional_flags)
        cmd.append(image_name)
        if command:
            cmd += command if isinstance(command, List) else [command]
        return cmd, env_file
