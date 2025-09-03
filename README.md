![Vemetric Python SDK](https://github.com/user-attachments/assets/4709b219-c0d7-42a8-8a5a-e0801f1ce69a)

# The Vemetric SDK for Python

Learn more about the Vemetric Python SDK in the [official docs](https://vemetric.com/docs/sdks/python).

You can also checkout the package on [PyPI](https://pypi.org/project/vemetric).

[![PyPI - Version](https://img.shields.io/pypi/v/vemetric)](https://pypi.org/project/vemetric)

## Installation

```bash
pip install vemetric
```

## Usage

```python
from vemetric import VemetricClient

vemetricClient = VemetricClient(token="YOUR_PROJECT_TOKEN")

vemetricClient.track_event(
  "SignupCompleted",
  user_identifier="user-id",
  user_display_name="John Doe",
  event_data={"key": "value"},
)

vemetricClient.update_user(
  "user-id",
  user_data={
    "set": {"key1": "value1"},
    "setOnce": {"key2": "value2"},
    "unset": ["key3"]
  },
)
```

## Configuration

The client can be configured with the following options:

```python
vemetricClient = VemetricClient(
  token="YOUR_PROJECT_TOKEN", # Required
  host="https://hub.vemetric.com", # Optional, defaults to https://hub.vemetric.com
  timeout=2.0, # Optional, default to 2 seconds
  session=requests.Session(), # Optional, defaults to None, creating a new one
)
```
