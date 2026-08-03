from enum import Enum


class ApplicationStatus(str, Enum):
    PENDING = "Pending"
    REVIEWING = "Reviewing"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"