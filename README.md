# Minimalist interLink Plugin

A minimal implementation of an interLink plugin that demonstrates the basic structure and API endpoints required for interLink integration. This plugin echoes all requests to stdout and returns minimal valid responses.

## Purpose

This plugin serves as:
- **Educational reference** for understanding the interLink plugin API
- **Testing tool** for debugging interLink core communication
- **Starting template** for building custom plugins

## Features

- ✅ Implements all required interLink plugin endpoints (`/create`, `/delete`, `/status`, `/getLogs`)
- ✅ Uses the official `interlink-plugin-sdk` Python package for type safety
- ✅ Pretty-prints all incoming requests to stdout for debugging
- ✅ Returns minimal valid responses to satisfy the interLink API contract
- ✅ Built with FastAPI for modern async Python web framework

## Requirements

- **Python 3.11+** (required by interlink-plugin-sdk)
- FastAPI
- uvicorn
- interlink-plugin-sdk (local package)

## Installation

**Important:** This plugin requires Python 3.11 or higher. If your system Python is older, use Anaconda/Miniconda or pyenv.

### Check Python Version

```bash
python3 --version
# If < 3.11, use: /opt/anaconda3/bin/python --version (if you have Anaconda)
```

### Install Dependencies

```bash
cd interlink-minimalist-plugin

# If using system Python 3.11+
pip install -r requirements.txt

# If using Anaconda Python (recommended on macOS)
/opt/anaconda3/bin/python -m pip install -r requirements.txt
```

## Running the Plugin

Start the plugin server:

```bash
# Using system Python 3.11+
uvicorn plugin:app --host 0.0.0.0 --port 4000

# Using Anaconda Python
/opt/anaconda3/bin/python -m uvicorn plugin:app --host 0.0.0.0 --port 4000
```

The plugin will be available at `http://localhost:4000`.

### Test the Plugin

You can access the interactive API documentation at `http://localhost:4000/docs` when the server is running.

Test the `/create` endpoint:

```bash
curl -X POST http://localhost:4000/create \
  -H "Content-Type: application/json" \
  -d '{
    "pod": {
      "metadata": {"name": "test", "namespace": "default", "uid": "test-123"},
      "spec": {"containers": [{"name": "test", "image": "nginx", "tag": "latest"}]}
    },
    "container": []
  }'
```

## API Endpoints

### POST /create
Creates a pod and returns a CreateStruct with PodUID and PodJID.

**Request**: `Pod` object from interlink-plugin-sdk
**Response**: `CreateStruct` with `PodUID` and `PodJID="1"`

### POST /delete
Deletes a pod.

**Request**: `PodRequest` object
**Response**: String confirmation message

### GET /status
Returns the status of one or more pods.

**Request**: List of `PodRequest` objects
**Response**: List of `PodStatus` objects with containers in "waiting" state

### GET /getLogs
Returns logs for a specific container.

**Request**: `LogRequest` object
**Response**: Plain text logs (minimal placeholder message)

## Example Output

When a pod creation request is received, the plugin prints:

```
============================================================
  CREATE
============================================================
{
  "pod": {
    "metadata": {
      "name": "test-pod",
      "uid": "abc-123",
      ...
    },
    "spec": {
      "containers": [...]
    }
  }
}
============================================================
```

## Docker Deployment

Build the Docker image:

```bash
docker build -t interlink-minimalist-plugin .
```

Run the container:

```bash
docker run -p 4000:4000 interlink-minimalist-plugin
```

## Integration with interLink

Configure your interLink deployment to point to this plugin:

```yaml
# In your interLink configuration
InterlinkURL: "http://localhost:3000"
SidecarURL: "http://localhost:4000"  # This plugin's address
```

## Development

This plugin is intentionally minimal. For production use, you would extend it to:

1. **Actually manage workloads** (e.g., submit to Slurm, create Docker containers, etc.)
2. **Track job states** and return real status information
3. **Implement proper logging** retrieval from your backend
4. **Add error handling** and validation
5. **Implement authentication** if required

## See Also

- [interLink Documentation](https://github.com/interTwin-eu/interLink)
- [interlink-plugin-sdk](../interlink-plugin-sdk/)
- [interlink-docker-plugin](../interlink-docker-plugin/) - Full Docker backend example
- [interlink-slurm-plugin](../interlink-slurm-plugin/) - Full Slurm backend example

## License

Same as the HPC-Pilot project.
