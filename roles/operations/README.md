# Fogo Validator Node Operations

Common operations for Fogo validator nodes, such as checking key services running status, binaries versions, latest logs, etc.

## Requirements

Target nodes should be Ubuntu/Debian-based systems with sudo access.

## Role Variables

All variables which can be overridden are stored in `defaults/main.yml`.

### systemd_services_to_check

List of systemd services to check status and logs for.

Default:

```yaml
systemd_services_to_check:
  - fail2ban
  - node_exporter
  - fogo-validator
```

### binaries_to_check

Dictionary of binaries to check versions for, including their path and version command option.

Default:

```yaml
binaries_to_check:
  fdctl:
    path: /usr/local/bin/fdctl
    option: version
```

## Examples

### Check fleet status and generate reports

This role generates detailed reports about the status of key services and binaries on Fogo validator nodes.

```yml
- name: Generate Validator Nodes Report
  hosts: validators
  become: true
  gather_facts: false

  tasks:
    - name: Generate Validator Nodes Report
      include_role:
        name: firstset.fogo_community.operations
        tasks_from: check_fleet.yml
```

The role will check:

- Systemd service status (active state and unit file state)
- Recent log entries (last 10 lines) for each service
- Binary versions for key executables
- Kernel version

The report for each Fogo validator node is set as a fact named `host_report`. There are several approaches to get the content of the report.

#### use the report plugin

This collection also ships a plugin called `firstset.fogo_community.report` that helps pretty-print the Fogo validator node report. To enable it, add the following into your `ansible.cfg` file in your playbooks folder:

```
[defaults]
callbacks_enabled = firstset.fogo_community.report
```

By doing this, everytime when the tasks in `check_fleet.yml` are executed and the fact `host_report` is set successfully, the report will be printed to the console in a human-readable format.

#### use the debug module

You can also output the report using the Ansible `debug` module:

```yml
- name: Output report
  debug:
    msg: "{{ host_report.split('\n') }}"
```

#### dump the report to a file

```yml
- name: Output report to a file
  become: false
  copy:
    content: "{{ host_report }}"
    dest: "./host_report_{{ inventory_hostname }}.txt"
  delegate_to: localhost
```

### Custom service and binary checks

You can override the default services and binaries to check:

```yml
- name: Custom Fleet Check
  hosts: validators
  become: true
  vars:
    systemd_services_to_check:
      - fogo-validator
      - prometheus
      - grafana
    binaries_to_check:
      fdctl:
        path: /usr/local/bin/fdctl
        option: version
      prometheus:
        path: /usr/local/bin/prometheus
        option: --version

  roles:
    - firstset.fogo_community.operations
```

## License

MIT

## Author Information

<https://www.firstset.xyz/>
