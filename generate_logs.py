import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

USERS = [
    "john@example.com",
    "sarah@company.com",
    "mike@test.com",
    "admin@internal.local",
    "customer.payments@example.org",
]

IPS = [
    "10.10.12.5",
    "172.16.4.22",
    "192.168.1.90",
    "10.0.0.45",
    "172.20.9.18",
]

TOKENS = [
    "sk_live_abc123",
    "ghp_123456789secret",
    "api-token-prod-xyz",
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI",
    "sk_live_payment_987654",
]

MESSAGES = [
    "Database connection timeout while connecting to postgres-prod.internal.local",
    "Connection pool exhausted for service auth-api",
    "Failed login attempt",
    "Payment service returned 500 Internal Server Error",
    "Nginx upstream timed out",
    "Retrying database connection",
    "User session expired",
    "Cache miss for customer profile",
    "CRITICAL: PostgreSQL max connections reached",
    "Background worker failed to process payment event",
]

SERVICES = [
    "auth-api",
    "payment-api",
    "checkout-service",
    "user-service",
    "nginx-gateway",
]

start_time = datetime.now(timezone.utc) - timedelta(hours=2)

def main() -> None:
    raw_log_path = LOG_DIR / "raw_app.log"

    with open(raw_log_path, "w", encoding="utf-8") as f:
        for i in range(50000):
            timestamp = start_time + timedelta(seconds=i)

            level = random.choices(
                ["INFO", "WARNING", "ERROR", "CRITICAL"],
                weights=[62, 15, 17, 6],
                k=1,
            )[0]

            user = random.choice(USERS)
            ip = random.choice(IPS)
            token = random.choice(TOKENS)
            service = random.choice(SERVICES)
            message = random.choice(MESSAGES)

            # Make the incident theme stronger by increasing database-related failures
            if i % 7 == 0:
                level = random.choice(["ERROR", "CRITICAL"])
                message = random.choice([
                    "Database connection timeout while connecting to postgres-prod.internal.local",
                    "Connection pool exhausted for service auth-api",
                    "CRITICAL: PostgreSQL max connections reached",
                ])
                service = random.choice(["auth-api", "payment-api", "checkout-service"])

            line = (
                f"{timestamp} {level} "
                f"service={service} "
                f"user={user} "
                f"ip={ip} "
                f"token={token} "
                f"request_id=req-{random.randint(10000,99999)} "
                f"message='{message}'\n"
            )

            f.write(line)

    print(f"Generated {raw_log_path} with 50,000 log lines")

if __name__ == "__main__":
    main()
