# Fogo Validator

Deploy Fogo validator to target nodes.

## Requirements

Target nodes should meet the requirements mentioned on Fogo's [official documentation page](https://docs.fogo.io/running-a-node.html).

## Role Variables

All variables which can be overridden are stored in `defaults/main.yml`. Please also check the Firedancer config template and its systemd definition file in the `templates` folder.

## Example Playbook

```yml
- name: Setup Fogo Validator Node
  hosts: all
  become: true

  roles:
    - fogo_validator
```

By default `bootstrap_disks` is set to `false` as this step is supposed to be executed only once. If you would like to detect the additional disks and format them for a Fogo validator, you can set `bootstrap_disks` to `true` by:

```bash
ansible-playbook -i inventory/fogo.yml playbooks/fogo.yml --ask-become-pass -e "bootstrap_disks=true"
```

## License

MIT

## Author Information

<https://www.firstset.xyz/>
