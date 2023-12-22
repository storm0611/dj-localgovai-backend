# Create your schemas here.
GLOBAL_ADMINS_TABLE_SCHEMA = {
    'TableName': 'GlobalAdmins',
    'KeySchema': [
        {'AttributeName': 'GlobalAdminID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'GlobalAdminID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

ORGANIZATIONS_TABLE_SCHEMA = {
    'TableName': 'Organizations',
    'KeySchema': [
        {'AttributeName': 'OrgID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'InstanceType', 'KeyType': 'RANGE'}  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'OrgID', 'AttributeType': 'S'},
        {'AttributeName': 'InstanceType', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
}

USERS_TABLE_SCHEMA = {
    'TableName': 'Users',
    'KeySchema': [
        {'AttributeName': 'UserID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'OrgID', 'KeyType': 'RANGE'}  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'OrgID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

BILLING_DETAILS_TABLE_SCHEMA = {
    'TableName': 'BillingDetails',
    'KeySchema': [
        {'AttributeName': 'BillingEntityID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'BillingID', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'BillingEntityID', 'AttributeType': 'S'},
        {'AttributeName': 'BillingID', 'AttributeType': 'S'},
        {'AttributeName': 'StripeToken', 'AttributeType': 'S'},
        {'AttributeName': 'TrialPeriod', 'AttributeType': 'S'},
        {'AttributeName': 'CardType', 'AttributeType': 'S'},
        {'AttributeName': 'InstanceType', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_PERMISSIONS_TABLE_SCHEMA = {
    'TableName': 'UserPermissions',
    'KeySchema': [
        {'AttributeName': 'UserID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'UserType', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'UserType', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_TYPE_TABLE_SCHEMA = {
    'TableName': 'UserType',
    'KeySchema': [
        {'AttributeName': 'UserTypeID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserTypeID', 'AttributeType': 'S'},
        {'AttributeName': 'Summary', 'AttributeType': 'S'},
        {'AttributeName': 'UserStory', 'AttributeType': 'S'},
        {'AttributeName': 'AcceptanceCriteria', 'AttributeType': 'S'},
        {'AttributeName': 'DefaultPermissionScheme', 'AttributeType': 'S'},
        {'AttributeName': 'CanInteractWithGlobal', 'AttributeType': 'BOOL'},
        {'AttributeName': 'CanInteractWithInstance', 'AttributeType': 'BOOL'},
        {'AttributeName': 'CanInteractWithExternal', 'AttributeType': 'BOOL'},
        {'AttributeName': 'MessageColor', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

KNOWLEDGE_BASE_TABLE_SCHEMA = {
    'TableName': 'KnowledgeBase',
    'KeySchema': [
        {'AttributeName': 'KnowledgeBaseID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'KnowledgeBaseID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

KNOWLEDGE_BASE_QUESTION_TABLE_SCHEMA = {
    'TableName': 'KnowledgeBaseQuestion',
    'KeySchema': [
        {'AttributeName': 'KnowledgeBaseID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'KnowledgeBaseQuestionID', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'KnowledgeBaseID', 'AttributeType': 'S'},
        {'AttributeName': 'KnowledgeBaseQuestionID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

CHANNELS_TABLE_SCHEMA = {
    'TableName': 'Channels',
    'KeySchema': [
        {'AttributeName': 'ChannelID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ChannelID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

MESSAGES_TABLE_SCHEMA = {
    'TableName': 'ChatMessages',
    'KeySchema': [
        {'AttributeName': 'ChannelID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'MessageID', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ChannelID', 'AttributeType': 'S'},
        {'AttributeName': 'MessageID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

TEAMS_TABLE_SCHEMA = {
    'TableName': 'Teams',
    'KeySchema': [
        {'AttributeName': 'TeamID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'TeamID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}


TEAM_MEMBERS_TABLE_SCHEMA = {
    'TableName': 'TeamMembers',
    'KeySchema': [
        {'AttributeName': 'TeamMemberID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'TeamMemberID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

FILE_UPLOADS_TABLE_SCHEMA = {
    'TableName': 'FileUploads',
    'KeySchema': [
        {'AttributeName': 'FileID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'FileID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SUBSCRIPTION_TIERS_TABLE_SCHEMA = {
    'TableName': 'SubscriptionTiers',
    'KeySchema': [
        {'AttributeName': 'TierID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'TierID', 'AttributeType': 'S'},
        {'AttributeName': 'TierName', 'AttributeType': 'S'},
        {'AttributeName': 'FileLimit', 'AttributeType': 'N'},
        {'AttributeName': 'FolderLimit', 'AttributeType': 'N'},
        {'AttributeName': 'FeatureList', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

LICENSE_KEYS_TABLE_SCHEMA = {
    'TableName': 'LicenseKeys',
    'KeySchema': [
        {'AttributeName': 'LicenseKey', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'LicenseKey', 'AttributeType': 'S'},
        {'AttributeName': 'OrgID', 'AttributeType': 'S'},
        {'AttributeName': 'Validity', 'AttributeType': 'S'},
        {'AttributeName': 'TierID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SUPPORT_AGENTS_TABLE_SCHEMA = {
    'TableName': 'SupportAgents',
    'KeySchema': [
        {'AttributeName': 'AgentID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'AgentID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'AvailabilityStatus', 'AttributeType': 'S'},
        {'AttributeName': 'CurrentQueue', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SUPPORT_QUEUE_TABLE_SCHEMA = {
    'TableName': 'SupportQueue',
    'KeySchema': [
        {'AttributeName': 'QueueID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'QueueID', 'AttributeType': 'S'},
        {'AttributeName': 'AgentID', 'AttributeType': 'S'},
        {'AttributeName': 'CustomerID', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

PROCESS_TABLE_SCHEMA = {
    'TableName': 'ProcessTable',
    'KeySchema': [
        {'AttributeName': 'ProcessID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ProcessID', 'AttributeType': 'S'},
        {'AttributeName': 'ProcessName', 'AttributeType': 'S'},
        {'AttributeName': 'OrgID', 'AttributeType': 'S'},
        {'AttributeName': 'DecisionTreeJSON', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

DECISION_TREES_TABLE_SCHEMA = {
    'TableName': 'DecisionTrees',
    'KeySchema': [
        {'AttributeName': 'TreeID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'TreeID', 'AttributeType': 'S'},
        {'AttributeName': 'TreeJSON', 'AttributeType': 'S'},
        {'AttributeName': 'ProcessID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

EXTENSIONS_TABLE_SCHEMA = {
    'TableName': 'Extensions',
    'KeySchema': [
        {'AttributeName': 'ExtensionID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ExtensionID', 'AttributeType': 'S'},
        {'AttributeName': 'ExtensionName', 'AttributeType': 'S'},
        {'AttributeName': 'OrgID', 'AttributeType': 'S'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

TRANSLATION_CACHE_TABLE_SCHEMA = {
    'TableName': 'TranslationCache',
    'KeySchema': [
        {'AttributeName': 'TranslationID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'TranslationID', 'AttributeType': 'S'},
        {'AttributeName': 'OriginalText', 'AttributeType': 'S'},
        {'AttributeName': 'TranslatedText', 'AttributeType': 'S'},
        {'AttributeName': 'Language', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

FAQS_TABLE_SCHEMA = {
    'TableName': 'FAQs',
    'KeySchema': [
        {'AttributeName': 'FAQID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'FAQID', 'AttributeType': 'S'},
        {'AttributeName': 'Question', 'AttributeType': 'S'},
        {'AttributeName': 'Answer', 'AttributeType': 'S'},
        {'AttributeName': 'ServiceID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SERVICE_EXTENSIONS_TABLE_SCHEMA = {
    'TableName': 'ServiceExtensions',
    'KeySchema': [
        {'AttributeName': 'ServiceExtensionID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ServiceExtensionID', 'AttributeType': 'S'},
        {'AttributeName': 'ServiceID', 'AttributeType': 'S'},
        {'AttributeName': 'ExtensionID', 'AttributeType': 'S'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
        {'AttributeName': 'OrgID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

AUDIT_TRAIL_FOR_FILES_TABLE_SCHEMA = {
    'TableName': 'AuditTrailForFiles',
    'KeySchema': [
        {'AttributeName': 'AuditFileID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'AuditFileID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'FileID', 'AttributeType': 'S'},
        {'AttributeName': 'ActionType', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_ACTIVITY_LOG_TABLE_SCHEMA = {
    'TableName': 'UserActivityLog',
    'KeySchema': [
        {'AttributeName': 'ActivityID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ActivityID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'ActivityType', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
        {'AttributeName': 'Details', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

CUSTOMER_SUPPORT_LOG_TABLE_SCHEMA = {
    'TableName': 'CustomerSupportLog',
    'KeySchema': [
        {'AttributeName': 'SupportLogID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'SupportLogID', 'AttributeType': 'S'},
        {'AttributeName': 'AgentID', 'AttributeType': 'S'},
        {'AttributeName': 'CustomerID', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
        {'AttributeName': 'InteractionType', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

LANGUAGE_SUPPORT_TABLE_SCHEMA = {
    'TableName': 'LanguageSupport',
    'KeySchema': [
        {'AttributeName': 'LanguageID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'LanguageID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_ROLE_MAPPINGS_TABLE_SCHEMA = {
    'TableName': 'UserRoleMappings',
    'KeySchema': [
        {'AttributeName': 'UserRoleMappingID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserRoleMappingID', 'AttributeType': 'S'},
        {'AttributeName': 'UserTypeID', 'AttributeType': 'S'},
        {'AttributeName': 'RoleID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

ROLES_TABLE_SCHEMA = {
    'TableName': 'Roles',
    'KeySchema': [
        {'AttributeName': 'RoleID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'RoleID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SUBSCRIPTION_HISTORY_TABLE_SCHEMA = {
    'TableName': 'SubscriptionHistory',
    'KeySchema': [
        {'AttributeName': 'SubscriptionHistoryID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'SubscriptionHistoryID', 'AttributeType': 'S'},
        {'AttributeName': 'OrgID', 'AttributeType': 'S'},
        {'AttributeName': 'OldTierID', 'AttributeType': 'S'},
        {'AttributeName': 'NewTierID', 'AttributeType': 'S'},
        {'AttributeName': 'ChangeTimestamp', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

THIRD_PARTY_INTEGRATIONS_TABLE_SCHEMA = {
    'TableName': 'ThirdPartyIntegrations',
    'KeySchema': [
        {'AttributeName': 'IntegrationID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'IntegrationID', 'AttributeType': 'S'},
        {'AttributeName': 'ServiceName', 'AttributeType': 'S'},
        {'AttributeName': 'APIKey', 'AttributeType': 'S'},
        {'AttributeName': 'SettingsJSON', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

WIDGETS_TABLE_SCHEMA = {
    'TableName': 'Widgets',
    'KeySchema': [
        {'AttributeName': 'WidgetID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'WidgetID', 'AttributeType': 'S'},
        {'AttributeName': 'WidgetName', 'AttributeType': 'S'},
        {'AttributeName': 'ServiceID', 'AttributeType': 'S'},
        {'AttributeName': 'ConfigJSON', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_SAVED_MESSAGES_TABLE_SCHEMA = {
    'TableName': 'UserSavedMessages',
    'KeySchema': [
        {'AttributeName': 'SavedMessageID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'SavedMessageID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'MessageID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_NOTIFICATION_SETTINGS_TABLE_SCHEMA = {
    'TableName': 'UserNotificationSettings',
    'KeySchema': [
        {'AttributeName': 'UserNotificationSettingID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserNotificationSettingID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'NotificationType', 'AttributeType': 'S'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

API_AUDIT_LOG_TABLE_SCHEMA = {
    'TableName': 'APIAuditLog',
    'KeySchema': [
        {'AttributeName': 'APIAuditID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'APIAuditID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'APIEndpoint', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
        {'AttributeName': 'ResponseCode', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SCHEDULED_TASKS_TABLE_SCHEMA = {
    'TableName': 'ScheduledTasks',
    'KeySchema': [
        {'AttributeName': 'TaskID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'TaskID', 'AttributeType': 'S'},
        {'AttributeName': 'TaskName', 'AttributeType': 'S'},
        {'AttributeName': 'CronExpression', 'AttributeType': 'S'},
        {'AttributeName': 'LastRun', 'AttributeType': 'S'},
        {'AttributeName': 'NextRun', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

WEBHOOKS_TABLE_SCHEMA = {
    'TableName': 'Webhooks',
    'KeySchema': [
        {'AttributeName': 'WebhookID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'WebhookID', 'AttributeType': 'S'},
        {'AttributeName': 'ServiceName', 'AttributeType': 'S'},
        {'AttributeName': 'WebhookURL', 'AttributeType': 'S'},
        {'AttributeName': 'SecretToken', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

DATA_RETENTION_POLICIES_TABLE_SCHEMA = {
    'TableName': 'DataRetentionPolicies',
    'KeySchema': [
        {'AttributeName': 'PolicyID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'PolicyID', 'AttributeType': 'S'},
        {'AttributeName': 'DataType', 'AttributeType': 'S'},
        {'AttributeName': 'RetentionPeriod', 'AttributeType': 'S'},
        {'AttributeName': 'InstanceType', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

EMAIL_TEMPLATES_TABLE_SCHEMA = {
    'TableName': 'EmailTemplates',
    'KeySchema': [
        {'AttributeName': 'TemplateID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'TemplateID', 'AttributeType': 'S'},
        {'AttributeName': 'TemplateName', 'AttributeType': 'S'},
        {'AttributeName': 'Subject', 'AttributeType': 'S'},
        {'AttributeName': 'Body', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

INVOICING_TABLE_SCHEMA = {
    'TableName': 'Invoicing',
    'KeySchema': [
        {'AttributeName': 'InvoiceID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'InvoiceID', 'AttributeType': 'S'},
        {'AttributeName': 'BillingID', 'AttributeType': 'S'},
        {'AttributeName': 'InvoiceDate', 'AttributeType': 'S'},
        {'AttributeName': 'Amount', 'AttributeType': 'N'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

PAYMENT_HISTORY_TABLE_SCHEMA = {
    'TableName': 'PaymentHistory',
    'KeySchema': [
        {'AttributeName': 'PaymentID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'PaymentID', 'AttributeType': 'S'},
        {'AttributeName': 'BillingID', 'AttributeType': 'S'},
        {'AttributeName': 'PaymentDate', 'AttributeType': 'S'},
        {'AttributeName': 'Amount', 'AttributeType': 'N'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

ERROR_LOGS_TABLE_SCHEMA = {
    'TableName': 'ErrorLogs',
    'KeySchema': [
        {'AttributeName': 'ErrorLogID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ErrorLogID', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
        {'AttributeName': 'ErrorType', 'AttributeType': 'S'},
        {'AttributeName': 'Details', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

FEEDBACK_AND_RATINGS_TABLE_SCHEMA = {
    'TableName': 'FeedbackAndRatings',
    'KeySchema': [
        {'AttributeName': 'FeedbackID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'FeedbackID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'ServiceID', 'AttributeType': 'S'},
        {'AttributeName': 'Rating', 'AttributeType': 'N'},
        {'AttributeName': 'Comments', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

CHAT_BOT_SESSIONS_TABLE_SCHEMA = {
    'TableName': 'ChatBotSessions',
    'KeySchema': [
        {'AttributeName': 'SessionID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'SessionID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

MACHINE_LEARNING_MODELS_TABLE_SCHEMA = {
    'TableName': 'MachineLearningModels',
    'KeySchema': [
        {'AttributeName': 'ModelID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ModelID', 'AttributeType': 'S'},
        {'AttributeName': 'ModelName', 'AttributeType': 'S'},
        {'AttributeName': 'Version', 'AttributeType': 'S'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

DEVICE_MANAGEMENT_TABLE_SCHEMA = {
    'TableName': 'DeviceManagement',
    'KeySchema': [
        {'AttributeName': 'DeviceID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'DeviceID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'DeviceType', 'AttributeType': 'S'},
        {'AttributeName': 'LastAccessed', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

GEO_LOCATIONS_TABLE_SCHEMA = {
    'TableName': 'GeoLocations',
    'KeySchema': [
        {'AttributeName': 'LocationID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'LocationID', 'AttributeType': 'S'},
        {'AttributeName': 'Latitude', 'AttributeType': 'N'},
        {'AttributeName': 'Longitude', 'AttributeType': 'N'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

TAGS_TABLE_SCHEMA = {
    'TableName': 'Tags',
    'KeySchema': [
        {'AttributeName': 'TagID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'TagID', 'AttributeType': 'S'},
        {'AttributeName': 'TagName', 'AttributeType': 'S'},
        {'AttributeName': 'TagDescription', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

TAG_ASSOCIATIONS_TABLE_SCHEMA = {
    'TableName': 'TagAssociations',
    'KeySchema': [
        {'AttributeName': 'TagAssociationID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'TagAssociationID', 'AttributeType': 'S'},
        {'AttributeName': 'TagID', 'AttributeType': 'S'},
        {'AttributeName': 'EntityID', 'AttributeType': 'S'},
        {'AttributeName': 'EntityType', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

RESOURCE_QUOTAS_TABLE_SCHEMA = {
    'TableName': 'ResourceQuotas',
    'KeySchema': [
        {'AttributeName': 'QuotaID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'QuotaID', 'AttributeType': 'S'},
        {'AttributeName': 'ResourceType', 'AttributeType': 'S'},
        {'AttributeName': 'Limit', 'AttributeType': 'N'},
        {'AttributeName': 'UserTypeID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SESSION_TOKENS_TABLE_SCHEMA = {
    'TableName': 'SessionTokens',
    'KeySchema': [
        {'AttributeName': 'SessionTokenID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'SessionTokenID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'SessionToken', 'AttributeType': 'S'},
        {'AttributeName': 'ExpiryTime', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SEARCH_HISTORY_TABLE_SCHEMA = {
    'TableName': 'SearchHistory',
    'KeySchema': [
        {'AttributeName': 'SearchID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'SearchID', 'AttributeType': 'S'},  # Assuming 'SearchID' is a unique identifier
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'SearchQuery', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,    # Adjust based on your read requirements
        'WriteCapacityUnits': 5    # Adjust based on your write requirements
    },
}

SYSTEM_NOTIFICATIONS_TABLE_SCHEMA = {
    'TableName': 'SystemNotifications',
    'KeySchema': [
        {'AttributeName': 'NotificationID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'NotificationID', 'AttributeType': 'S'},
        {'AttributeName': 'Message', 'AttributeType': 'S'},
        {'AttributeName': 'Type', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SENSITIVE_DATA_AUDIT_TABLE_SCHEMA = {
    'TableName': 'SensitiveDataAudit',
    'KeySchema': [
        {'AttributeName': 'SensitiveDataAuditID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'SensitiveDataAuditID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'AccessTime', 'AttributeType': 'S'},
        {'AttributeName': 'DataType', 'AttributeType': 'S'},
        {'AttributeName': 'Action', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_PREFERENCES_TABLE_SCHEMA = {
    'TableName': 'UserPreferences',
    'KeySchema': [
        {'AttributeName': 'UserPreferenceID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserPreferenceID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'PreferenceType', 'AttributeType': 'S'},
        {'AttributeName': 'PreferenceValue', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

ANALYTICS_DASHBOARD_TABLE_SCHEMA = {
    'TableName': 'AnalyticsDashboard',
    'KeySchema': [
        {'AttributeName': 'DashboardID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'DashboardID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'ConfigJSON', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

REPORT_GENERATION_TABLE_SCHEMA = {
    'TableName': 'ReportGeneration',
    'KeySchema': [
        {'AttributeName': 'ReportID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ReportID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'ReportType', 'AttributeType': 'S'},
        {'AttributeName': 'GenerationTimestamp', 'AttributeType': 'S'},
        {'AttributeName': 'FileID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SHORT_LINKS_TABLE_SCHEMA = {
    'TableName': 'ShortLinks',
    'KeySchema': [
        {'AttributeName': 'ShortLinkID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ShortLinkID', 'AttributeType': 'S'},
        {'AttributeName': 'OriginalURL', 'AttributeType': 'S'},
        {'AttributeName': 'ShortURL', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_VERIFICATION_TABLE_SCHEMA = {
    'TableName': 'UserVerification',
    'KeySchema': [
        {'AttributeName': 'VerificationID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'VerificationID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'VerificationCode', 'AttributeType': 'S'},
        {'AttributeName': 'ExpiryTime', 'AttributeType': 'S'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}


CONTENT_MODERATION_TABLE_SCHEMA = {
    'TableName': 'ContentModeration',
    'KeySchema': [
        {'AttributeName': 'ModerationID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ModerationID', 'AttributeType': 'S'},
        {'AttributeName': 'ContentID', 'AttributeType': 'S'},
        {'AttributeName': 'ModeratorID', 'AttributeType': 'S'},
        {'AttributeName': 'Action', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

CAMPAIGNS_TABLE_SCHEMA = {
    'TableName': 'Campaigns',
    'KeySchema': [
        {'AttributeName': 'CampaignID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'CampaignID', 'AttributeType': 'S'},
        {'AttributeName': 'CampaignName', 'AttributeType': 'S'},
        {'AttributeName': 'StartDate', 'AttributeType': 'S'},
        {'AttributeName': 'EndDate', 'AttributeType': 'S'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

COUPONS_TABLE_SCHEMA = {
    'TableName': 'Coupons',
    'KeySchema': [
        {'AttributeName': 'CouponID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'CouponID', 'AttributeType': 'S'},
        {'AttributeName': 'CouponCode', 'AttributeType': 'S'},
        {'AttributeName': 'DiscountAmount', 'AttributeType': 'N'},
        {'AttributeName': 'ExpiryDate', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

PUSH_NOTIFICATIONS_TABLE_SCHEMA = {
    'TableName': 'PushNotifications',
    'KeySchema': [
        {'AttributeName': 'NotificationID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'NotificationID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'Message', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

EVENT_LOGGING_TABLE_SCHEMA = {
    'TableName': 'EventLogging',
    'KeySchema': [
        {'AttributeName': 'EventID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'EventID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'EventType', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
        {'AttributeName': 'AdditionalDetails', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

TEMPORARY_FILES_TABLE_SCHEMA = {
    'TableName': 'TemporaryFiles',
    'KeySchema': [
        {'AttributeName': 'TempFileID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'TempFileID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'FileName', 'AttributeType': 'S'},
        {'AttributeName': 'ExpirationTime', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

AB_TESTING_TABLE_SCHEMA = {
    'TableName': 'A-BTesting',
    'KeySchema': [
        {'AttributeName': 'TestID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'TestID', 'AttributeType': 'S'},
        {'AttributeName': 'FeatureID', 'AttributeType': 'S'},
        {'AttributeName': 'GroupName', 'AttributeType': 'S'},
        {'AttributeName': 'StartDate', 'AttributeType': 'S'},
        {'AttributeName': 'EndDate', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

PRODUCT_CATALOG_TABLE_SCHEMA = {
    'TableName': 'ProductCatalog',
    'KeySchema': [
        {'AttributeName': 'ProductID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ProductID', 'AttributeType': 'S'},
        {'AttributeName': 'ProductName', 'AttributeType': 'S'},
        {'AttributeName': 'ProductDescription', 'AttributeType': 'S'},
        {'AttributeName': 'Price', 'AttributeType': 'N'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SHOPPING_CART_TABLE_SCHEMA = {
    'TableName': 'ShoppingCart',
    'KeySchema': [
        {'AttributeName': 'CartID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'CartID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'ProductID', 'AttributeType': 'S'},
        {'AttributeName': 'Quantity', 'AttributeType': 'N'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

WISHLIST_TABLE_SCHEMA = {
    'TableName': 'Wishlist',
    'KeySchema': [
        {'AttributeName': 'WishlistID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'WishlistID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'ProductID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_ACHIEVEMENTS_TABLE_SCHEMA = {
    'TableName': 'UserAchievements',
    'KeySchema': [
        {'AttributeName': 'AchievementID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'AchievementID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'AchievementName', 'AttributeType': 'S'},
        {'AttributeName': 'DateEarned', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SOCIAL_INTERACTIONS_TABLE_SCHEMA = {
    'TableName': 'Social_Interactions',
    'KeySchema': [
        {'AttributeName': 'InteractionID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'Timestamp', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'InteractionID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'ContentID', 'AttributeType': 'S'},
        {'AttributeName': 'InteractionType', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

INVENTORY_MANAGEMENT_TABLE_SCHEMA = {
    'TableName': 'Inventory_Management',
    'KeySchema': [
        {'AttributeName': 'ProductID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'StockDate', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ProductID', 'AttributeType': 'S'},
        {'AttributeName': 'StockDate', 'AttributeType': 'S'},
        {'AttributeName': 'StockCount', 'AttributeType': 'N'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

ORDER_HISTORY_TABLE_SCHEMA = {
    'TableName': 'OrderHistory',
    'KeySchema': [
        {'AttributeName': 'OrderID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'OrderDate', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'OrderID', 'AttributeType': 'S'},
        {'AttributeName': 'OrderDate', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'ProductIDs', 'AttributeType': 'SS'},
        {'AttributeName': 'TotalAmount', 'AttributeType': 'N'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_REVIEWS_TABLE_SCHEMA = {
    'TableName': 'User_Reviews',
    'KeySchema': [
        {'AttributeName': 'ReviewID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'UserID', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ReviewID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'ProductID', 'AttributeType': 'S'},
        {'AttributeName': 'Rating', 'AttributeType': 'N'},
        {'AttributeName': 'ReviewText', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

DATA_ARCHIVES_TABLE_SCHEMA = {
    'TableName': 'Data_Archives',
    'KeySchema': [
        {'AttributeName': 'ArchiveID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'ArchiveDate', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ArchiveID', 'AttributeType': 'S'},
        {'AttributeName': 'ArchiveDate', 'AttributeType': 'S'},
        {'AttributeName': 'DataType', 'AttributeType': 'S'},
        {'AttributeName': 'DataID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

CUSTOMIZATIONS_TABLE_SCHEMA = {
    'TableName': 'Customizations',
    'KeySchema': [
        {'AttributeName': 'UserID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'CustomizationType', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'CustomizationType', 'AttributeType': 'S'},
        {'AttributeName': 'SettingsJSON', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

TAXONOMIES_TABLE_SCHEMA = {
    'TableName': 'Taxonomies',
    'KeySchema': [
        {'AttributeName': 'CategoryID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'CategoryID', 'AttributeType': 'S'},
        {'AttributeName': 'ParentCategoryID', 'AttributeType': 'S'},
        {'AttributeName': 'CategoryName', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

BOOKMARKS_FAVORITES_TABLE_SCHEMA = {
    'TableName': 'Bookmarks-Favorites',
    'KeySchema': [
        {'AttributeName': 'UserID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'ContentID', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'ContentID', 'AttributeType': 'S'},
        {'AttributeName': 'BookmarkDate', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

NOTIFICATIONS_TABLE_SCHEMA = {
    'TableName': 'Notifications',
    'KeySchema': [
        {'AttributeName': 'NotificationID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'UserID', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'NotificationID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'NotificationType', 'AttributeType': 'S'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SECURITY_POLICIES_TABLE_SCHEMA = {
    'TableName': 'Security_Policies',
    'KeySchema': [
        {'AttributeName': 'PolicyID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'PolicyID', 'AttributeType': 'S'},
        {'AttributeName': 'PolicyJSON', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_JOURNEY_FUNNEL_TABLE_SCHEMA = {
    'TableName': 'User_Journey_Funnel',
    'KeySchema': [
        {'AttributeName': 'UserID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'StepID', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'StepID', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

COMPLIANCE_RECORDS_TABLE_SCHEMA = {
    'TableName': 'Compliance_Records',
    'KeySchema': [
        {'AttributeName': 'RecordID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'ComplianceDate', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'RecordID', 'AttributeType': 'S'},
        {'AttributeName': 'ComplianceDate', 'AttributeType': 'S'},
        {'AttributeName': 'ComplianceType', 'AttributeType': 'S'},
        {'AttributeName': 'Details', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SCHEDULED_REPORTS_TABLE_SCHEMA = {
    'TableName': 'Scheduled_Reports',
    'KeySchema': [
        {'AttributeName': 'UserID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'ReportID', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'ReportID', 'AttributeType': 'S'},
        {'AttributeName': 'ScheduleDate', 'AttributeType': 'S'},
        {'AttributeName': 'ReportType', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

AFFILIATE_PROGRAMS_TABLE_SCHEMA = {
    'TableName': 'Affiliate_Programs',
    'KeySchema': [
        {'AttributeName': 'AffiliateID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'AffiliateID', 'AttributeType': 'S'},
        {'AttributeName': 'ReferralLink', 'AttributeType': 'S'},
        {'AttributeName': 'Commission', 'AttributeType': 'N'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

CHAT_MESSAGING_ARCHIVES_TABLE_SCHEMA = {
    'TableName': 'Chat-Messaging_Archives',
    'KeySchema': [
        {'AttributeName': 'ChatID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'ArchiveDate', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ChatID', 'AttributeType': 'S'},
        {'AttributeName': 'ArchiveDate', 'AttributeType': 'S'},
        {'AttributeName': 'UserIDs', 'AttributeType': 'S'},
        {'AttributeName': 'MessageCount', 'AttributeType': 'N'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_CERTIFICATES_TABLE_SCHEMA = {
    'TableName': 'UserCertificates',
    'KeySchema': [
        {'AttributeName': 'CertificateID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'UserID', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'CertificateID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'CourseID', 'AttributeType': 'S'},
        {'AttributeName': 'IssueDate', 'AttributeType': 'S'},
        {'AttributeName': 'ExpiryDate', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

FORUMS_TABLE_SCHEMA = {
    'TableName': 'Forums',
    'KeySchema': [
        {'AttributeName': 'ForumID', 'KeyType': 'HASH'},  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ForumID', 'AttributeType': 'S'},
        {'AttributeName': 'Title', 'AttributeType': 'S'},
        {'AttributeName': 'Description', 'AttributeType': 'S'},
        {'AttributeName': 'CategoryID', 'AttributeType': 'S'},
        {'AttributeName': 'Moderators', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

FORUM_POSTS_TABLE_SCHEMA = {
    'TableName': 'ForumPosts',
    'KeySchema': [
        {'AttributeName': 'PostID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'ForumID', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'PostID', 'AttributeType': 'S'},
        {'AttributeName': 'ForumID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'Content', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_BADGES_TABLE_SCHEMA = {
    'TableName': 'UserBadges',
    'KeySchema': [
        {'AttributeName': 'BadgeID', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'UserID', 'KeyType': 'RANGE'},  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'BadgeID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'BadgeName', 'AttributeType': 'S'},
        {'AttributeName': 'IssueDate', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

EVENTS_TABLE_SCHEMA = {
    'TableName': 'Events',
    'KeySchema': [
        {'AttributeName': 'EventID', 'KeyType': 'HASH'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'EventID', 'AttributeType': 'S'},
        {'AttributeName': 'Title', 'AttributeType': 'S'},
        {'AttributeName': 'Description', 'AttributeType': 'S'},
        {'AttributeName': 'StartTime', 'AttributeType': 'S'},
        {'AttributeName': 'EndTime', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_EVENTS_TABLE_SCHEMA = {
    'TableName': 'UserEvents',
    'KeySchema': [
        {'AttributeName': 'UserID', 'KeyType': 'HASH'},
        {'AttributeName': 'EventID', 'KeyType': 'RANGE'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'EventID', 'AttributeType': 'S'},
        {'AttributeName': 'RSVPStatus', 'AttributeType': 'S'},
        {'AttributeName': 'AttendanceStatus', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SURVEYS_TABLE_SCHEMA = {
    'TableName': 'Surveys',
    'KeySchema': [
        {'AttributeName': 'SurveyID', 'KeyType': 'HASH'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'SurveyID', 'AttributeType': 'S'},
        {'AttributeName': 'Title', 'AttributeType': 'S'},
        {'AttributeName': 'Description', 'AttributeType': 'S'},
        {'AttributeName': 'QuestionsJSON', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SURVEY_RESPONSES_TABLE_SCHEMA = {
    'TableName': 'SurveyResponses',
    'KeySchema': [
        {'AttributeName': 'ResponseID', 'KeyType': 'HASH'},
        {'AttributeName': 'SurveyID', 'KeyType': 'RANGE'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ResponseID', 'AttributeType': 'S'},
        {'AttributeName': 'SurveyID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'AnswersJSON', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_GROUPS_TABLE_SCHEMA = {
    'TableName': 'UserGroups',
    'KeySchema': [
        {'AttributeName': 'GroupID', 'KeyType': 'HASH'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'GroupID', 'AttributeType': 'S'},
        {'AttributeName': 'GroupName', 'AttributeType': 'S'},
        {'AttributeName': 'Description', 'AttributeType': 'S'},
        {'AttributeName': 'Admins', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

GROUP_MEMBERS_TABLE_SCHEMA = {
    'TableName': 'GroupMembers',
    'KeySchema': [
        {'AttributeName': 'GroupID', 'KeyType': 'HASH'},
        {'AttributeName': 'UserID', 'KeyType': 'RANGE'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'GroupID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'MemberRole', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}


USER_NOTES_TABLE_SCHEMA = {
    'TableName': 'UserNotes',
    'KeySchema': [
        {'AttributeName': 'NoteID', 'KeyType': 'HASH'},
        {'AttributeName': 'UserID', 'KeyType': 'RANGE'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'NoteID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'Content', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

DISCUSSIONS_TABLE_SCHEMA = {
    'TableName': 'Discussions',
    'KeySchema': [
        {'AttributeName': 'DiscussionID', 'KeyType': 'HASH'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'DiscussionID', 'AttributeType': 'S'},
        {'AttributeName': 'Topic', 'AttributeType': 'S'},
        {'AttributeName': 'Description', 'AttributeType': 'S'},
        {'AttributeName': 'Participants', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

DISCUSSION_COMMENTS_TABLE_SCHEMA = {
    'TableName': 'DiscussionComments',
    'KeySchema': [
        {'AttributeName': 'CommentID', 'KeyType': 'HASH'},
        {'AttributeName': 'DiscussionID', 'KeyType': 'RANGE'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'CommentID', 'AttributeType': 'S'},
        {'AttributeName': 'DiscussionID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'Content', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

FAQ_CATEGORIES_TABLE_SCHEMA = {
    'TableName': 'FAQCategories',
    'KeySchema': [
        {'AttributeName': 'CategoryID', 'KeyType': 'HASH'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'CategoryID', 'AttributeType': 'S'},
        {'AttributeName': 'CategoryName', 'AttributeType': 'S'},
        {'AttributeName': 'Description', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

FAQ_ITEMS_TABLE_SCHEMA = {
    'TableName': 'FAQItems',
    'KeySchema': [
        {'AttributeName': 'FAQID', 'KeyType': 'HASH'},
        {'AttributeName': 'CategoryID', 'KeyType': 'RANGE'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'FAQID', 'AttributeType': 'S'},
        {'AttributeName': 'CategoryID', 'AttributeType': 'S'},
        {'AttributeName': 'Question', 'AttributeType': 'S'},
        {'AttributeName': 'Answer', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_BOOKMARKS_TABLE_SCHEMA = {
    'TableName': 'UserBookmarks',
    'KeySchema': [
        {'AttributeName': 'UserID', 'KeyType': 'HASH'},
        {'AttributeName': 'ContentID', 'KeyType': 'RANGE'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'ContentID', 'AttributeType': 'S'},
        {'AttributeName': 'BookmarkDate', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_HISTORY_TABLE_SCHEMA = {
    'TableName': 'UserHistory',
    'KeySchema': [
        {'AttributeName': 'UserID', 'KeyType': 'HASH'},
        {'AttributeName': 'Timestamp', 'KeyType': 'RANGE'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
        {'AttributeName': 'AccessedContent', 'AttributeType': 'S'},
        {'AttributeName': 'ActionType', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

RESOURCE_FOLDERS_TABLE_SCHEMA = {
    'TableName': 'ResourceFolders',
    'KeySchema': [
        {'AttributeName': 'FolderID', 'KeyType': 'HASH'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'FolderID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

RESOURCE_FILES_TABLE_SCHEMA = {
    'TableName': 'ResourceFiles',
    'KeySchema': [
        {'AttributeName': 'FileID', 'KeyType': 'HASH'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'FileID', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_FEEDBACK_TABLE_SCHEMA = {
    'TableName': 'UserFeedback',
    'KeySchema': [
        {'AttributeName': 'FeedbackID', 'KeyType': 'HASH'},
        {'AttributeName': 'UserID', 'KeyType': 'RANGE'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'FeedbackID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'Rating', 'AttributeType': 'N'},
        {'AttributeName': 'Comments', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SYSTEM_SETTINGS_TABLE_SCHEMA = {
    'TableName': 'SystemSettings',
    'KeySchema': [
        {'AttributeName': 'SettingID', 'KeyType': 'HASH'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'SettingID', 'AttributeType': 'S'},
        {'AttributeName': 'SettingName', 'AttributeType': 'S'},
        {'AttributeName': 'Value', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

SYSTEM_LOGS_TABLE_SCHEMA = {
    'TableName': 'SystemLogs',
    'KeySchema': [
        {'AttributeName': 'LogID', 'KeyType': 'HASH'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'LogID', 'AttributeType': 'S'},
        {'AttributeName': 'EventType', 'AttributeType': 'S'},
        {'AttributeName': 'Details', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_ALERTS_TABLE_SCHEMA = {
    'TableName': 'UserAlerts',
    'KeySchema': [
        {'AttributeName': 'AlertID', 'KeyType': 'HASH'},
        {'AttributeName': 'UserID', 'KeyType': 'RANGE'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'AlertID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'AlertType', 'AttributeType': 'S'},
        {'AttributeName': 'Message', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

FILE_PERMISSIONS_TABLE_SCHEMA = {
    'TableName': 'FilePermissions',
    'KeySchema': [
        {'AttributeName': 'FileID', 'KeyType': 'HASH'},
        {'AttributeName': 'UserID', 'KeyType': 'RANGE'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'FileID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'file_url', 'AttributeType': 'S'},
        {'AttributeName': 'permissions', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

QUERY_TABLE_SCHEMA = {
    'TableName': 'QueryTable',
    'KeySchema': [
        {'AttributeName': 'QueryID', 'KeyType': 'HASH'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'QueryID', 'AttributeType': 'S'},
        {'AttributeName': 'query_text', 'AttributeType': 'S'},
        {'AttributeName': 'query_results', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

DOCUMENT_TABLE_SCHEMA = {
    'TableName': 'DocumentTable',
    'KeySchema': [
        {'AttributeName': 'DocumentID', 'KeyType': 'HASH'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'DocumentID', 'AttributeType': 'S'},
        {'AttributeName': 'document_text', 'AttributeType': 'S'},
        {'AttributeName': 'document_metadata', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_PROGRESS_TABLE_SCHEMA = {
    'TableName': 'UserProgress',
    'KeySchema': [
        {'AttributeName': 'UserID', 'KeyType': 'HASH'},        # Partition key
        {'AttributeName': 'ContentID', 'KeyType': 'RANGE'},    # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'ContentID', 'AttributeType': 'S'},
        {'AttributeName': 'Progress', 'AttributeType': 'N'},    # Assuming Progress is a numeric value
        {'AttributeName': 'LastAccessed', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

USER_PROGRESS_TABLE_SCHEMA = {
    'TableName': 'UserProgress',
    'KeySchema': [
        {'AttributeName': 'UserID', 'KeyType': 'HASH'},       # Partition key
        {'AttributeName': 'ContentID', 'KeyType': 'RANGE'}   # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'ContentID', 'AttributeType': 'S'},
        {'AttributeName': 'Progress', 'AttributeType': 'N'},
        {'AttributeName': 'LastAccessed', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

FAILED_LOGIN_ATTEMPTS_TABLE_SCHEMA = {
    'TableName': 'FailedLoginAttempts',
    'KeySchema': [
        {'AttributeName': 'AttemptID', 'KeyType': 'HASH'}  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'AttemptID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'IPAddress', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

RATE_LIMITING_TABLE_SCHEMA = {
    'TableName': 'RateLimiting',
    'KeySchema': [
        {'AttributeName': 'RateLimitID', 'KeyType': 'HASH'}  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'RateLimitID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'APIEndpoint', 'AttributeType': 'S'},
        {'AttributeName': 'Timestamp', 'AttributeType': 'S'},
        {'AttributeName': 'CallCount', 'AttributeType': 'N'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

DATA_EXPORTS_TABLE_SCHEMA = {
    'TableName': 'DataExports',
    'KeySchema': [
        {'AttributeName': 'ExportID', 'KeyType': 'HASH'}  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ExportID', 'AttributeType': 'S'},
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'RequestDate', 'AttributeType': 'S'},
        {'AttributeName': 'CompletionDate', 'AttributeType': 'S'},
        {'AttributeName': 'Status', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

NEWSLETTER_SUBSCRIPTIONS_TABLE_SCHEMA = {
    'TableName': 'NewsletterSubscriptions',
    'KeySchema': [
        {'AttributeName': 'SubscriptionID', 'KeyType': 'HASH'}  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'SubscriptionID', 'AttributeType': 'S'},
        {'AttributeName': 'Email', 'AttributeType': 'S'},
        {'AttributeName': 'SubscriptionStatus', 'AttributeType': 'S'},
        {'AttributeName': 'OptInDate', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

PENDING_INVITATIONS_TABLE_SCHEMA = {
    'TableName': 'PendingInvitations',
    'KeySchema': [
        {'AttributeName': 'InvitationID', 'KeyType': 'HASH'}  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'InvitationID', 'AttributeType': 'S'},
        {'AttributeName': 'Email', 'AttributeType': 'S'},
        {'AttributeName': 'InvitationCode', 'AttributeType': 'S'},
        {'AttributeName': 'ExpirationDate', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

LEARNING_MANAGEMENT_TABLE_SCHEMA = {
    'TableName': 'LearningManagement',
    'KeySchema': [
        {'AttributeName': 'UserID', 'KeyType': 'HASH'},     # Partition key
        {'AttributeName': 'CourseID', 'KeyType': 'RANGE'}  # Sort key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'CourseID', 'AttributeType': 'S'},
        {'AttributeName': 'Progress', 'AttributeType': 'N'},
        {'AttributeName': 'Scores', 'AttributeType': 'N'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

COURSE_TABLE_SCHEMA = {
    'TableName': 'Course',
    'KeySchema': [
        {'AttributeName': 'CourseID', 'KeyType': 'HASH'}  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'CourseID', 'AttributeType': 'S'},
        {'AttributeName': 'CourseName', 'AttributeType': 'S'},
        {'AttributeName': 'Category', 'AttributeType': 'S'},
        {'AttributeName': 'Description', 'AttributeType': 'S'},
        {'AttributeName': 'Duration', 'AttributeType': 'N'},
        {'AttributeName': 'Level', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

GAMIFICATION_TABLE_SCHEMA = {
    'TableName': 'Gamification',
    'KeySchema': [
        {'AttributeName': 'UserID', 'KeyType': 'HASH'}  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserID', 'AttributeType': 'S'},
        {'AttributeName': 'Points', 'AttributeType': 'N'},
        {'AttributeName': 'Level', 'AttributeType': 'N'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

COURSE_CONTENT_TABLE_SCHEMA = {
    'TableName': 'CourseContent',
    'KeySchema': [
        {'AttributeName': 'ContentID', 'KeyType': 'HASH'}  # Partition key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ContentID', 'AttributeType': 'S'},
        {'AttributeName': 'CourseID', 'AttributeType': 'S'},
        {'AttributeName': 'Section', 'AttributeType': 'S'},
        {'AttributeName': 'Lecture', 'AttributeType': 'S'},
        {'AttributeName': 'Duration', 'AttributeType': 'N'},
        {'AttributeName': 'MediaType', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
}

GUEST_LANGUAGE_PREFERENCES_TABLE_SCHEMA = {
    'TableName': 'GuestLanguagePreferences',
    'KeySchema': [
        {'AttributeName': 'SessionID', 'KeyType': 'HASH'},  # Primary Key
        {'AttributeName': 'DeviceID', 'KeyType': 'RANGE'}   # Sort Key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'SessionID', 'AttributeType': 'S'},
        {'AttributeName': 'DeviceID', 'AttributeType': 'S'}
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
}

USER_LANGUAGE_PREFERENCES_TABLE_SCHEMA = {
    'TableName': 'UserLanguagePreferences',
    'KeySchema': [
        {'AttributeName': 'UserID', 'KeyType': 'HASH'}  # Primary Key
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'UserID', 'AttributeType': 'S'}
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
}