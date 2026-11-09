
import unittest

from security.network_validator import evaluate_network_security


class TestNetworkSecurity(unittest.TestCase):

    def setUp(self):

        self.network = """
        addressPrefixes: [
            '10.10.0.0/16'
        ]

        name: 'application-subnet'
        addressPrefix: '10.10.1.0/24'
        networkSecurityGroup: {
            id: nsgResourceId
        }

        name: 'private-endpoints-subnet'
        addressPrefix: '10.10.2.0/24'
        privateEndpointNetworkPolicies: 'Disabled'
        """

        self.nsg = """
        name: 'Allow-HTTPS-Inbound'
        direction: 'Inbound'
        access: 'Allow'
        destinationPortRange: '443'

        name: 'Deny-Internet-Inbound'
        direction: 'Inbound'
        access: 'Deny'
        sourceAddressPrefix: 'Internet'
        """

    def run_validation(self):

        return evaluate_network_security(
            self.network,
            self.nsg
        )

    def test_valid_network_configuration(self):

        checks = self.run_validation()

        self.assertTrue(
            all(item["passed"] for item in checks)
        )

    def test_invalid_vnet_address_space(self):

        self.network = self.network.replace(
            "10.10.0.0/16",
            "192.168.0.0/16"
        )

        checks = self.run_validation()

        self.assertFalse(checks[0]["passed"])

    def test_missing_application_subnet(self):

        self.network = self.network.replace(
            "name: 'application-subnet'",
            "name: 'missing-subnet'"
        )

        checks = self.run_validation()

        self.assertFalse(checks[1]["passed"])

    def test_missing_nsg_attachment(self):

        self.network = self.network.replace(
            "networkSecurityGroup: {",
            "missingNetworkSecurityGroup: {"
        )

        checks = self.run_validation()

        self.assertFalse(checks[2]["passed"])

    def test_private_endpoint_policies_enabled(self):

        self.network = self.network.replace(
            "'Disabled'",
            "'Enabled'"
        )

        checks = self.run_validation()

        self.assertFalse(checks[4]["passed"])

    def test_missing_https_rule(self):

        self.nsg = self.nsg.replace(
            "name: 'Allow-HTTPS-Inbound'",
            "name: 'Missing-HTTPS-Rule'"
        )

        checks = self.run_validation()

        self.assertFalse(checks[5]["passed"])

    def test_missing_internet_deny_rule(self):

        self.nsg = self.nsg.replace(
            "name: 'Deny-Internet-Inbound'",
            "name: 'Missing-Deny-Rule'"
        )

        checks = self.run_validation()

        self.assertFalse(checks[6]["passed"])


if __name__ == "__main__":
    unittest.main()
