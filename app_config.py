import os

#CLIENT_ID = "1bfce52d-0ed8-44c9-86e4-32bbbad9b33a" # Application (client) ID of app registration
#CLIENT_SECRET = "Qsm~_RXZ1lZ6~oPiy3Z-J2L.9m-h0QYkdU" # Placeholder - for use ONLY during testing.

CLIENT_ID = "d3e03654-6e7b-4ff2-a9b8-7c778112baf2"
CLIENT_SECRET = "OnO1En.aqH20uq_-1S8RdX2c_HbE5IRX_9"
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
SCOPE = ["OnlineMeetings.ReadWrite", "User.ReadBasic.All"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session


username = 'kelvin@synnexmetrodataindonesia.onmicrosoft.com'
pw = 'Testingapi44'

#agent_email = "gume-br1lmyldfzyvrw2j_admin@qismo.com"
#app_code = 'gume-br1lmyldfzyvrw2j'
agent_email = "tyes-razurkhhoyewouxd_admin@qismo.com"
app_code = "tyes-razurkhhoyewouxd"