
targetScope = 'resourceGroup'

@description('Environment name')
@allowed([
  'dev'
  'test'
  'prod'
])
param environment string = 'dev'

@description('Azure deployment region')
param location string = 'centralindia'

@description('Project name')
param projectName string = 'enterprise-ai'

var resourcePrefix = '${projectName}-${environment}'

var foundryAccountName = '${resourcePrefix}-${uniqueString(resourceGroup().id)}'

module foundry './modules/foundry-account.bicep' = {
  name: 'foundry-account-${environment}'

  params: {
    accountName: foundryAccountName
    location: location

    tags: {
      project: projectName
      environment: environment
      managedBy: 'Bicep'
      purpose: 'Enterprise AI Platform'
    }
  }
}


module network './modules/network.bicep' = {
  name: 'network-${environment}'

  params: {
    vnetName: '${resourcePrefix}-vnet'
    location: location
    nsgResourceId: networkSecurity.outputs.nsgResourceId

    tags: {
      project: projectName
      environment: environment
      managedBy: 'Bicep'
      purpose: 'Enterprise AI Networking'
    }
  }
}


module privateDns './modules/private-dns.bicep' = {
  name: 'private-dns-${environment}'

  params: {
    vnetName: '${resourcePrefix}-vnet'

    tags: {
      project: projectName
      environment: environment
      managedBy: 'Bicep'
      purpose: 'Private DNS'
    }
  }

  dependsOn: [
    network
  ]
}

output privateDnsZoneNames array = privateDns.outputs.privateDnsZoneNames


module privateEndpoint './modules/private-endpoint.bicep' = {
  name: 'private-endpoint-${environment}'

  params: {
    accountName: foundry.outputs.resourceName
    privateEndpointName: '${resourcePrefix}-foundry-pe'
    location: location

    subnetId: network.outputs.privateEndpointSubnetId

    privateDnsZoneIds: privateDns.outputs.privateDnsZoneIds
  }
}

output privateEndpointId string = privateEndpoint.outputs.privateEndpointId
output privateEndpointName string = privateEndpoint.outputs.privateEndpointName




module identity './modules/identity.bicep' = {
  name: 'identity-${environment}'

  params: {
    identityName: '${resourcePrefix}-identity'
    location: location

    tags: {
      project: projectName
      environment: environment
      managedBy: 'Bicep'
      purpose: 'Application Managed Identity'
    }
  }
}

output identityResourceId string = identity.outputs.identityResourceId
output identityPrincipalId string = identity.outputs.identityPrincipalId
output identityClientId string = identity.outputs.identityClientId

// RBAC module
module rbac './modules/rbac.bicep' = {
  name: 'rbac-${environment}'

  params: {
    accountName: foundry.outputs.resourceName
    principalId: identity.outputs.identityPrincipalId
  }
}

output roleAssignmentId string = rbac.outputs.roleAssignmentId
output assignedPrincipalId string = rbac.outputs.assignedPrincipalId
output assignedRoleId string = rbac.outputs.assignedRoleId


module networkSecurity './modules/network-security.bicep' = {
  name: 'network-security-${environment}'

  params: {
    nsgName: '${resourcePrefix}-nsg'
    location: location

    tags: {
      project: projectName
      environment: environment
      managedBy: 'Bicep'
      purpose: 'Network Security'
    }
  }
}

output nsgResourceId string = networkSecurity.outputs.nsgResourceId

output vnetResourceId string = network.outputs.vnetResourceId
output applicationSubnetId string = network.outputs.applicationSubnetId
output privateEndpointSubnetId string = network.outputs.privateEndpointSubnetId


output environmentName string = environment
output deploymentRegion string = location
output resourcePrefix string = resourcePrefix
output foundryResourceId string = foundry.outputs.resourceId
output foundryResourceName string = foundry.outputs.resourceName

output foundryProjectId string = foundry.outputs.projectResourceId
output foundryProjectName string = foundry.outputs.projectResourceName