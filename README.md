# FOGO Community Ansible Collection

[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-firstset.fogo__community-blue.svg)](https://galaxy.ansible.com/ui/repo/published/firstset/fogo_community/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An Ansible collection that provides automated deployment and management tools for FOGO validators. This collection simplifies the process of setting up, configuring, and maintaining FOGO validator nodes.

## Overview

FOGO is a Solana validator client built on Firedancer, designed for high performance and reliability. This Ansible collection automates the deployment process, making it easier for validators to maintain their nodes with best practices and consistent configurations.

## Features

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
ansible-playbook -i inventory site.yml --ask-become-pass
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

## Configuration

All configurable variables are documented in [`roles/validator_service/defaults/main.yml`](roles/validator_service/defaults/main.yml). Key variables include:

| Variable | Default | Description |
|----------|---------|-------------|
| `validator_client_version` | `v6.0.0` | FOGO release version to install |
| `validator_client_tarfile_checksum` | `817533105183734d5f4dffb4f0b11b0de2adf38b` | The SHA1 checksum of the source code tar file provided by FOGO [here](https://docs.fogo.io/releases.html) |
| `service_user` | `fogo` | System user for the validator service |
| `firedancer_gossip_port` | `8001` | Port for gossip network communication |
| `bootstrap_disks` | `false` | Whether to detect and format additional disks |
| `upgrade_only` | `false` | Only upgrade binaries without full setup |

## Common Usage Patterns

### Initial Deployment

```bash
# Full setup including disk bootstrapping
ansible-playbook site.yml -e "bootstrap_disks=true" --ask-become-pass
```

### Binary Upgrades

```bash
# Upgrade to new version
ansible-playbook site.yml -e "upgrade_only=true validator_client_version=v6.1.0 validator_client_tarfile_checksum=817533105183734d5f4dffb4f0b11b0de2adf38b" --ask-become-pass
```

## Repository Structure

```
├── roles/
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