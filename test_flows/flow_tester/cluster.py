from datetime import datetime, timedelta
import re
from os import path
import subprocess
from time import sleep

from kubernetes import client

REFRESH_INTERVAL = 2


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
                return 0

    def wait_and_refresh(self):
        remaining = self.remaining_time()
        if remaining == 0:
            self._refresh()
        else:
            sleep(remaining + 0.5)

    def refresh(self):
        self.wait_and_refresh()

    def _refresh(self):
        if self.remaining_time() <= 0:
            try:
                self.on_refresh()
            finally:
                self._last_refresh = datetime.utcnow()

    def on_refresh(self):
        pass


class FlowRun(Refreshable):
    def __init__(self, id, data=None):
        super().__init__()
        self.id = id
        self.status = None
        self.started_at = None
        self.finished_at = None
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
            print(me.keys())
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


class FlowFinder(Refreshable):
    def __init__(self, names, started_at, deadline):
        super().__init__()
        self.patterns = {}
        for name in names:
            updated = re.sub("_ns", "", name)
            updated = re.sub("\.py", "", updated)
            updated = re.sub("_", "", updated)
            self.patterns[name] = f".*{updated}.*"
        self.min_started_at = started_at
        self._deadline = datetime.utcnow() + timedelta(seconds=deadline)
        self.found = []

    def api(self):
        return client.CustomObjectsApi()

    def _matches_name(self, candidate_name):
        for key in self.patterns.keys():
            pattern = self.patterns[key]
            if re.fullmatch(pattern, candidate_name):
                return (True, key)
        return (False, None)

    def _is_deadline_exceeded(self):
        return datetime.utcnow() > self._deadline

    def on_refresh(self):
        if self._is_deadline_exceeded():
            raise TimeoutError("Flow discovery deadline exceeded")
        result = self.api().list_namespaced_custom_object(
            "argoproj.io", "v1alpha1", "metaflow-jobs", "workflows", limit=100
        )
        for item in result["items"]:
            if "metadata" in item and "status" in item:
                id = item["metadata"]["name"]
                (matches, found_name) = self._matches_name(id)
                if not matches:
                    continue
                started_at = datetime.strptime(
                    item["status"]["startedAt"], "%Y-%m-%dT%H:%M:%SZ"
                )
                if started_at > self.min_started_at:
                    run = FlowRun(id, data=item)
                    self.found.append(run)
                    self.patterns.pop(found_name, None)

    def has_found_all(self):
        return len(self.patterns) == 0


class FlowRunner:
    def __init__(self, flow):
        self.name = path.basename(flow)
        self.flow = flow
        self.creator = Command(["python", flow, "--quiet", "argo-workflows", "create"])
        self.starter = Command(["python", flow, "argo-workflows", "trigger"])

    def setup(self):
        self.creator.must()

    def run(self):
        output = self.starter.must()
        match = re.search("run-id argo-[a-z0-9\-\.]+", output)
        indices = match.span()
        match_text = output[indices[0] : indices[1]]
        id = match_text.split(" ")[-1].replace("argo-", "")
        return FlowRun(id)


class Command:
    def __init__(self, cmd):
        if type(cmd) == str:
            self.commands = cmd.split(" ")
        else:
            self.commands = cmd

    def execute(self, check=False):
        result = subprocess.run(
            self.commands,
            text=True,
            check=check,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
        )
        return result

    def must(self):
        result = self.execute(check=True)
        return result.stdout.strip()

    def should(self):
        return self.execute().returncode == 0
