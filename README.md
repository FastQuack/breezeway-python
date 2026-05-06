# Breezeway Python Client

A Python client library for communicating with Breezeway.io, providing an easy interface for managing authentication and
interacting with Breezeway's API.

## Installation

```sh
pip install breezeway
```

## Example Usage

```python
import breezeway

# Initialize the client
bw = breezeway.Breezeway(client_id='your_client_id', client_secret='your_client_secret')

# Get companies associated with the client
companies = bw.company.list_all()
for company in companies:
    print(company.name)

# Get task information
task = bw.task.get(task_id=12345)
print(
    bw.unit.get(unit_id=task.unit_id).title,
    task.status,
    task.title,
    task.description
)

# Upload an attachment
bw.task.upload_attachment(task_id=12345, file_path='path/to/file.jpg')
```

### Available as an async client too
```python
import breezeway
bw = breezeway.AsyncBreezeway(client_id='your_client_id', client_secret='your_client_secret')
```

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.

