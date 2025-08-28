# Fogo Validator Node Bootstrapping

Bootstrap and harden Fogo validator nodes with security configurations, monitoring, and user management.

## Requirements

Target nodes should be Ubuntu/Debian-based systems with sudo access.

## Role Variables

All variables which can be overridden are stored in `defaults/main.yml`.

### Default Variables

- `prometheus_node_ip`: IP address of the Prometheus server to whitelist for metrics scraping (default: `null`)
- `enable_ufw`: Whether to enable UFW firewall after configuration (default: `false`)
- `ssh_port_number`: SSH port to use instead of default port 22 (default: `156`)
- `sudo_users`: Dictionary of sudo users to create with their SSH public keys

## Dependencies

- prometheus.prometheus: <https://galaxy.ansible.com/ui/repo/published/prometheus/prometheus/>

## Examples

### Bootstrap a validator node with security hardening

This role performs the following tasks:

- Creates sudo users with SSH key authentication
- Configures SSH security (disables root login, password authentication)
- Changes SSH port for enhanced security
- Installs and configures fail2ban for intrusion prevention
- Sets up UFW firewall with default deny policy
- Installs Prometheus node exporter for monitoring
- Whitelists Prometheus server for metrics collection

Here's an example for a playbook that uses this role:

```yml
- name: Bootstrap Fogo Validator Node
  hosts: all
  become: true
  vars:
    sudo_users:
      admin1: "ssh-rsa AAAAB3NzaC1yc2E... user1@example.com"
      admin2: "ssh-rsa AAAAB3NzaC1yc2E... user2@example.com"
    prometheus_node_ip: "10.0.1.100"
    enable_ufw: true
    ssh_port_number: 156

  roles:
    - firstset.fogo_community.node_bootstrapping
```

### Important Notes Regarding SSH

Please be aware that, with the current implementation, after executing the `node_bootstrapping` tasks, SSH using a password will be disabled. SSH using the root user is disabled as well while this can be configured with `disallow_root_login: false/true`. If there is at least one sudo user configured using `sudo_users`, the role also configures SSH to only allow the connection from these users by default. Blocking non-managed sudo users can be disabled by setting `block_non_managed_sudo_users` to `false`.

Considering there can be multiple sudo users to be created and the operator may not want to input the password for each user, the role generates a one-time, expired password for each user. It is possible to set the one-time password using `-e "sudo_user_activation_password=<activation_password>"`. This password is logged in the Ansible output, so please make sure to capture it during the playbook execution if it is not set via `sudo_user_activation_password`. A sudo user can use this password for the initial login and then change it immediately after logging in.

Here is an example of the relevant log output:

```
TASK [firstset.fogo_community.node_bootstrapping : Send the following one-time password to the user <username>, which is needed for creating the real password] ***********************************************
ok: [some-node-name] => {
    "msg": "some-password"
}
```

If there are several hosts included in the execution, the random password for a user will be reused for all of the hosts.

### Basic setup with minimal configuration

Or the simplest playbook:

```yml
- name: Basic Node Bootstrapping
  hosts: all
  become: true

  roles:
    - firstset.fogo_community.node_bootstrapping
```

### Enable UFW firewall after configuration

By default, UFW rules are configured but UFW remains disabled. To enable UFW after setup, either specify it in the inventory/playbook, or use the following command:

```bash
ansible-playbook -i inventory/fogo.yml playbooks/bootstrap.yml --ask-become-pass -e "enable_ufw=true"
```

## License

MIT

## Author Information

<https://www.firstset.xyz/>
