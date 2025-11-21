# Quick Start: Debugging Setup 🚀

This is a companion guide to the comprehensive blog post in `docs/post.md`.

## Quick Setup

### 1. Create Conda Environment
```bash
conda env create -f environment.yml
conda activate datetime-api
```

### 2. Run Locally
```bash
cd src
uvicorn main:app --reload --log-level debug
```

Access: http://localhost:8000

### 3. Run in Docker
```bash
# Build
docker build -t datetime-api:latest -f src/Dockerfile src/

# Run
docker run -d --name datetime-api -p 8000:8000 -v $(pwd)/src:/app datetime-api:latest
```

### 4. Run with Docker Compose
```bash
docker-compose up -d
```

### 5. Test the API
```bash
# Basic endpoint
curl http://localhost:8000/

# Get current time in EST
curl "http://localhost:8000/datetime?tz=EST"

# Convert time to multiple timezones
curl "http://localhost:8000/datetime/convert?time_str=2024-11-21T15:00:00Z&timezones=EST,PST,JST"

# Check business hours
curl "http://localhost:8000/business-hours?tz=EST&start_hour=9&end_hour=17"

# Calculate time difference
curl "http://localhost:8000/time-diff?time1=2024-11-21T09:00:00Z&time2=2024-11-21T17:00:00Z"
```

## PyCharm Run/Debug Configurations

Create these configurations in PyCharm:

### Local Debugging: `datetime-api-local`
- **Module name**: `uvicorn`
- **Parameters**: `main:app --reload --log-level debug`
- **Working directory**: `<project>/src`
- **Interpreter**: `datetime-api` (conda env)

### Docker Debugging: `datetime-api-docker`
- **Module name**: `uvicorn`
- **Parameters**: `main:app --host 0.0.0.0 --port 8000 --reload --log-level debug`
- **Working directory**: `/app`
- **Interpreter**: Docker interpreter (datetime-api:latest)
- **Port bindings**: `8000:8000`
- **Volume bindings**: `<project>/src:/app`

### Docker Compose Debugging: `datetime-api-compose`
- **Module name**: `uvicorn`
- **Parameters**: `main:app --host 0.0.0.0 --port 8000 --reload --log-level debug`
- **Working directory**: `/app`
- **Interpreter**: Docker Compose interpreter (datetime-api service)

### Remote Debug Server: `docker-remote-debug`
- **Type**: Python Debug Server
- **IDE host name**: `localhost`
- **Port**: `5678`
- **Path mappings**: `<project>/src` → `/app`

## Debugging Locations

### Good breakpoints to try:

**Line 74** (`get_current_datetime`):
```python
local_time, timezone_name = _convert_to_timezone(now_utc, tz)
```
*Debug timezone conversion logic*

**Line 106** (`convert_timezones`):
```python
for tz in tz_list:
```
*Step through multiple timezone conversions*

**Line 140** (`check_business_hours`):
```python
is_business_hours, hours_until_open, hours_until_close = _check_if_business_hours(
```
*Debug business hours calculation*

**Line 206** (`_convert_to_timezone`):
```python
offset_hours = TIMEZONE_OFFSETS[tz_code.upper()]
```
*Understand timezone offset logic*

**Line 240** (`_check_if_business_hours`):
```python
is_business_hours = start_hour <= current_decimal_hour < end_hour
```
*Inspect boolean logic*

## Pro Tips

1. **Use Exception Breakpoints**: `Run → View Breakpoints → + → Python Exception Breakpoints → ValueError`
2. **Conditional Breakpoints**: Right-click breakpoint → Condition: `tz == "EST"`
3. **Evaluate Expressions**: While debugging, press `⌥F8` to evaluate any Python expression
4. **Watches**: Add expressions to track across debugging sessions

## Troubleshooting

**Breakpoints not working?**
- Check that you're using the correct interpreter in Run/Debug config
- Verify path mappings (local → container)
- Ensure volume mounts are correct

**Can't connect to Docker?**
- Verify Docker Desktop is running
- Check PyCharm Docker connection: Settings → Docker

**Import errors in Docker?**
- Rebuild image: `docker build -t datetime-api:latest -f src/Dockerfile src/`
- Check WORKDIR matches your working directory in config

## Read the Full Guide

For comprehensive explanations, troubleshooting, and advanced techniques, see:
**`docs/post.md`**
