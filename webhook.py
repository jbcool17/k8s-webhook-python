import logging
import math
import os
from decimal import Decimal

from flask import Flask, jsonify, request
from kubernetes import config, utils

logging.basicConfig(format="%(asctime)s: %(levelname)s - %(message)s", level=os.getenv("LOG_LEVEL", "DEBUG"))

app = Flask(__name__)


class WebhookHandler:
    """
    Handle me some kubernetes webhooks
    """

    def __init__(self, request_info: dict):
        self.request_info = request_info
        self.admission_review = f"{request_info['kind']} - {request_info['apiVersion']}"
        logging.info(
            "%s | kind: %s - operation: %s - namespace: %s - name: %s",
            self.admission_review,
            self.request_info["request"]["object"]["kind"],
            self.request_info["request"]["operation"],
            self.request_info["request"]["namespace"],
            self.request_info["request"]["name"],
        )
        self.default_response = None
        self.response = None

    @staticmethod
    def build_default_response(request_info, check_name) -> dict:
        """
        Setup admission review reponse
        """
        response = {
            "apiVersion": request_info["apiVersion"],
            "kind": request_info["kind"],
            "response": {
                "allowed": False,
                "uid": request_info["request"]["uid"],
                "status": {"message": f"{check_name}: OK"},
            },
        }
        return response

    def validate_resources(self) -> dict:
        self.default_response = WebhookHandler.build_default_response(
            request_info=self.request_info, check_name="validate-resources"
        )
        self.response = check_container_resource_ratio(request_info=self.request_info, response=self.default_response)

        logging.info(self.response)

        return self.response

    def validate_replicas(self) -> dict:
        self.default_response = WebhookHandler.build_default_response(
            request_info=self.request_info, check_name="validate-resources"
        )
        self.response = check_replicas(request_info=self.request_info, response=self.default_response)

        logging.info(self.response)

        return self.response

    def validate_service_accounts(self) -> dict:
        self.default_response = WebhookHandler.build_default_response(
            request_info=self.request_info, check_name="validate-service-accounts"
        )
        self.response = check_service_account(request_info=self.request_info, response=self.default_response)

        logging.info(self.response)

        return self.response


# ------------------------------------------------------------------------------
#  ROUTES
# ------------------------------------------------------------------------------
@app.route("/validate-resources", methods=["POST"])
def validate_resources() -> jsonify:
    """
    Validate resources
    - container requests
    """
    whh = WebhookHandler(request_info=request.get_json())

    response = whh.validate_resources()

    return jsonify(response)


@app.route("/validate-replicas", methods=["POST"])
def validate_replicas() -> jsonify:
    """
    Validate replicasets
    """

    whh = WebhookHandler(request_info=request.get_json())

    response = whh.validate_replicas()

    return jsonify(response)


@app.route("/validate-service-accounts", methods=["POST"])
def validate_workload_identity() -> jsonify:
    """
    Validate service account annotations
    """
    whh = WebhookHandler(request_info=request.get_json())

    response = whh.validate_service_accounts()

    return jsonify(response)


# ------------------------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------------------------
def convert_size(size_bytes) -> dict:
    """
    Convert bytes to human readable format
    """
    if size_bytes == 0:
        return {"STRING": "0 B", "NUMBER": 0}

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(float(size_bytes) / p, 2)
    return {"STRING": f"{float(s)} {size_name[i]}", "NUMBER": float(s)}


def bytesto(bytes, to, bsize=1024):
    """
    Convert bytes
    """
    a = {"k": 1, "m": 2, "g": 3, "t": 4, "p": 5, "e": 6}
    # r = float(bytes)
    return bytes / (bsize ** a[to])


# ------------------------------------------------------------------------------
# VALIDATIONS
# ------------------------------------------------------------------------------
def check_replicas(request_info, response) -> dict:
    """
    Validate replicas
    - replicas less then or greater then 2
    """

    if request_info["request"]["object"]["spec"]["replicas"] > 2:
        response["response"]["status"]["message"] = f"{request_info['request']['name']} - Greater then 2"
    else:
        response["response"]["status"]["message"] = f"{request_info['request']['name']} - Less then or equal to 2"

    response["response"]["allowed"] = True

    return response


def check_service_account(request_info, response) -> dict:
    """
    Validate service accounts
    - check for annotations
    """
    if "annotations" in request_info["request"]["object"]["metadata"].keys():
        annotations = request_info["request"]["object"]["metadata"]["annotations"]

        response["response"]["status"]["message"] = annotations
    else:
        response["response"]["status"]["message"] = "No annotations found"

    response["response"]["allowed"] = True

    return response

def check_container_resource_ratio(request_info, response) -> dict:
    """
    Review container resource requests and total them per pod
    """
    total_request_cpu = Decimal(0)
    total_request_mem = Decimal(0)

    containers = request_info["request"]["object"]["spec"]["containers"]
    for container in containers:
        # Get requests and total cpu / memory per pod
        if "resources" in container and "requests" in container["resources"]:
            if "cpu" in container["resources"]["requests"]:
                total_request_cpu += utils.parse_quantity(container["resources"]["requests"]["cpu"])
            if "memory" in container["resources"]["requests"]:
                total_request_mem += utils.parse_quantity(container["resources"]["requests"]["memory"])
            response["response"]["allowed"] = True
            response["response"]["status"][
                "message"
            ] = f"TOTAL CPU: {total_request_cpu} | TOTAL MEM:  {total_request_mem} B, {convert_size(total_request_mem)['STRING']}"
        else:
            response["response"]["allowed"] = True
            response["response"]["status"]["message"] = "Resource Requests not found"

    return response


if __name__ == "__main__":
    # try:
    config.load_incluster_config()
    print("In Cluster Config Loaded.")
    app.run(debug=True, host="0.0.0.0", port=8443, ssl_context=("/etc/certs/tls.crt", "/etc/certs/tls.key"))
    # except Exception as e:
    #     logging.info(e)
    #     config.load_kube_config()
    #     app.run(debug=True, host="0.0.0.0")
    # print("Local Config Loaded.")
