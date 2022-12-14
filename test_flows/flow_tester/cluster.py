from datetime import datetime, timedelta
import re
from os import path
import random
import subprocess
import sys
from time import sleep

import requests
from kubernetes import client
from kubernetes.client.exceptions import ApiException

from test_flows.flow_tester.util import class_name_from_file


REFRESH_INTERVAL = 1

CREATE_EXPR = re.compile(
    "Workflow ([a-z0-9\.]+|[a-z0-9]+) for flow [a-zA-Z0-9_]+ pushed to Argo Workflows successfully\.",
    re.M,
)


class Refreshable:
    def __init__(self):
        self._last_refresh = None

    def remaining_time(self):
        if self._last_refresh is None:
            return 0
        else:
            td = (datetime.utcnow() - self._last_refresh).seconds
            if td < REFRESH_INTERVAL:
                return REFRESH_INTERVAL - td
            else:
                return 0.0

    def wait_and_refresh(self):
        remaining = self.remaining_time()
        while remaining > 0:
            sleep(remaining * 0.25)
            remaining = self.remaining_time()
        self._refresh()

    def refresh(self):
        self.wait_and_refresh()

    def _refresh(self):
        try:
            self.on_refresh()
        finally:
            self._last_refresh = datetime.utcnow()

    def on_refresh(self):
        pass


class FlowRun(Refreshable):
    def __init__(self, id, data=None, api_key=""):
        super().__init__()
        self.id = id
        self.class_name = class_name_from_file(id)
        self.status = None
        self.started_at = None
        self.finished_at = None
        self.api_key = api_key
        if data is not None:
            self._populate(data)
        else:
            self.refresh()

    def api(self):
        return client.CustomObjectsApi()

    def __str__(self):
        started_at = datetime.strftime(self.started_at, "%Y-%m-%dT%H:%M:%SZ")
        return f"<FlowRun id: {self.id}, status: {self.status}, started: {started_at}>"

    def on_refresh(self):
        if self.status in ["Succeeded", "Failed", "Error"]:
            if self.started_at is not None and self.finished_at is not None:
                return
        result = self.api().get_namespaced_custom_object(
            "argoproj.io", "v1alpha1", "metaflow-jobs", "workflows", self.id
        )
        self._populate(result)

    def _populate(self, me):
        if "status" not in me:
            return
        else:
            my_status = me["status"]
            self.status = my_status["phase"]
            if self.started_at is None:
                if "startedAt" in my_status:
                    self.started_at = datetime.strptime(
                        my_status["startedAt"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                else:
                    self.started_at = datetime.utcnow()
            if self.status not in ["Pending", "Running"]:
                if self.finished_at is None and "finishedAt" in my_status:
                    self.finished_at = datetime.strptime(
                        my_status["finishedAt"], "%Y-%m-%dT%H:%M:%SZ"
                    )


class SearchTimeoutError(Exception):
    pass


class FlowFinder(Refreshable):
    def __init__(self, names, started_at, deadline):
        super().__init__()
        self.patterns = {}
        for name in names:
            pattern = ""
            updated = re.sub("_ns\.py$", "", name)
            if updated != name:
                pattern = ".*"
            else:
                pattern = "^"
                updated = re.sub("\.py$", "", name)
            updated = updated.replace("_", "")
            self.patterns[name] = f"{pattern}{updated}.*"
        self.min_started_at = started_at
        self._deadline = datetime.utcnow() + timedelta(seconds=deadline)
        self.found = []

    def api(self):
        return client.CustomObjectsApi()

    def _matches_name(self, candidate_name):
        matches = []
        for key in self.patterns.keys():
            pattern = self.patterns[key]
            if re.fullmatch(pattern, candidate_name):
                matches.append((key, pattern))
        if len(matches) > 0:
            if len(matches) == 1:
                return (True, matches[0][0])
            else:
                longest = None
                for m in matches:
                    if longest is None:
                        longest = m
                    else:
                        if len(m[1]) > len(longest[1]):
                            longest = m
                return (True, longest[0])
        return (False, None)

    def _is_deadline_exceeded(self):
        return datetime.utcnow() > self._deadline

    def on_refresh(self):
        if self._is_deadline_exceeded():
            if len(self.patterns.keys()) > 0:
                e = SearchTimeoutError("Flow discovery deadline exceeded")
                e.missing = self.patterns.keys()
                raise e
            return
        result = self.api().list_namespaced_custom_object(
            "argoproj.io",
            "v1alpha1",
            "metaflow-jobs",
            "workflows",
            limit=20,
            label_selector="workflows.argoproj.io/phase=Running",
        )
        for item in result["items"]:
            if "metadata" in item and "status" in item:
                started_at = datetime.strptime(
                    item["status"]["startedAt"], "%Y-%m-%dT%H:%M:%SZ"
                )
                if started_at >= self.min_started_at:
                    id = item["metadata"]["name"]
                    (matches, found_name) = self._matches_name(id)
                    if matches:
                        run = FlowRun(id, data=item)
                        self.found.append(run)
                        self.patterns.pop(found_name, None)

    def has_found_all(self):
        return len(self.patterns) == 0


class FlowRunner:
    def __init__(self, flow, api_key=""):
        self.name = path.basename(flow)
        self.class_name = class_name_from_file(self.name)
        self.flow = flow
        self.creator = Command(["python", flow, "argo-workflows", "create"])
        self.starter = Command(["python", flow, "argo-workflows", "trigger"])
        self.api_key = api_key

    def setup(self, env):
        output = self.creator.must(env)
        match = re.search(CREATE_EXPR, output)
        if match is None:
            print(f"{self.flow} creation output not found!")
            return None
        else:
            g = match.groups(1)
            file_name = f"FLOW_NAME_{int(datetime.timestamp(datetime.utcnow()) * 100)}"
            with open(file_name, "w+") as fd:
                if type(g) == str:
                    fd.write(f"{g}\n")
                else:
                    fd.write(f"{g[0]}\n")

    def run(self, env):
        output = self.starter.must(env)
        match = re.search("run-id argo-[a-z0-9\-\.]+", output)
        indices = match.span()
        match_text = output[indices[0] : indices[1]]
        id = match_text.split(" ")[-1].replace("argo-", "")
        return FlowRun(id, api_key=self.api_key)


class Command:
    def __init__(self, cmd):
        if type(cmd) == str:
            self.commands = cmd.split(" ")
        else:
            self.commands = cmd

    def execute(self, env, check=False):
        if env is None:
            result = subprocess.run(
                self.commands,
                text=True,
                check=check,
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE,
            )
        else:
            result = subprocess.run(
                self.commands,
                text=True,
                check=check,
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE,
                env=env,
            )
        return result

    def must(self, env):
        result = self.execute(env, check=True)
        return result.stdout.strip()

    def should(self):
        return self.execute().returncode == 0
