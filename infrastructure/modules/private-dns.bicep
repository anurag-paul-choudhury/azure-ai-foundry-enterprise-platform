
@description('Name of the existing virtual network')
param vnetName string

@description('Resource tags')
param tags object

// Reference the VNet created by the network module.
resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' existing = {
  name: vnetName
}

// Private DNS zones required for Foundry endpoints.
var dnsZoneNames = [
  'privatelink.cognitiveservices.azure.com'
  'privatelink.openai.azure.com'
  'privatelink.services.ai.azure.com'
]

// Create all three private DNS zones.
resource privateDnsZones 'Microsoft.Network/privateDnsZones@2020-06-01' = [
  for zoneName in dnsZoneNames: {
    name: zoneName
    location: 'global'
    tags: tags
  }
]

// Link each DNS zone to the virtual network.
resource dnsZoneLinks 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2024-06-01' = [
  for (zoneName, i) in dnsZoneNames: {
    parent: privateDnsZones[i]
    name: '${vnetName}-link'
    location: 'global'

    properties: {
      virtualNetwork: {
        id: vnet.id
      }
      registrationEnabled: false
    }
  }
]

output privateDnsZoneNames array = dnsZoneNames

output privateDnsZoneIds array = [
  for i in range(0, length(dnsZoneNames)): privateDnsZones[i].id
]