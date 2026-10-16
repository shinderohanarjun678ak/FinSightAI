
from src.frontend.services.auth_api import login_user

try:
    result = login_user(
        "saisjadhv@gmail.com",
        "Saioo007",
    )

    print("Status:", result["status_code"])
    print("Response:", result["data"])

except Exception as error:
    print("API connection failed:", error)
