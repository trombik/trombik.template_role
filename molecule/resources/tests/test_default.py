import pytest
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


def service_name(host):
    if host.system_info.distribution == 'freebsd':
        return 'syslogd'
    elif host.system_info.distribution == 'openbsd':
        return 'syslogd'
    elif host.system_info.distribution == 'ubuntu':
        return 'rsyslog'
    elif host.system_info.distribution == 'centos':
        return 'rsyslog'
    else:
        raise NameError('Unknown distribution')


def flags_file(host):
    if host.system_info.distribution == 'freebsd':
        return '/etc/rc.conf.d/syslogd'
    elif host.system_info.distribution == 'openbsd':
        return '/etc/rc.conf.local'
    elif host.system_info.distribution == 'ubuntu':
        return '/etc/default/rsyslog'
    elif host.system_info.distribution == 'centos':
        return '/etc/sysconfig/rsyslog'
    else:
        raise NameError('Unknown distribution')


def package_name(host):
    return 'tree'


def test_hosts_file(host):
    f = host.file(flags_file(host))
    assert f.is_file
    assert f.exists
    assert f.user == default_user(host)
    assert f.group == default_group(host)
    assert f.mode == 0o644


def test_package_is_installed(host):
    package = host.package(package_name(host))
    assert package.is_installed


def test_rcctl(host):
    if host.system_info.distribution != 'openbsd':
        return
    result = host.run('rcctl get syslogd flags')
    assert '-h' in result.stdout


def test_service(host):
    service = host.service(service_name(host))
    assert service.is_enabled
    if host.system_info.distribution == 'freebsd':
        with host.sudo():
            assert service.is_running
    else:
        assert service.is_running


def port_number(host):
    return 22


@pytest.mark.skip(reason="fails in docker")
def test_port(host):
    port = port_number(host)
    assert host.socket(f"tcp://{port}").is_listening
