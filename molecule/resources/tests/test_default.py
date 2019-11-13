# import pytest
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def default_group(host):
    if host.system_info.distribution == 'freebsd' or \
            host.system_info.distribution == 'openbsd':
        return 'wheel'
    return 'root'


def default_user(host):
    return 'root'


def user_name(host):
    if host.system_info.distribution == 'freebsd':
        return 'sshd'
    elif host.system_info.distribution == 'openbsd':
        return 'sshd'
    elif host.system_info.distribution == 'ubuntu':
        return 'sshd'
    elif host.system_info.distribution == 'centos':
        return 'sshd'
    else:
        raise NameError('Unknown distribution')


def group_name(host):
    if host.system_info.distribution == 'freebsd':
        return 'sshd'
    elif host.system_info.distribution == 'openbsd':
        return 'sshd'
    elif host.system_info.distribution == 'ubuntu':
        return 'nogroup'
    elif host.system_info.distribution == 'centos':
        return 'sshd'
    else:
        raise NameError('Unknown distribution')


def port_number(host):
    if host.system_info.distribution == 'centos':
        return 22
    return 10022


def service_name(host):
    if host.system_info.distribution == 'freebsd':
        return 'openssh'
    elif host.system_info.distribution == 'openbsd':
        return 'sshd'
    elif host.system_info.distribution == 'ubuntu':
        return 'ssh'
    elif host.system_info.distribution == 'centos':
        return 'sshd'
    else:
        raise NameError('Unknown distribution')


def config_file(host):
    if host.system_info.distribution == 'freebsd':
        return '/usr/local/etc/ssh/sshd_config'
    else:
        return '/etc/ssh/sshd_config'


def log_dir(host):
    return '/var/log/template_role'


def flags_file(host):
    if host.system_info.distribution == 'freebsd':
        return '/etc/rc.conf.d/openssh'
    elif host.system_info.distribution == 'openbsd':
        return '/etc/rc.conf.local'
    elif host.system_info.distribution == 'ubuntu':
        return '/etc/default/sshd'
    elif host.system_info.distribution == 'centos':
        return '/etc/sysconfig/sshd'
    else:
        raise NameError('Unknown distribution')


def package_name(host):
    if host.system_info.distribution == 'freebsd':
        return 'security/openssh-portable'
    elif host.system_info.distribution == 'openbsd':
        return None
    elif host.system_info.distribution == 'ubuntu':
        return 'openssh-server'
    elif host.system_info.distribution == 'centos':
        return 'openssh-server'
    else:
        raise NameError('Unknown distribution')


def test_config_file(host):
    f = host.file(config_file(host))
    assert f.is_file
    assert f.exists
    assert f.user == default_user(host)
    assert f.group == default_group(host)
    if host.system_info.distribution == 'centos':
        assert f.mode == 0o600
    else:
        assert f.mode == 0o644
    if host.system_info.distribution == 'centos':
        with host.sudo():
            assert f.contains('Managed by ansible')
    else:
        assert f.contains('UseDNS no')


def test_package_is_installed(host):
    if package_name(host) is None:
        return
    package = host.package(package_name(host))
    assert package.is_installed


def test_rcctl(host):
    if host.system_info.distribution != 'openbsd':
        return
    result = host.run('rcctl get sshd flags')
    assert '-4' in result.stdout


def test_group(host):
    assert host.group(group_name(host)).exists


def test_user(host):
    assert host.user(user_name(host)).name
    assert host.user(user_name(host)).group == group_name(host)


def test_log_dir(host):
    d = host.file(log_dir(host))
    assert d.is_directory
    assert d.user == user_name(host)
    assert d.group == group_name(host)
    assert d.group == group_name(host)
    assert d.mode == 0o755


def test_service(host):
    service = host.service(service_name(host))
    assert service.is_enabled
    assert service.is_running


def test_port(host):
    port = port_number(host)
    # XXX does not work on OpenBSD 6.3
    if host.system_info.distribution != 'openbsd':
        assert host.socket(f"tcp://{port}").is_listening
