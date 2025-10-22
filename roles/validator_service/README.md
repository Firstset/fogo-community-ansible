# Fogo Validator

Deploy Fogo validator to target nodes.

## Requirements

Target nodes should meet the requirements mentioned on Fogo's [official documentation page](https://docs.fogo.io/running-a-node.html).

## Role Variables

All variables which can be overridden are stored in `defaults/main.yml`. Please also check the Firedancer config template and its systemd definition file in the `templates` folder.

## Examples

### Setup a validator node including the following tasks

- Enable CPU performance mode if available
- Kernel parameter tuning (sysctl)
- Network ring buffer adjustment
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
+    # use v18.0.0 as an example here
+    validator_client_version: v18.0.0
+    validator_client_tarfile_checksum: 3bfaa77791659f985dcfa274999fac23906bf3e9

  roles:
    - firstset.fogo_community.validator_service
```

Then specify the tag `update_binary` when you run the playbook:

```bash
ansible-playbook -i inventory/fogo.yml playbooks/fogo.yml --ask-become-pass -t update_binary
```

#### Configure the Binaries to Be Built

By default, the role builds three binaries: `fdctl`, `solana`, and `agave-ledger-tool`. This can be configured with `fogo_binaries_to_build`, for example:

```yaml
# build and update fdctl only
fogo_binaries_to_build:
  - fdctl
```

#### Build Binaries in One Host and Push to Other Nodes

By default, each host does the same tasks for updating the binaries: 1) fetching the source code bundle, 2) run `./deps.sh`, 3) run `make -j ...`, and 4) replacing the binaries and restarting the service if `fdctl` needs to be updated.

This can be an issue if one wants to upgrade `fdctl` in an active validator node because building the binaries takes time and consumes CPU and memory resources, which will most likely makes the validator delinquent for some time. To address this, there is another mode for updating the binaries in this role: `fogo_binaries_build_mode: push`. When it is configured like this, the role pushes the binaries from the controller node to each host, and the binaries can be prepared using the following playbook:

```yaml
---
- name: Build fogo artifacts and pull them to localhost
  hosts: <the_host_you_would_like_to_build_the_binaries>
  vars:
    validator_client_version: v18.0.0
    validator_client_tarfile_checksum: 3bfaa77791659f985dcfa274999fac23906bf3e9
    fogo_binaries_to_build:
      - fdctl
      - solana
      - agave-ledger-tool

  tasks:
    - name: Build artifacts in the remote host
      include_role:
        name: firstset.fogo_community.validator_service
        tasks_from: fogo_build_and_fetch_artifacts.yml
      tags: always # this guarantees that the task is always included
```

The playbook builds the binaries in the target host and then fetches the artifacts to the controller node under `<playbooks_folder>/fogo_artifacts` (can be configured with `fogo_binaries_local_path`). If the binaries are already built and available at `/home/{{ service_user }}/fogo-{{ validator_client_version }}/fogo/build/native/gcc/bin`, the playbook can be executed with a tag filter `-t fetch_only`.

Then run the following command to update the binaries in target hosts:

```bash
ansible-playbook -i inventory/fogo.yml playbooks/fogo.yml --ask-become-pass -t update_binary -e "fogo_binaries_build_mode=push"
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
