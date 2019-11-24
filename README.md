## `trombik.template_role`

A template for `ansible` role.

### Features

* A ready-to-test role. Tests includes: `yamlint`for YAML files, `rubocop` for
  `ruby` files, `serverspec` for unit tests, and `molecule` for integration tests.
* Supports CI in `travis CI`
* Supported Virtualisations: `virtualbox` for `serverspec` and `molecule`,
  `docker` for `molecule`.`
* Supported OS platforms inlcude: FreeBSD, OpenBSD, Ubuntu, and CentOS
