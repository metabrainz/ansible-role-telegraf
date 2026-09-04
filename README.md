# Ansible Role: Telegraf

Ansible role for installing and configuring Telegraf, the plugin-driven server agent for collecting and sending metrics.

## Usage

### Basic Configuration

Define Telegraf configuration using Ansible variables. The role supports inputs, outputs, processors, and aggregators.

#### Simple Example

Telegraf config:
```toml
[[inputs.cpu]]
  percpu = false
  totalcpu = true
```

Ansible equivalent:
```yaml
telegraf_group_inputs:
  cpu:
    percpu: false
    totalcpu: true
```

#### Repeated Sections

Telegraf config:
```toml
[[inputs.postgresql]]
  address = "host=db1.example.com user=telegraf database=postgres"

[[inputs.postgresql]]
  address = "host=db2.example.com user=telegraf database=postgres"
```

Ansible equivalent:
```yaml
telegraf_group_inputs:
  postgresql:
    - address: "host=db1.example.com user=telegraf database=postgres"
    - address: "host=db2.example.com user=telegraf database=postgres"
```

#### Nested Sections

Telegraf config:
```toml
[[inputs.http]]
  urls = ["http://api.example.com/metrics"]

  [inputs.http.json_v2]
    measurement_name = "api_metrics"

    [[inputs.http.json_v2.object]]
      path = "data"
      tags = ["environment"]
```

Ansible equivalent:
```yaml
telegraf_group_inputs:
  http:
    urls:
      - "http://api.example.com/metrics"
    json_v2:
      measurement_name: "api_metrics"
      object:
        - path: "data"
          tags:
            - "environment"
```

### Group and Host Variables

Use Ansible's variable precedence to override configurations:

```yaml
# group_vars/all.yml - applies to all hosts
telegraf_group_inputs:
  cpu:
    percpu: false

# group_vars/webservers.yml - applies to webservers group
telegraf_group_inputs:
  nginx:
    urls: ["http://localhost/status"]

# host_vars/web01.yml - applies to specific host
telegraf_host_inputs:
  disk:
    mount_points: ["/", "/data"]
```

The role merges `telegraf_group_*` and `telegraf_host_*` variables, with host variables taking precedence.

#### Hosts in multiple groups

A single `telegraf_group_inputs` (or `_outputs`/`_processors`/`_tags`/`_sudo_commands`) is resolved by
Ansible from only **one** group per host, so a host belonging to two groups that each define it would
silently lose one group's config. To contribute config from **every** group a host is in, use a
per-group variable suffixed with the group name:

```yaml
# group_vars/gw_servers.yml
telegraf_group_inputs__gw_servers:
  haproxy:
    servers: ["/run/haproxy/*.sock"]

# group_vars/consul_agents.yml
telegraf_group_inputs__consul_agents:
  consul:
    address: "127.0.0.1:8500"
```

A host in both `gw_servers` and `consul_agents` then gets **both** the `haproxy` and `consul` inputs.
The role folds `telegraf_group_<section>__<group>` across all of the host's groups. The legacy single
`telegraf_group_<section>` variable is still honoured (merged first), so existing inventories keep
working. Precedence (last wins): base defaults → `telegraf_group_<section>` → per-group
`telegraf_group_<section>__<group>` → `telegraf_host_<section>`.

### Version Pinning

To install a specific version of Telegraf, set the `telegraf_version` variable:

```yaml
telegraf_version: "1.36.3-1"
```

If not set, the latest available version will be installed.

## Testing

### Prerequisites

- Docker installed and running
- Python 3.11 (or Python 3.10)
- User must have Docker permissions

### Setup

1. **Install Docker** (if not already installed):
```bash
sudo apt-get install docker.io  # Debian/Ubuntu
# or
sudo yum install docker  # RHEL/CentOS
```

2. **Start Docker and enable it**:
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

3. **Add your user to the docker group**:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

4. **Create a virtual environment and install tox**:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install tox
```

### Running Tests

Run all test environments:
```bash
tox
```

Run a specific test environment:
```bash
tox -e py311-ansible7
```

Available test environments:
- `py310-ansible5`, `py310-ansible6`, `py310-ansible7`
- `py311-ansible5`, `py311-ansible6`, `py311-ansible7`

### Test Environment Variables

You can customize the test environment:

```bash
# Use a different distro (default: ubuntu2004)
MOLECULE_DISTRO=ubuntu2204 tox

# Use a different playbook
MOLECULE_PLAYBOOK=custom.yml tox
```

### Modifying the Test Matrix

To add or remove Python/Ansible versions, edit `tox.ini`:

**Add a new version:**
```ini
[tox]
envlist = py{310,311,312}-ansible{5,6,7,8}  # Add py312 and ansible8
```

**Add dependencies for new Ansible version:**
```ini
[testenv]
deps =
    ansible5: ansible == 5.*
    ansible6: ansible == 6.*
    ansible7: ansible == 7.*
    ansible8: ansible == 8.*  # Add new version
```

**Remove a version:**
Simply remove it from the `envlist` (e.g., remove `py310` or `ansible5`).

### Updating Tests After Template Changes

When you modify the Telegraf configuration template or add new features, update the test files:

1. **Update test variables** in `molecule/default/inventory/group_vars/all.yml`:
```yaml
telegraf_group_inputs:
  cpu:
    collect_cpu_time: true
    percpu: false
```

2. **Update expected output** in `molecule/default/files/telegraf.conf`:
```
[[inputs.cpu]]
  collect_cpu_time = true
  percpu = false
```

3. **Run tests** to verify:
```bash
tox -e py311-ansible7
```
