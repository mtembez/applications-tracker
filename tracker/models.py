"""Domain models and schema definitions for Applications Tracker."""
from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class AppStatus(str, Enum):
    WISHLIST = "WISHLIST"
    APPLIED = "APPLIED"
    SCREENING = "SCREENING"
    TECHNICAL = "TECHNICAL"
    FINAL_ROUND = "FINAL_ROUND"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"

class LocationType(str, Enum):
    NAIROBI = "NAIROBI"
    REMOTE_EMEA = "REMOTE_EMEA"
    REMOTE_GLOBAL = "REMOTE_GLOBAL"
    HYBRID = "HYBRID"

class EventType(str, Enum):
    CREATED = "CREATED"
    STATUS_CHANGE = "STATUS_CHANGE"
    NOTE_ADDED = "NOTE_ADDED"
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED"

class ApplicationBase(BaseModel):
    company: str = Field(..., min_length=1, max_length=120)
    role: str = Field(..., min_length=1, max_length=120)
    location_type: LocationType = LocationType.REMOTE_GLOBAL
    compensation: Optional[str] = Field(None, max_length=80)
    channel: str = Field("Direct", max_length=80)
    job_url: Optional[str] = None
    contact_person: Optional[str] = None
    notes: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    status: AppStatus = AppStatus.APPLIED

class ApplicationStatusUpdate(BaseModel):
    status: AppStatus
    note: Optional[str] = None

class TimelineEventResponse(BaseModel):
    id: int
    app_id: int
    event_type: EventType
    details: str
    created_at: str

class ApplicationResponse(ApplicationBase):
    id: int
    status: AppStatus
    applied_at: str
    last_activity_at: str
    timeline: List[TimelineEventResponse] = []

class MetricsResponse(BaseModel):
    total_applications: int
    active_applications: int
    interview_count: int
    offer_count: int
    rejection_count: int
    interview_rate_pct: float
    offer_rate_pct: float
    funnel: dict[str, int]
