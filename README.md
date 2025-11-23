# Ansible Role: Telegraf

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
