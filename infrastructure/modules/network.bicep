
@description('Name of the virtual network')
param vnetName string

@description('Azure deployment region')
param location string

@description('Resource tags')
param tags object

@description('Resource ID of the Network Security Group')
param nsgResourceId string

resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: vnetName
  location: location

  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.10.0.0/16'
      ]
    }

    subnets: [
      {
        name: 'application-subnet'
        properties: {
          addressPrefix: '10.10.1.0/24'
          networkSecurityGroup: {
            id: nsgResourceId
          }
        }
      }
      {
        name: 'private-endpoints-subnet'
        properties: {
          addressPrefix: '10.10.2.0/24'
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
    ]
  }

  tags: tags
}

output vnetResourceId string = vnet.id
output vnetResourceName string = vnet.name

output applicationSubnetId string = resourceId(
  'Microsoft.Network/virtualNetworks/subnets',
  vnetName,
  'application-subnet'
)

output privateEndpointSubnetId string = resourceId(
  'Microsoft.Network/virtualNetworks/subnets',
  vnetName,
  'private-endpoints-subnet'
)
