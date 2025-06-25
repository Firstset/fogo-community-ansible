# Fogo Validator

Deploy Fogo validator to target nodes.

## Requirements

Target nodes should meet the requirements mentioned on Fogo's [official documentation page](https://docs.fogo.io/running-a-node.html).

## Role Variables

All variables which can be overridden are stored in `defaults/main.yml`. Please also check the Firedancer config template and its systemd definition file in the `templates` folder.

## Examples

### Setup a validator node including the following tasks

- Enable CPU performance mode if available
- Update UFW settings
- Create a service user (username `fogo` by default)
- Fetch Fogo release and build Firedancer binary
- Generate Firedancer config and systemd service file
- Enable and start the Fogo validator service

```yml
- name: Setup Fogo Validator Node
  hosts: all
  become: true

  roles:
    - firstset.fogo_community.validator_service
```

By default `bootstrap_disks` is set to `false` as this step is supposed to be executed only once. If you would like to detect the additional disks and format them for a Fogo validator, you can set `bootstrap_disks` to `true` by:

```bash
ansible-playbook -i inventory/fogo.yml playbooks/fogo.yml --ask-become-pass -e "bootstrap_disks=true"
```

### Upgrade Fogo Firedancer binary

Building Firedancer binary is included by default. The version and the release checksum are defined by `validator_client_version` and `validator_client_tarfile_checksum`. If there is a new version available, you can override these variables in your playbook or inventory file:

```diff
- name: Setup Fogo Validator Node
  hosts: all
  become: true
+  vars:
+    # use v7.0.0 as an example here
+    validator_client_version: v7.0.0
+    validator_client_tarfile_checksum: 7d2ca6e4e47bf31ffd1c4e04634895acd820984d

  roles:
    - firstset.fogo_community.validator_service
```

Then specify the tag `update_binary` when you run the playbook:

```bash
ansible-playbook -i inventory/fogo.yml playbooks/fogo.yml --ask-become-pass -t update_binary
```

### Update FOGO Firedancer Configuration

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

The tag `update_config` also works for overriding the systemd definition file. The corresponding variable is `firedancer_systemd_template_path` which defaults to `templates/firedancer_systemd.j2`.

## License

MIT

## Author Information

<https://www.firstset.xyz/>
