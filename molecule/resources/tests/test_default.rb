default_user = 'root'
default_group = 'root'
service_name = 'sshd'
package_name = 'tree'
flags_file = ''
flags_patterns = []

case os.name
when 'ubuntu'
  flags_file = '/etc/default/rsyslog'
  flags_patterns = [/Managed by ansible/]
when 'freebsd'
  flags_file = '/etc/rc.conf.d/syslogd'
  default_group = 'wheel'
  flags_patterns = [/Managed by ansible/]
when 'openbsd'
  flags_file = '/etc/rc.conf.local'
  flags_patterns = [/syslogd_flags=-h/]
  default_group = 'wheel'
when 'centos'
  flags_file = '/etc/sysconfig/rsyslog'
  flags_patterns = [/Managed by ansible/]
end

describe file '/etc/hosts' do
  it { should exist }
  its('owner') { should eq default_user }
  its('group') { should eq default_group }
  its('mode') { should cmp '0644' }
end

describe package package_name do
  it { should be_installed }
end

describe file flags_file do
  it { should exist }
  its('owner') { should eq default_user }
  its('group') { should eq default_group }
  its('mode') { should cmp '0644' }
  flags_patterns.each do |p|
    its('content') { should match p }
  end
end

if os.name == 'openbsd'
  describe command 'rcctl get syslogd flags' do
    its('exit_status') { should eq 0 }
    its('stderr') { should eq '' }
    its('stdout') { should match(/-h/) }
  end
end

describe service service_name do
  it { should be_enabled }
  it { should be_running }
end
