# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import absolute_import, division, print_function

__metaclass__ = type
from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    """
    This callback module pretty-prints the host report for Fogo validator nodes.
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "aggregate"
    CALLBACK_NAME = "firstset.fogo_community.report"

    # only needed if you ship it and don't want to enable by default
    CALLBACK_NEEDS_ENABLED = True

    def v2_runner_on_ok(self, result):
        role = getattr(result._task, "_role", None)
        if (
            str(role) == "firstset.fogo_community.operations"
            and str(result.task_name) == "Set fact host_report"
        ):
            facts = result._result.get("ansible_facts", {})
            report = facts["host_report"]
            self._display.display(f"[{result._host.get_name()}] HOST REPORT:\n{report}")
        else:
            return
