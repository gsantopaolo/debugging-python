#  Deep-Dive: Debugging Python with PyCharm on macOS (Local & Docker) 🐍


A FastAPI-based DateTime API with advanced timezone conversion and business hours functionality. This project serves as a comprehensive example for debugging Python applications with PyCharm on macOS, both locally and in Docker containers.

## Features

- ✅ Current UTC datetime retrieval with timezone conversion
- ✅ Multi-timezone conversion for any datetime
- ✅ Business hours checking across timezones
- ✅ Time difference calculations
- ✅ Comprehensive logging for debugging
- ✅ Full Docker support

## Quick Start

```bash
# Option 1: Local with conda
conda env create -f environment.yml
conda activate datetime-api
cd src && uvicorn main:app --reload

# Option 2: Docker
docker build -t datetime-api:latest -f src/Dockerfile src/
docker run -d -p 8000:8000 datetime-api:latest

# Option 3: Docker Compose
docker-compose up -d
```

Access the API: http://localhost:8000  
API Documentation: http://localhost:8000/docs

## API Endpoints

- `GET /` - API information
- `GET /datetime` - Current UTC datetime (with optional timezone conversion)
- `GET /datetime/convert` - Convert datetime to multiple timezones
- `GET /business-hours` - Check if current time is within business hours
- `GET /time-diff` - Calculate difference between two datetimes

## Debugging Guide 🐛

This project includes a comprehensive guide for debugging Python applications with PyCharm:

- **Quick Start**: See `DEBUGGING_GUIDE.md` for setup instructions
- **Full Blog Post**: See `docs/post.md` for the complete debugging guide covering:
  - Local debugging with conda
  - Docker interpreter debugging
  - Docker Compose debugging
  - Remote debugging with Python Debug Server
  - Troubleshooting and best practices

## Project Structure

```
codechallenge/
├── src/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Docker image definition
├── deployment/
│   └── build.sh                # Build script
├── docs/
│   └── post.md                 # Comprehensive debugging blog post
├── docker-compose.yml          # Standard Docker Compose config
├── docker-compose.debug.yml    # Debug-specific compose config
├── environment.yml             # Conda environment definition
├── DEBUGGING_GUIDE.md          # Quick debugging setup guide
└── README.md                   # This file
```

## Development

### Prerequisites

- Python 3.11+
- Conda/Miniconda
- Docker Desktop (for containerized development)
- PyCharm Professional (recommended for full debugging features)

### Local Development

```bash
# Create environment
conda env create -f environment.yml
conda activate datetime-api

# Run locally
cd src
uvicorn main:app --reload --log-level debug
```

### Testing the API

```bash
# Get current time in EST
curl "http://localhost:8000/datetime?tz=EST"

# Convert time to multiple timezones
curl "http://localhost:8000/datetime/convert?time_str=2024-11-21T15:00:00Z&timezones=EST,PST,JST"

# Check business hours
curl "http://localhost:8000/business-hours?tz=EST&start_hour=9&end_hour=17"
```

## License

See LICENSE file for details.

## Learn More

For a deep dive into debugging Python applications with PyCharm (local and Docker), read the comprehensive guide in `docs/post.md`.