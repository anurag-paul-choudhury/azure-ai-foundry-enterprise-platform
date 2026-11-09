
from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parents[1]

NETWORK_FILE = (
    PROJECT_ROOT / "infrastructure/modules/network.bicep"
)

NSG_FILE = (
    PROJECT_ROOT / "infrastructure/modules/network-security.bicep"
)


def read_file(file_path):
    if not file_path.exists():
        return ""

    return file_path.read_text(encoding="utf-8")


def check(pattern, content):
    return bool(re.search(pattern, content, re.IGNORECASE))


def evaluate_network_security(network, nsg):

    checks = [

        {
            "name": "VNet address space configured",
            "passed": check(
                r"addressPrefixes\s*:\s*\[\s*'10\.10\.0\.0/16'",
                network
            )
        },

        {
            "name": "Application subnet configured",
            "passed": check(
                r"name\s*:\s*'application-subnet'",
                network
            ) and check(
                r"addressPrefix\s*:\s*'10\.10\.1\.0/24'",
                network
            )
        },

        {
            "name": "Application subnet attached to NSG",
            "passed": check(
                r"\bnetworkSecurityGroup\s*:\s*\{\s*id\s*:\s*nsgResourceId",
                network
            )
        },

        {
            "name": "Private endpoint subnet configured",
            "passed": check(
                r"name\s*:\s*'private-endpoints-subnet'",
                network
            ) and check(
                r"addressPrefix\s*:\s*'10\.10\.2\.0/24'",
                network
            )
        },

        {
            "name": "Private endpoint network policies disabled",
            "passed": check(
                r"privateEndpointNetworkPolicies\s*:\s*'Disabled'",
                network
            )
        },

        {
            "name": "HTTPS inbound rule configured",
            "passed": (
                check(r"name\s*:\s*'Allow-HTTPS-Inbound'", nsg)
                and check(r"destinationPortRange\s*:\s*'443'", nsg)
                and check(r"direction\s*:\s*'Inbound'", nsg)
                and check(r"access\s*:\s*'Allow'", nsg)
            )
        },

        {
            "name": "Internet inbound deny rule configured",
            "passed": (
                check(r"name\s*:\s*'Deny-Internet-Inbound'", nsg)
                and check(r"sourceAddressPrefix\s*:\s*'Internet'", nsg)
                and check(r"access\s*:\s*'Deny'", nsg)
                and check(r"direction\s*:\s*'Inbound'", nsg)
            )
        }
    ]

    return checks


def validate_network_security():

    network = read_file(NETWORK_FILE)
    nsg = read_file(NSG_FILE)

    checks = evaluate_network_security(network, nsg)

    print("\n======================================")
    print(" ENTERPRISE NETWORK SECURITY CHECK")
    print("======================================\n")

    passed = 0

    for item in checks:

        if item["passed"]:
            print(f"[PASS] {item['name']}")
            passed += 1
        else:
            print(f"[FAIL] {item['name']}")

    total = len(checks)

    print("\n======================================")
    print(f"Total checks : {total}")
    print(f"Passed       : {passed}")
    print(f"Failed       : {total - passed}")
    print("======================================")

    return passed == total


if __name__ == "__main__":

    success = validate_network_security()

    raise SystemExit(0 if success else 1)
