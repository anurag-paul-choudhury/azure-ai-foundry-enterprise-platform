
@description('Name of the Azure AI Foundry account')
param accountName string

@description('Azure deployment region')
param location string

@description('Resource tags')
param tags object

resource foundryAccount 'Microsoft.CognitiveServices/accounts@2026-05-01' = {
  name: accountName
  location: location
  kind: 'AIServices'

  sku: {
    name: 'S0'
  }

  identity: {
    type: 'SystemAssigned'
  }

  properties: {
    allowProjectManagement: true
    customSubDomainName: accountName
    disableLocalAuth: true
    publicNetworkAccess: 'Disabled'
  }

  tags: tags
}


@description('Name of the Foundry project')
param projectName string = 'enterprise-ai-project'

resource foundryProject 'Microsoft.CognitiveServices/accounts/projects@2026-05-01' = {
  parent: foundryAccount
  name: projectName
  location: location

  properties: {
    displayName: 'Enterprise AI Project'
    description: 'Development project for the Enterprise AI Infrastructure Platform'
  }

  tags: tags
}

output projectResourceId string = foundryProject.id
output projectResourceName string = foundryProject.name


output resourceId string = foundryAccount.id
output resourceName string = foundryAccount.name
