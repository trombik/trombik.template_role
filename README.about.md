## `trombik.template_role`

A template for `ansible` role. The template is written for `sshd` server. You
can simply replace `template_role_*` variables and tasks with new role name
and what the new role does.

Without any modifications, the role can be tested on local machine, and in
`travis CI`. You do not have to write tests from scratch. Adjust the role and
the tests as you develop the role.

### Features

* A ready-to-test role. Tests includes: `yamlint`for YAML files, `rubocop` for
  `ruby` files, `serverspec` for unit tests, and `molecule` for integration tests.
* Supports CI in `travis CI` for linting and integration tests using `docker`
* Supported Virtualisations: `virtualbox` for `serverspec` and `molecule`,
  `virtualbox` and `docker` for `molecule`
* Supported OS platforms include: FreeBSD, OpenBSD, Ubuntu, and CentOS
* Tests scenarios in `travis CI` run in parallel

### Implementations

#### Unit tests and integration tests

A unit test is defined here as "a test that examines every task in the role".
In a unit test, the test will see every details of converged states in VMs.
Files, services, and other resources are tested in unit tests. Unit tests are
expected not to change the state of VMs, i.e. repeated tests produce same
results.

Unit tests are located under [`tests/serverspec`](tests/serverspec).

An integration test is defined as "a test that expects certain results after
conversion and, optionally, side effects. Unlike unit tests, expected
outcomes are tested in integration tests. Examples are: fail-over in a
cluster, and message delivery from a client to a server.

In this role template, `test-kitchen`, `kitchen-vagrant`, and `serverspec` are
used for unit tests.

`molecule`, `vagrant`, and `testinfra` are used for integration tests.

Integration tests are located under [`tests/molecule`](tests/molecule).

## Requirements

TBW

## LICENSE

```
Copyright (c) 2019 Tomoyuki Sakurai <y@trombik.org>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```
