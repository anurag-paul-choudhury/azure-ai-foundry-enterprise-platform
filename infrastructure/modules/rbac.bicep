
@description('Name of the Azure AI Foundry account')
param accountName string

@description('Principal ID of the managed identity')
param principalId string

// Reference the existing Foundry account.
resource foundryAccount 'Microsoft.CognitiveServices/accounts@2026-05-01' existing = {
  name: accountName
}

// Foundry User built-in role ID.
var roleDefinitionId = '53ca6127-db72-4b80-b1b0-d745d6d5456d'

// Assign Foundry User to the managed identity.
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(
    foundryAccount.id,
    principalId,
    roleDefinitionId
  )

  scope: foundryAccount

  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      roleDefinitionId
    )

    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}

output roleAssignmentId string = roleAssignment.id
output assignedPrincipalId string = principalId
output assignedRoleId string = roleDefinitionId
