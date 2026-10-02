from fastapi import APIRouter, Depends
from typing import Dict, Any
from decimal import Decimal, ROUND_HALF_UP

from app.services.cache import get_revenue_summary
from app.core.auth import authenticate_request as get_current_user
from app.models.auth import AuthenticatedUser

router = APIRouter()

@router.get("/dashboard/summary")
async def get_dashboard_summary(
    property_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
) -> Dict[str, Any]:

    tenant_id = current_user.tenant_id

    revenue_data = await get_revenue_summary(property_id, tenant_id)

    total_revenue = Decimal(revenue_data["total"]).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    return {
        "property_id": revenue_data["property_id"],
        "total_revenue": str(total_revenue),
        "currency": revenue_data["currency"],
        "reservations_count": revenue_data["count"]
    }