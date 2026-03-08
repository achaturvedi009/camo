import os

class DashboardLoader:
    @staticmethod
    def get_dashboard_url(profile_id: str) -> str:
        # Resolves via localhost backend diagnostic API
        return f"http://127.0.0.1:8000/dashboard-api/viewer?id={profile_id}"
