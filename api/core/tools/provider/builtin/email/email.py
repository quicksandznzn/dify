from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin.email.tools.email import EmailTool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController


class EmailProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict) -> None:
        try:
            EmailTool().fork_tool_runtime(
                runtime={
                    "credentials": credentials,
                }
            ).invoke(
                user_id='',
                tool_parameters={
                    "subject":"Email Tool",
                    "content": "Email Tool",
                    "to": "noone",
                },
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
