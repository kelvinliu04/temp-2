import os

CLIENT_ID = "1bfce52d-0ed8-44c9-86e4-32bbbad9b33a" # Application (client) ID of app registration

CLIENT_SECRET = "Qsm~_RXZ1lZ6~oPiy3Z-J2L.9m-h0QYkdU" # Placeholder - for use ONLY during testing.
# In a production app, we recommend you use a more secure method of storing your secret,
# like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")

AUTHORITY = "https://login.microsoftonline.com/common"  # For multi-tenant app
AUTHORITYORG = "https://login.microsoftonline.com/organizations"
#AUTHORITY = "https://login.microsoftonline.com/d26bf608-8326-4a29-88fc-36e8f30b976d"

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
                              # The absolute URL must match the redirect URI you set
                              # in the app's registration in the Azure portal.

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["User.ReadBasic.All", "OnlineMeetings.ReadWrite", "Calendars.ReadWrite"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session


username = 'kelvin@synnexmetrodataindonesia.onmicrosoft.com'
pw = 'Testingapi44'