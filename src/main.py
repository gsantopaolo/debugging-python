from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel
from typing import Optional, Dict, List
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="DateTime API", version="1.0.0")

# Supported timezones for conversion
TIMEZONE_OFFSETS = {
    "UTC": 0,
    "EST": -5,
    "PST": -8,
    "CET": 1,
    "JST": 9,
    "AEST": 10,
}


class DateTimeResponse(BaseModel):
    utc_datetime: str
    timestamp: float
    timezone: str = "UTC"
    local_datetime: Optional[str] = None


class TimezoneConversion(BaseModel):
    original_time: str
    converted_times: Dict[str, str]
    time_differences: Dict[str, float]


class BusinessHoursResponse(BaseModel):
    is_business_hours: bool
    current_time: str
    business_start: str
    business_end: str
    hours_until_open: Optional[float] = None
    hours_until_close: Optional[float] = None


@app.get("/")
async def root():
    """Root endpoint with API information"""
    logger.info("Root endpoint accessed")
    return {
        "message": "DateTime API - Advanced time operations",
        "endpoints": [
            "/datetime",
            "/datetime/convert",
            "/business-hours",
            "/time-diff",
        ],
    }


@app.get("/datetime", response_model=DateTimeResponse)
async def get_current_datetime(
    tz: Optional[str] = Query(None, description="Timezone code (e.g., EST, PST, CET)")
):
    """Returns the current date and time in UTC or specified timezone"""
    logger.debug(f"Getting current datetime for timezone: {tz}")
    
    now_utc = datetime.now(timezone.utc)
    local_time = None
    timezone_name = "UTC"
    
    if tz:
        # This is a good place to set a breakpoint to debug timezone conversion
        local_time, timezone_name = _convert_to_timezone(now_utc, tz)
        logger.info(f"Converted UTC time to {timezone_name}: {local_time}")
    
    return DateTimeResponse(
        utc_datetime=now_utc.isoformat(),
        timestamp=now_utc.timestamp(),
        timezone=timezone_name,
        local_datetime=local_time,
    )


@app.get("/datetime/convert", response_model=TimezoneConversion)
async def convert_timezones(
    time_str: str = Query(..., description="ISO format datetime string"),
    timezones: str = Query("EST,PST,CET", description="Comma-separated timezone codes"),
):
    """Convert a given time to multiple timezones"""
    logger.debug(f"Converting time {time_str} to timezones: {timezones}")
    
    try:
        # Parse the input datetime - good debugging point for format errors
        original_dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        logger.info(f"Parsed datetime: {original_dt}")
    except ValueError as e:
        logger.error(f"Failed to parse datetime: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid datetime format: {e}")
    
    tz_list = [tz.strip().upper() for tz in timezones.split(",")]
    converted_times = {}
    time_differences = {}
    
    # Complex loop - great for step-through debugging
    for tz in tz_list:
        if tz not in TIMEZONE_OFFSETS:
            logger.warning(f"Unknown timezone: {tz}, skipping")
            continue
        
        converted_time, _ = _convert_to_timezone(original_dt, tz)
        converted_times[tz] = converted_time
        
        # Calculate time difference in hours
        time_diff = _calculate_time_difference(original_dt, tz)
        time_differences[tz] = time_diff
        logger.debug(f"Timezone {tz}: {converted_time} (diff: {time_diff}h)")
    
    return TimezoneConversion(
        original_time=original_dt.isoformat(),
        converted_times=converted_times,
        time_differences=time_differences,
    )


@app.get("/business-hours", response_model=BusinessHoursResponse)
async def check_business_hours(
    tz: str = Query("EST", description="Timezone for business hours"),
    start_hour: int = Query(9, ge=0, le=23),
    end_hour: int = Query(17, ge=0, le=23),
):
    """Check if current time falls within business hours"""
    logger.debug(f"Checking business hours in {tz}: {start_hour}-{end_hour}")
    
    now_utc = datetime.now(timezone.utc)
    local_time_str, _ = _convert_to_timezone(now_utc, tz)
    local_time = datetime.fromisoformat(local_time_str)
    
    # Set breakpoint here to debug business hours logic
    is_business_hours, hours_until_open, hours_until_close = _check_if_business_hours(
        local_time, start_hour, end_hour
    )
    
    business_start = local_time.replace(
        hour=start_hour, minute=0, second=0, microsecond=0
    )
    business_end = local_time.replace(
        hour=end_hour, minute=0, second=0, microsecond=0
    )
    
    return BusinessHoursResponse(
        is_business_hours=is_business_hours,
        current_time=local_time.isoformat(),
        business_start=business_start.isoformat(),
        business_end=business_end.isoformat(),
        hours_until_open=hours_until_open,
        hours_until_close=hours_until_close,
    )


@app.get("/time-diff")
async def calculate_time_difference(
    time1: str = Query(..., description="First datetime (ISO format)"),
    time2: str = Query(..., description="Second datetime (ISO format)"),
):
    """Calculate the difference between two datetimes"""
    logger.debug(f"Calculating difference between {time1} and {time2}")
    
    try:
        dt1 = datetime.fromisoformat(time1.replace("Z", "+00:00"))
        dt2 = datetime.fromisoformat(time2.replace("Z", "+00:00"))
        
        # Good debugging point for datetime arithmetic
        diff = dt2 - dt1
        total_seconds = diff.total_seconds()
        
        return {
            "time1": dt1.isoformat(),
            "time2": dt2.isoformat(),
            "difference": {
                "days": diff.days,
                "seconds": diff.seconds,
                "total_seconds": total_seconds,
                "total_minutes": total_seconds / 60,
                "total_hours": total_seconds / 3600,
                "total_days": total_seconds / 86400,
            },
        }
    except ValueError as e:
        logger.error(f"Invalid datetime format: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid datetime format: {e}")


# ============================================================================
# Helper functions - Perfect for stepping through during debugging
# ============================================================================


def _convert_to_timezone(dt: datetime, tz_code: str) -> tuple[str, str]:
    """Convert a datetime to a specific timezone"""
    # Set a breakpoint here to understand timezone conversion logic
    if tz_code.upper() not in TIMEZONE_OFFSETS:
        logger.warning(f"Unknown timezone {tz_code}, defaulting to UTC")
        return dt.isoformat(), "UTC"
    
    offset_hours = TIMEZONE_OFFSETS[tz_code.upper()]
    offset = timedelta(hours=offset_hours)
    
    # Watch these variables during debugging
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    local_dt = dt + offset
    logger.debug(f"Converted {dt} to {tz_code}: {local_dt}")
    
    return local_dt.isoformat(), tz_code.upper()


def _calculate_time_difference(dt: datetime, tz_code: str) -> float:
    """Calculate time difference in hours for a timezone"""
    if tz_code.upper() not in TIMEZONE_OFFSETS:
        return 0.0
    return float(TIMEZONE_OFFSETS[tz_code.upper()])


def _check_if_business_hours(
    local_time: datetime, start_hour: int, end_hour: int
) -> tuple[bool, Optional[float], Optional[float]]:
    """Check if time is within business hours and calculate time until open/close"""
    # Great function to step through with the debugger
    current_hour = local_time.hour
    current_minute = local_time.minute
    current_decimal_hour = current_hour + (current_minute / 60.0)
    
    logger.debug(
        f"Current time: {current_decimal_hour:.2f}, "
        f"Business hours: {start_hour}-{end_hour}"
    )
    
    is_business_hours = start_hour <= current_decimal_hour < end_hour
    
    hours_until_open = None
    hours_until_close = None
    
    if not is_business_hours:
        if current_decimal_hour < start_hour:
            # Before business hours
            hours_until_open = start_hour - current_decimal_hour
            logger.debug(f"Before business hours, opens in {hours_until_open:.2f}h")
        else:
            # After business hours
            hours_until_open = (24 - current_decimal_hour) + start_hour
            logger.debug(f"After business hours, opens in {hours_until_open:.2f}h")
    else:
        # During business hours
        hours_until_close = end_hour - current_decimal_hour
        logger.debug(f"Currently open, closes in {hours_until_close:.2f}h")
    
    return is_business_hours, hours_until_open, hours_until_close
