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

### Basic setup with minimal configuration

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
