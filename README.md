## `trombik.template_role`

`ansible` role for `template_role`.

## Requirements

## Role Variables

## Dependencies

## Example Playbook

```yaml
---
- name: Converge
  hosts: all
  roles:
    - role: trombik.template_role
  pre_tasks:
    - name: Dump all hostvars
      debug:
        var: hostvars[inventory_hostname]
    - name: List all services (systemd)
      # workaround ansible-lint: [303] service used in place of service module
      shell: "echo; systemctl list-units --type service"
      changed_when: false
      when:
        # in docker, init is not systemd
        - ansible_virtualization_type != 'docker'
        - ansible_os_family == 'RedHat' or ansible_os_family == 'Debian'
    - name: list all services (FreeBSD service)
      # workaround ansible-lint: [303] service used in place of service module
      shell: "echo; service -l"
      changed_when: false
      when:
        - ansible_os_family == 'FreeBSD'
    - name: list all services (rcctl)
      command: "rcctl ls all"
      changed_when: false
      when:
        - ansible_os_family == 'OpenBSD'


  vars:
    os_template_role_flags:
      OpenBSD: -4
      FreeBSD: ""
      Debian: ""
      RedHat: ""
    os_port:
      OpenBSD: 10022
      FreeBSD: 10022
      Debian: 10022
      RedHat: 22
    template_role_flags: "{{ os_template_role_flags[ansible_os_family] }}"
    template_role_extra_groups:
      - bin
    # on RedHat, non-default port is not allowed to listen on
    # on FreeBSD, sshd from the base and one from the package are both running
    template_role_config: |
      UseDNS no
      Port {{ os_port[ansible_os_family] }}
      {% if ansible_os_family != 'FreeBSD' and ansible_os_family != 'RedHat' %}
      Port 22
      {% endif %}
```

## License

## Author Information
