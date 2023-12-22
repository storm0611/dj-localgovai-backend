from utils.aws_s3 import s3_logger
from models.authentication import (
    User,
    Org
)
from models.communication import (
    Channel,
    ChatMessage,
    LanguageSupport,
    Feedback
)
from models.knowledge_base import (
    KnowledgeBase,
    KnowledgeBaseQuestion,
)
from models.user_manager import (
    Role,
    Team,
    TeamMember,
    UserPermission,
)
from models.file_manager import (
    ResourceFile,
    ResourceFolder
)

# Migrate Users Table
def init_users_table():
    try:
        exists = User.exists_table()
        if not exists:
            User.create_table()
            s3_logger.info(f"Table {User.table.name} created successfully.")
            print(f"Table {User.table.name} created successfully.")
        else:
            s3_logger.info(f"Table {User.table.name} already exists.")
            print(f"Table {User.table.name} already exists.")
    except:
        raise

# Migrate UserPermissions Table
def init_user_permissions_table():
    try:
        exists = UserPermission.exists_table()
        if not exists:
            UserPermission.create_table()
            s3_logger.info(f"Table {UserPermission.table.name} created successfully.")
            print(f"Table {UserPermission.table.name} created successfully.")
        else:
            s3_logger.info(f"Table {UserPermission.table.name} already exists.")
            print(f"Table {UserPermission.table.name} already exists.")
    except:
        raise

# Migrate Organizations Table
def init_orgs_table():
    try:
        exists = Org.exists_table()
        if not exists:
            Org.create_table()
            s3_logger.info(f"Table {Org.table.name} created successfully.")
            print(f"Table {Org.table.name} created successfully.")
        else:
            s3_logger.info(f"Table {Org.table.name} already exists.")
            print(f"Table {Org.table.name} already exists.")
    except:
        raise

# Migrate Feedbacks Table
def init_feedbacks_table():
    try:
        exists = Feedback.exists_table()
        if not exists:
            Feedback.create_table()
            s3_logger.info(f"Table {Feedback.table.name} created successfully.")
            print(f"Table {Feedback.table.name} created successfully.")
        else:
            s3_logger.info(f"Table {Feedback.table.name} already exists.")
            print(f"Table {Feedback.table.name} already exists.")
    except:
        raise

# Migrate Channels Table
def init_channels_table():
    try:
        exists = Channel.exists_table()
        if not exists:
            Channel.create_table()
            s3_logger.info(f"Table {Channel.table.name} created successfully.")
            print(f"Table {Channel.table.name} created successfully.")
        else:
            s3_logger.info(f"Table {Channel.table.name} already exists.")
            print(f"Table {Channel.table.name} already exists.")
    except:
        raise

# Migrate Messages Table
def init_messages_table():
    try:
        exists = ChatMessage.exists_table()
        if not exists:
            ChatMessage.create_table()
            s3_logger.info(f"Table {ChatMessage.table.name} created successfully.")
            print(f"Table {ChatMessage.table.name} created successfully.")
        else:
            s3_logger.info(f"Table {ChatMessage.table.name} already exists.")
            print(f"Table {ChatMessage.table.name} already exists.")
    except:
        raise

# Migrate KnowledgeBases Table
def init_knowledge_bases_table():
    try:
        exists = KnowledgeBase.exists_table()
        if not exists:
            KnowledgeBase.create_table()
            s3_logger.info(f"Table {KnowledgeBase.table.name} created successfully.")
            print(f"Table {KnowledgeBase.table.name} created successfully.")
        else:
            s3_logger.info(f"Table {KnowledgeBase.table.name} already exists.")
            print(f"Table {KnowledgeBase.table.name} already exists.")
    except:
        raise

# Migrate KnowledgeBaseQuestions Table
def init_knowledge_base_questions_table():
    try:
        exists = KnowledgeBaseQuestion.exists_table()
        if not exists:
            KnowledgeBaseQuestion.create_table()
            s3_logger.info(f"Table {KnowledgeBaseQuestion.table.name} created successfully.")
            print(f"Table {KnowledgeBaseQuestion.table.name} created successfully.")
        else:
            s3_logger.info(f"Table {KnowledgeBaseQuestion.table.name} already exists.")
            print(f"Table {KnowledgeBaseQuestion.table.name} already exists.")
    except:
        raise

# Migrate Teams Table
def init_teams_table():
    try:
        exists = Team.exists_table()
        if not exists:
            Team.create_table()
            s3_logger.info(f"Table {Team.table.name} created successfully.")
            print(f"Table {Team.table.name} created successfully.")
        else:
            s3_logger.info(f"Table {Team.table.name} already exists.")
            print(f"Table {Team.table.name} already exists.")
    except:
        raise

# Migrate TeamMembers Table
def init_team_members_table():
    try:
        exists = TeamMember.exists_table()
        if not exists:
            TeamMember.create_table()
            s3_logger.info(f"Table {TeamMember.table.name} created successfully.")
            print(f"Table {TeamMember.table.name} created successfully.")
        else:
            s3_logger.info(f"Table {TeamMember.table.name} already exists.")
            print(f"Table {TeamMember.table.name} already exists.")
    except:
        raise

# Migrate LanguageSupports Table
def init_language_support_table():
    SUPPORTED_LANGUAGES = {
        1: {'CountryCode': 'US', 'LanguageCode': 'en', 'LanguageName': 'English'},
        2: {'CountryCode': 'GB', 'LanguageCode': 'en', 'LanguageName': 'English'},
        3: {'CountryCode': 'FR', 'LanguageCode': 'fr', 'LanguageName': 'French'},
        4: {'CountryCode': 'DE', 'LanguageCode': 'de', 'LanguageName': 'German'},
        5: {'CountryCode': 'IT', 'LanguageCode': 'it', 'LanguageName': 'Italian'},
        6: {'CountryCode': 'ES', 'LanguageCode': 'es', 'LanguageName': 'Spanish'},
        7: {'CountryCode': 'CN', 'LanguageCode': 'zh', 'LanguageName': 'Chinese'},
        8: {'CountryCode': 'JP', 'LanguageCode': 'ja', 'LanguageName': 'Japanese'},
        9: {'CountryCode': 'RU', 'LanguageCode': 'ru', 'LanguageName': 'Russian'},
        10: {'CountryCode': 'BR', 'LanguageCode': 'pt', 'LanguageName': 'Portuguese'},
        11: {'CountryCode': 'NL', 'LanguageCode': 'nl', 'LanguageName': 'Dutch'},
        12: {'CountryCode': 'KR', 'LanguageCode': 'ko', 'LanguageName': 'Korean'},
        13: {'CountryCode': 'TR', 'LanguageCode': 'tr', 'LanguageName': 'Turkish'},
        14: {'CountryCode': 'AR', 'LanguageCode': 'ar', 'LanguageName': 'Arabic'},
        15: {'CountryCode': 'IL', 'LanguageCode': 'he', 'LanguageName': 'Hebrew'},
        16: {'CountryCode': 'SE', 'LanguageCode': 'sv', 'LanguageName': 'Swedish'},
        17: {'CountryCode': 'NO', 'LanguageCode': 'no', 'LanguageName': 'Norwegian'},
        18: {'CountryCode': 'PL', 'LanguageCode': 'pl', 'LanguageName': 'Polish'},
        19: {'CountryCode': 'RO', 'LanguageCode': 'ro', 'LanguageName': 'Romanian'},
        20: {'CountryCode': 'AU', 'LanguageCode': 'en', 'LanguageName': 'English'},
        21: {'CountryCode': 'CA', 'LanguageCode': 'en', 'LanguageName': 'English'},
        22: {'CountryCode': 'MX', 'LanguageCode': 'es', 'LanguageName': 'Spanish'},  # Mexico
        23: {'CountryCode': 'ZA', 'LanguageCode': 'af', 'LanguageName': 'Afrikaans'},  # South Africa
        24: {'CountryCode': 'AE', 'LanguageCode': 'ar', 'LanguageName': 'Arabic'},  # United Arab Emirates
        25: {'CountryCode': 'AM', 'LanguageCode': 'hy', 'LanguageName': 'Armenian'},  # Armenia
        26: {'CountryCode': 'AZ', 'LanguageCode': 'az', 'LanguageName': 'Azerbaijani'},  # Azerbaijan
        27: {'CountryCode': 'BY', 'LanguageCode': 'be', 'LanguageName': 'Belarusian'},  # Belarus
        28: {'CountryCode': 'BA', 'LanguageCode': 'bs', 'LanguageName': 'Bosnian'},  # Bosnia and Herzegovina
        29: {'CountryCode': 'BG', 'LanguageCode': 'bg', 'LanguageName': 'Bulgarian'},  # Bulgaria
        30: {'CountryCode': 'AD', 'LanguageCode': 'ca', 'LanguageName': 'Catalan'},  # Andorra
        31: {'CountryCode': 'HR', 'LanguageCode': 'hr', 'LanguageName': 'Croatian'},  # Croatia
        32: {'CountryCode': 'CZ', 'LanguageCode': 'cs', 'LanguageName': 'Czech'},  # Czech Republic
        33: {'CountryCode': 'DK', 'LanguageCode': 'da', 'LanguageName': 'Danish'},  # Denmark
        34: {'CountryCode': 'EE', 'LanguageCode': 'et', 'LanguageName': 'Estonian'},  # Estonia
        35: {'CountryCode': 'FI', 'LanguageCode': 'fi', 'LanguageName': 'Finnish'},  # Finland
        36: {'CountryCode': 'GL', 'LanguageCode': 'gl', 'LanguageName': 'Galician'},  # Greenland
        37: {'CountryCode': 'GR', 'LanguageCode': 'el', 'LanguageName': 'Greek'},  # Greece
        38: {'CountryCode': 'IL', 'LanguageCode': 'he', 'LanguageName': 'Hebrew'},  # Israel
        39: {'CountryCode': 'IS', 'LanguageCode': 'is', 'LanguageName': 'Icelandic'},  # Iceland
        40: {'CountryCode': 'ID', 'LanguageCode': 'id', 'LanguageName': 'Indonesian'},  # Indonesia
        41: {'CountryCode': 'KZ', 'LanguageCode': 'kk', 'LanguageName': 'Kazakh'},  # Kazakhstan
        42: {'CountryCode': 'LV', 'LanguageCode': 'lv', 'LanguageName': 'Latvian'},  # Latvia
        43: {'CountryCode': 'LT', 'LanguageCode': 'lt', 'LanguageName': 'Lithuanian'},  # Lithuania
        44: {'CountryCode': 'MK', 'LanguageCode': 'mk', 'LanguageName': 'Macedonian'},  # North Macedonia
        45: {'CountryCode': 'MY', 'LanguageCode': 'ms', 'LanguageName': 'Malay'},  # Malaysia
        46: {'CountryCode': 'NZ', 'LanguageCode': 'mi', 'LanguageName': 'Māori'},  # New Zealand
        47: {'CountryCode': 'NP', 'LanguageCode': 'ne', 'LanguageName': 'Nepali'},  # Nepal
        48: {'CountryCode': 'IR', 'LanguageCode': 'fa', 'LanguageName': 'Persian'},  # Iran
        49: {'CountryCode': 'RS', 'LanguageCode': 'sr', 'LanguageName': 'Serbian'},  # Serbia
        50: {'CountryCode': 'SK', 'LanguageCode': 'sk', 'LanguageName': 'Slovak'},  # Slovakia
        51: {'CountryCode': 'SI', 'LanguageCode': 'sl', 'LanguageName': 'Slovenian'},  # Slovenia
        52: {'CountryCode': 'KE', 'LanguageCode': 'sw', 'LanguageName': 'Swahili'},  # Kenya
        53: {'CountryCode': 'PH', 'LanguageCode': 'tl', 'LanguageName': 'Tagalog'},  # Philippines
        54: {'CountryCode': 'LK', 'LanguageCode': 'ta', 'LanguageName': 'Tamil'},  # Sri Lanka
        55: {'CountryCode': 'TH', 'LanguageCode': 'th', 'LanguageName': 'Thai'},  # Thailand
        56: {'CountryCode': 'UA', 'LanguageCode': 'uk', 'LanguageName': 'Ukrainian'},  # Ukraine
        57: {'CountryCode': 'PK', 'LanguageCode': 'ur', 'LanguageName': 'Urdu'},  # Pakistan
        58: {'CountryCode': 'VN', 'LanguageCode': 'vi', 'LanguageName': 'Vietnamese'},  # Vietnam
        59: {'CountryCode': 'WLS', 'LanguageCode': 'cy', 'LanguageName': 'Welsh'},  # Wales
        60: {'CountryCode': 'HU', 'LanguageCode': 'hu', 'LanguageName': 'Hungarian'},  # Hungary
        61: {'CountryCode': 'IN', 'LanguageCode': 'hi', 'LanguageName': 'Hindi'},  # India
        62: {'CountryCode': 'IN', 'LanguageCode': 'kn', 'LanguageName': 'Kannada'},  # India
        63: {'CountryCode': 'IN', 'LanguageCode': 'mr', 'LanguageName': 'Marathi'},  # India
    }
    try:
        exists = LanguageSupport.exists_table()
        if not exists:
            LanguageSupport.create_table()
            s3_logger.info(f"Table {LanguageSupport.table.name} created successfully.")
            print(f"Table {LanguageSupport.table.name} created successfully.")
            for id, lang in SUPPORTED_LANGUAGES.items():
                language_id = LanguageSupport.put_item(
                    LanguageID=str(id),
                    LanguageCode=lang["LanguageCode"],
                    LanguageName=lang["LanguageName"],
                    CountryCode=lang["CountryCode"],
                )
                s3_logger.info(f"Language {language_id} created successfully.")
                print(f"Language {language_id} created successfully.")
        else:
            s3_logger.info(f"Table {LanguageSupport.table.name} already exists.")
            print(f"Table {LanguageSupport.table.name} already exists.")
    except:
        raise

# Migrate Roles Table
def init_roles_table():
    try:
        exists = Role.exists_table()
        if not exists:
            Role.create_table()
            s3_logger.info(f"Table {Role.table.name} created successfully.")
            print(f"Table {Role.table.name} created successfully.")
        else:
            s3_logger.info(f"Table {Role.table.name} already exists.")
            print(f"Table {Role.table.name} already exists.")
    except:
        raise

# Migrate ResourceFolders Table
def init_resource_folders_table():
    try:
        exists = ResourceFolder.exists_table()
        if not exists:
            ResourceFolder.create_table()
            s3_logger.info(f"Table {ResourceFolder.table.name} created successfully.")
            print(f"Table {ResourceFolder.table.name} created successfully.")
        else:
            s3_logger.info(f"Table {ResourceFolder.table.name} already exists.")
            print(f"Table {ResourceFolder.table.name} already exists.")
    except:
        raise

# Migrate ResourceFiles Table
def init_resource_files_table():
    try:
        exists = ResourceFile.exists_table()
        if not exists:
            ResourceFile.create_table()
            s3_logger.info(f"Table {ResourceFile.table.name} created successfully.")
            print(f"Table {ResourceFile.table.name} created successfully.")
        else:
            s3_logger.info(f"Table {ResourceFile.table.name} already exists.")
            print(f"Table {ResourceFile.table.name} already exists.")
    except:
        raise

# Function to initialize all tables
def initialize_all_tables():

    init_functions = [
        # authentication app
        init_users_table,
        init_orgs_table,
        # init_user_permissions_table,
        # init_roles_table,
        
        # communication app
        init_channels_table,
        init_messages_table,
        init_language_support_table,
        init_feedbacks_table,

        # # knowledge base app
        init_knowledge_bases_table,
        init_knowledge_base_questions_table,
        

        # user manager app
        init_roles_table,
        init_teams_table,
        init_team_members_table,
        init_user_permissions_table,

        # file manager app
        init_resource_folders_table,
        init_resource_files_table,


        # init_billing_details_table,
        # init_channels_table,
        # init_messages_table,
        # init_file_uploads_table,
        # init_subscription_tiers_table,
        # init_license_keys_table,
        # init_support_agents_table,
        # init_support_queue_table,
        # init_process_table,
        # init_decision_trees_table,
        # init_extensions_table,
        # init_translation_cache_table,
        # init_faqs_table,
        # init_service_extensions_table,
        # init_audit_trail_for_files_table,
        # init_user_activity_log_table,
        # init_customer_support_log_table,
        # init_subscription_history_table,
        # init_third_party_integrations_table,
        # init_widgets_table,
        # init_user_saved_messages_table,
        # init_user_notification_settings_table,
        # init_api_audit_log_table,
        # init_scheduled_tasks_table,
        # init_webhooks_table,    
        # init_data_retention_policies_table,
        # init_email_templates_table,
        # init_invoicing_table,
        # init_payment_history_table,
        # init_payment_history,
        # init_feedback_and_ratings,
        # init_chat_bot_sessions,
        # init_machine_learning_models,
        # init_device_management,
        # init_geo_locations,
        # init_tags,
        # init_tag_associations,
        # init_error_logs,
        # init_team_members,
        # init_chat_bot_sessions,
        # init_machine_learning_models,
        # init_session_tokens,
        # init_search_history,
        # init_system_notifications,
        # init_sensitive_data_audit,
        # init_user_preferences,
        # init_analytics_dashboard,
        # init_report_generation,
        # init_short_links,
        # init_user_verification,
        # init_content_moderation,
        # init_campaigns,
        # init_coupons,
        # init_push_notifications,
        # init_event_logging,
        # init_temporary_files,
        # init_ab_testing,
        # init_failed_login_attempts,
        # init_rate_limiting,
        # init_data_exports,
        # init_newsletter_subscriptions,
        # init_pending_invitations,
        # init_social_interactions,
        # init_inventory_management,
        # init_order_history,
        # init_user_reviews,
        # init_data_archives,
        # init_customizations,
        # init_taxonomies,
        # init_bookmarks_favorites,
        # init_notifications,
        # init_security_policies,
        # init_user_journey_funnel,
        # init_compliance_records,
        # init_scheduled_reports,
        # init_affiliate_programs,
        # init_chat_messaging_archives,
        # init_learning_management,
        # init_course,
        # init_gamification,
        # init_course_content,
        # init_user_progress,
        # init_user_certificates,
        # init_forums,
        # init_forum_posts,
        # init_user_badges,
        # init_events,
        # init_user_events,
        # init_surveys,
        # init_survey_responses,
        # init_user_groups,
        # init_group_members,
        # init_user_notes,
        # init_discussions,
        # init_discussion_comments,
        # init_faq_categories,
        # init_faq_items,
        # init_user_bookmarks,
        # init_user_history,
        # init_resource_files,
        # init_user_feedback,
        # init_system_settings,
        # init_system_logs,
        # init_user_alerts,
        # init_file_permissions,
        # init_query_table,
        # init_document_table,
        # init_user_language_preferences,
        # init_guest_language_preferences,
    ]

    update_functions = [
        # update_folder_size,
        # update_file_size,
        # update_knowledge_base_with_setting
    ]
    
    for init_function in init_functions:
        try:
            init_function()
        except Exception as e:
            print(e)
            raise
    
    for update_function in update_functions:
        try:
            update_function()
        except Exception as e:
            print(e)
            raise

if __name__ == "__main__":
    initialize_all_tables()
