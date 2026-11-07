
from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parents[1]

FOUNDRY_FILE = PROJECT_ROOT / "infrastructure/modules/foundry-account.bicep"
IDENTITY_FILE = PROJECT_ROOT / "infrastructure/modules/identity.bicep"
RBAC_FILE = PROJECT_ROOT / "infrastructure/modules/rbac.bicep"
PRIVATE_ENDPOINT_FILE = PROJECT_ROOT / "infrastructure/modules/private-endpoint.bicep"


def read_file(file_path):
    if not file_path.exists():
        return ""

    return file_path.read_text(encoding="utf-8")


def contains_pattern(content, pattern):
    return bool(re.search(pattern, content, re.IGNORECASE))


def evaluate_checks(foundry, identity, rbac, private_endpoint):

    checks = [
        {
            "name": "Public network access disabled",
            "passed": contains_pattern(
                foundry, r"publicNetworkAccess\s*:\s*'Disabled'"
            )
        },
        {
            "name": "Local authentication disabled",
            "passed": contains_pattern(
                foundry, r"disableLocalAuth\s*:\s*true"
            )
        },
        {
            "name": "Managed identity configured",
            "passed": (
                contains_pattern(foundry, r"type\s*:\s*'SystemAssigned'")
                and "Microsoft.ManagedIdentity/userAssignedIdentities" in identity
            )
        },
        {
            "name": "RBAC configured",
            "passed": (
                "Microsoft.Authorization/roleAssignments" in rbac
                and "scope: foundryAccount" in rbac
                and "53ca6127-db72-4b80-b1b0-d745d6d5456d" in rbac
            )
        },
        {
            "name": "Private Endpoint configured",
            "passed": (
                "Microsoft.Network/privateEndpoints@" in private_endpoint
                and "privateLinkServiceConnections" in private_endpoint
                and "'account'" in private_endpoint
            )
        }
    ]

    return checks


def validate_security():

    foundry = read_file(FOUNDRY_FILE)
    identity = read_file(IDENTITY_FILE)
    rbac = read_file(RBAC_FILE)
    private_endpoint = read_file(PRIVATE_ENDPOINT_FILE)

    checks = evaluate_checks(
        foundry,
        identity,
        rbac,
        private_endpoint
    )

    print("\n====================================")
    print(" ENTERPRISE AI SECURITY VALIDATION")
    print("====================================\n")

    passed_count = 0

    for check in checks:

        if check["passed"]:
            print(f"[PASS] {check['name']}")
            passed_count += 1
        else:
            print(f"[FAIL] {check['name']}")

    total_checks = len(checks)
    failed_count = total_checks - passed_count

    print("\n====================================")
    print(f"Total checks : {total_checks}")
    print(f"Passed       : {passed_count}")
    print(f"Failed       : {failed_count}")
    print("====================================")

    return failed_count == 0


if __name__ == "__main__":
    success = validate_security()
    raise SystemExit(0 if success else 1)
