"""
Creates a job using Api from file job.yaml.
"""
import os
import sys
from time import sleep
import pdb
import logging
import argparse
import traceback

import urllib3
import yaml
from kubernetes import client, config
from kubernetes.client.api import core_v1_api
from kubernetes.watch import Watch


NAMESPACE = "openmmlab-test"
# create formatter
FMT = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
logging.basicConfig(level=logging.INFO, format=FMT)
logger = logging.getLogger(__name__)


class Job:
    def __init__(self, namespace, job_name=None):
        self.namespace = namespace
        config.load_kube_config()
        self.core_v1 = core_v1_api.CoreV1Api()
        self.batch_v1 = client.BatchV1Api()
        self.job_name = job_name if job_name else None

    def reset_connection(self):
        config.load_kube_config()
        self.core_v1 = core_v1_api.CoreV1Api()
        self.batch_v1 = client.BatchV1Api()

    def create(self, job_yaml, image_name, cmd):
        with open(os.path.join(os.path.dirname(__file__), job_yaml)) as f:
            dep = yaml.safe_load(f)
            if self.job_name:
                dep["metadata"]["name"] = job_name
                dep["spec"]["template"]["metadata"]["labels"]["job-name"] = job_name
            dep["spec"]["template"]["spec"]["containers"][0]["image"] = image_name
            dep["spec"]["template"]["spec"]["containers"][0]["name"] = job_name
            # update args for executing cmd
            dep["spec"]["template"]["spec"]["containers"][0]["args"] = ["-c", cmd]
            try:
                api_response = self.batch_v1.create_namespaced_job(
                    body=dep,
                    namespace=self.namespace)
                logger.info("Job created. status='%s'" % str(api_response.status))
            except Exception as e:
                logger.error("Create failed with %s" % str(e))

    def get_pod(self):
        pod_name = None
        pod_list = self.core_v1.list_namespaced_pod(namespace=self.namespace, label_selector="job-name=%s" % self.job_name)
        if not pod_list.items:
            logger.warning("No pod found")
            return None
        if len(pod_list.items) > 1:
            logger.warning("Many pods in job")
            return None
        pod = pod_list.items[0]
        pod_name = pod.metadata.name
        logger.info("Pod: %s status: %s" % (pod_name, pod.status.phase))
        if pod.status.phase.lower() != "running":
            return None
        return pod_name

    # get the status of the job
    def get_status(self):
        """
        Function: get the status of the job
        """
        job_completed = False
        api_response = self.batch_v1.read_namespaced_job_status(
            name=self.job_name,
            namespace=self.namespace)
        if api_response.status.succeeded is not None or \
                api_response.status.failed is not None:
            job_completed = True
            logger.info("Job completed")
        return job_completed, api_response.status.succeeded

    def watch_log(self):
        pod_name = None

        while self.get_status()[0] is False:
            pod_name = self.get_pod()
            if not pod_name:
                sleep(2)
                continue
            try:
                # tmp = False
                logger.info("Pod name: %s in watch_log" % (pod_name))
                watcher = Watch()
                for event in watcher.stream(
                        self.core_v1.read_namespaced_pod_log,
                        name=pod_name,
                        # follow=False,
                        _request_timeout=60,
                        # _preload_content=False,
                        container=self.job_name,
                        namespace=self.namespace):
                    logger.info(event)
                    # tmp = True
                # if tmp:
                #     break
                #     # if event["type"] == "DELETED":
                #     #     watcher.stop()
            except client.rest.ApiException as e:
                logger.error("Pod starting ...")
                sleep(2)
            except urllib3.exceptions.MaxRetryError as e:
                logger.error(str(e))
                self.reset_connection()
            except Exception as e:
                logger.error(str(e))
                logger.error(traceback.format_exc())
                pass

    def delete(self):
        api_response = self.batch_v1.delete_namespaced_job(
            name=self.job_name,
            namespace=self.namespace,
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5))
        logger.info("Job deleted. status='%s'" % str(api_response.status))


if __name__ == '__main__':
    job_name = "dev-test-8"
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument(
        "--job-name",
        default="unit-test",
        help="job name")
    arg_parser.add_argument(
        "--namespace",
        default=NAMESPACE,
        help="cluster namespace")
    arg_parser.add_argument(
        "--job-yaml",
        metavar='FILE',
        default='job.yaml',
        help="load job yaml")
    arg_parser.add_argument(
        "--image-name",
        default='registry.sensetime.com/mmcv/ubuntu_1804_py_37_cuda_101_cudnn_7_torch_160_dev:20211020',
        help="image name")
    arg_parser.add_argument(
        "--cmd",
        default='',
        help="excute cmd")

    args = arg_parser.parse_args()

    job_yaml = args.job_yaml
    job_name = args.job_name.replace("_", "-")
    namespace = args.namespace
    image_name = args.image_name
    cmd = args.cmd
    logger.info(cmd)

    if not image_name or not cmd:
        logger.error("Params invalid")
        sys.exit(-1)

    job = Job(namespace, job_name=job_name)
    job.create(job_yaml, image_name, cmd)
    job.watch_log()
    # Wait job to finish 
    while job.get_status()[0] is False:
        sleep(1)
    status = job.get_status()
    # The job is done successfully (status[1] = api_response.status.succeeded)
    if status[1]:
        job.delete()     # release the pod resources when the job is done
        sys.exit(0)
    else:
        job.delete()
        sys.exit(1)
