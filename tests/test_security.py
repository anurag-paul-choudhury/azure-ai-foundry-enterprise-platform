
import unittest

from security.policy_validator import evaluate_checks


class TestSecurityValidator(unittest.TestCase):

    def setUp(self):

        self.foundry = """
        publicNetworkAccess: 'Disabled'
        disableLocalAuth: true
        identity: {
            type: 'SystemAssigned'
        }
        """

        self.identity = """
        Microsoft.ManagedIdentity/userAssignedIdentities
        """

        self.rbac = """
        Microsoft.Authorization/roleAssignments
        scope: foundryAccount
        53ca6127-db72-4b80-b1b0-d745d6d5456d
        """

        self.private_endpoint = """
        Microsoft.Network/privateEndpoints@2024-05-01
        privateLinkServiceConnections
        groupIds: ['account']
        """

    def run_validation(self):
        return evaluate_checks(
            self.foundry,
            self.identity,
            self.rbac,
            self.private_endpoint
        )

    def test_valid_configuration(self):
        checks = self.run_validation()

        self.assertTrue(all(check["passed"] for check in checks))

    def test_public_access_enabled(self):
        self.foundry = self.foundry.replace(
            "'Disabled'", "'Enabled'"
        )

        checks = self.run_validation()

        self.assertFalse(checks[0]["passed"])

    def test_local_authentication_enabled(self):
        self.foundry = self.foundry.replace(
            "disableLocalAuth: true",
            "disableLocalAuth: false"
        )

        checks = self.run_validation()

        self.assertFalse(checks[1]["passed"])

    def test_missing_rbac(self):
        self.rbac = ""

        checks = self.run_validation()

        self.assertFalse(checks[3]["passed"])

    def test_missing_private_endpoint(self):
        self.private_endpoint = ""

        checks = self.run_validation()

        self.assertFalse(checks[4]["passed"])


if __name__ == "__main__":
    unittest.main()
