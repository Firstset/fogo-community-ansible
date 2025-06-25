# FOGO Community Ansible Collection

[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-firstset.fogo__community-blue.svg)](https://galaxy.ansible.com/ui/repo/published/firstset/fogo_community/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An Ansible collection that provides automated deployment and management tools for FOGO validators. This collection simplifies the process of setting up, configuring, and maintaining FOGO validator nodes.

## Overview

FOGO is a Solana validator client built on Firedancer, designed for high performance and reliability. This Ansible collection automates the deployment process, making it easier for validators to maintain their nodes with best practices and consistent configurations.

## Features

### Node bootstrapping

- **SSH security hardening** - Creates sudo users with key authentication and disables root/password login
- **Enhanced security configuration** - Changes default SSH port and configures fail2ban for intrusion prevention
- **Firewall management** - Sets up UFW with default deny policy and security rules
- **Monitoring integration** - Installs Prometheus node exporter with server whitelisting

### Validator service deployment

- **Automated validator deployment** - Complete setup from system configuration to service deployment
- **Performance optimization** - CPU performance mode configuration and system tuning
- **Security hardening** - UFW firewall configuration and service user management
- **Disk management** - Automatic detection and formatting of additional storage disks
- **Binary management** - Automated building and upgrading of Firedancer binaries
- **Configuration templating** - Flexible Firedancer configuration with sensible defaults
- **Service management** - Systemd service creation and lifecycle management

## Requirements

- **Ansible**: >= 2.9
- **Target OS**: Ubuntu 20.04+ or Debian 11+
- **Hardware**: Meets [FOGO's official requirements](https://docs.fogo.io/running-a-node.html)
- **Network**: Open ports for gossip (8001) and dynamic port range (8901-9000)

## Installation

Install from Ansible Galaxy:

```bash
ansible-galaxy collection install firstset.fogo_community
```

Or install from source:

```bash
git clone https://github.com/Firstset/fogo-community-ansible.git
cd fogo-community-ansible
ansible-galaxy collection build
ansible-galaxy collection install firstset-fogo_community-*.tar.gz
```

## Quick Start

### Node Bootstrapping

Create a playbook to bootstrap the node, including sudo user creation, SSH hardening, Node Exporter installation, and firewall setup:

```yaml
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

Run the playbook:

```bash
ansible-playbook -i inventory bootstrap-node.yml --ask-become-pass
```

In this example, we change the SSH port to `156`, so don't forget to update your SSH client configuration accordingly. The `prometheus_node_ip` should be set to the IP address of your Prometheus server for metrics collection.

### Basic Validator Setup

Create a playbook to deploy a FOGO validator:

```yaml
---
- name: Deploy FOGO Validator
  hosts: validator_nodes
  become: true
  roles:
    - firstset.fogo_community.validator_service
```

Run the playbook:

```bash
ansible-playbook -i inventory deploy-service.yml --ask-become-pass
```

### Advanced Configuration

Override default settings by setting variables:

```yaml
---
- name: Deploy FOGO Validator with Custom Config
  hosts: validator_nodes
  become: true
  vars:
    validator_client_version: v6.0.0
    validator_client_tarfile_checksum: 817533105183734d5f4dffb4f0b11b0de2adf38b
    firedancer_gossip_port: 8001
    accounts_path: "/fast-storage/accounts"
    bootstrap_disks: true
  roles:
    - firstset.fogo_community.validator_service
```

## Included Roles

### `node_bootstrapping`

The main role for bootstrapping a FOGO validator node. See the [role documentation](roles/node_bootstrapping/README.md) for detailed configuration options and examples.

**Key tasks performed:**

- Sudo user creation with SSH key authentication
- SSH security hardening (disable root/password login)
- SSH port configuration for enhanced security
- Fail2ban installation and configuration
- UFW firewall setup with default deny policy
- Prometheus node exporter installation
- Network security rules and monitoring integration

**Role variables:**

| Variable             | Default | Description                                                   |
| -------------------- | ------- | ------------------------------------------------------------- |
| `prometheus_node_ip` | `null`  | IP address of the Prometheus server to whitelist for metrics  |
| `enable_ufw`         | `false` | Whether to enable UFW firewall after configuration            |
| `ssh_port_number`    | `156`   | SSH port to use instead of default port 22                    |
| `sudo_users`         | `{}`    | Dictionary of sudo users to create with their SSH public keys |

### `validator_service`

The main role for deploying and managing FOGO validators. See the [role documentation](roles/validator_service/README.md) for detailed configuration options and examples.

**Key tasks performed:**

- System dependencies installation
- Optional disk bootstrapping and formatting
- CPU performance mode configuration
- UFW firewall setup
- Service user creation
- Firedancer binary compilation
- Configuration file generation
- Systemd service setup and activation

All configurable variables are documented in [`roles/validator_service/defaults/main.yml`](roles/validator_service/defaults/main.yml). Key variables include:

| Variable                            | Default                                    | Description                                                                                               |
| ----------------------------------- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| `validator_client_version`          | `v7.0.0`                                   | FOGO release version to install                                                                           |
| `validator_client_tarfile_checksum` | `7d2ca6e4e47bf31ffd1c4e04634895acd820984d` | The SHA1 checksum of the source code tar file provided by FOGO [here](https://docs.fogo.io/releases.html) |
| `service_user`                      | `fogo`                                     | System user for the validator service                                                                     |
| `firedancer_gossip_port`            | `8001`                                     | Port for gossip network communication                                                                     |
| `bootstrap_disks`                   | `false`                                    | Whether to detect and format additional disks                                                             |

The role also provides two tags `update_binary` and `update_config` for filtering the tasks during execution. Use these tags to update the Firedancer binary or configuration without re-running the entire playbook. Check the common use cases below.

#### Common Usage Patterns

##### Initial Deployment

```bash
# Full setup including disk bootstrapping
ansible-playbook site.yml -e "bootstrap_disks=true" --ask-become-pass
```

##### Binary Upgrades

```bash
# Upgrade to new version
ansible-playbook site.yml -t update_binary -e "validator_client_version=v7.0.0 validator_client_tarfile_checksum=7d2ca6e4e47bf31ffd1c4e04634895acd820984d" --ask-become-pass
```

##### Config Updates

The role already includes a FOGO firedancer config template that you can find in `templates/firedancer_config_template.toml.j2`. If you need to override the config, first create your own template file and set the variable `firedancer_config_template_path` to point to your custom template. For example:

```yaml
- name: Deploy FOGO Validator
  hosts: validator_nodes
  become: true
  vars:
    firedancer_config_template_path: "./templates/my_fogo_service_config.toml.j2"
  roles:
    - firstset.fogo_community.validator_service
```

Then the following command can be used for only updating the configuration file and restarting the service:

```bash
ansible-playbook site.yml -t update_config --ask-become-pass
```

## Repository Structure

```
├── roles/
│   ├── node_bootstrapping/    # Node bootstrapping role
│   └── validator_service/     # Main validator deployment role
├── galaxy.yml                 # Collection metadata
├── LICENSE                    # MIT license
└── README.md                 # This file
```

## Contributing

We welcome contributions! Please feel free to:

- Report bugs or request features via [GitHub Issues](https://github.com/Firstset/fogo-community-ansible/issues)
- Submit pull requests for improvements
- Share your validator configurations and best practices

## Support

- **Documentation**: [Ansible Galaxy Docs](https://galaxy.ansible.com/ui/repo/published/firstset/fogo_community/docs/)
- **Issues**: [GitHub Issues](https://github.com/Firstset/fogo-community-ansible/issues)
- **FOGO Documentation**: [docs.fogo.io](https://docs.fogo.io/)

## License

This collection is licensed under the [MIT License](LICENSE).
