from typing import Any, Union

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.tool.builtin_tool import BuiltinTool
from libs.smtp import SMTPClient


class EmailTool(BuiltinTool):
    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]
                ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
            invoke tools
        """
        self.validate_credentials(self.runtime.credentials, tool_parameters)

        cc = tool_parameters.get('cc', '')

        content = tool_parameters.get('content', '')
        if not content:
            return self.create_text_message('Invalid parameter content')

        subject = tool_parameters.get('subject', '')
        if not subject:
            return self.create_text_message('Invalid parameter subject')

        to = tool_parameters.get('to', '')
        if not to:
            return self.create_text_message('Invalid parameter to')

        smtp_client = SMTPClient(
            server=self.runtime.credentials['smtp_server'],
            port=self.runtime.credentials['smtp_port'],
            username=self.runtime.credentials['smtp_username'],
            password=self.runtime.credentials['smtp_password'],
            _from=self.runtime.credentials['smtp_from'],
            use_tls=self.runtime.credentials['smtp_use_tls']
        )

        try:
            smtp_client.send({
                "to": to,
                "cc": cc,
                "subject": subject,
                "html": content
            })
            return self.create_text_message("Text email sent successfully")
        except Exception as e:
            return self.create_text_message("Failed to send email. {}".format(e))

    def validate_credentials(self, credentials: dict[str, Any], parameters: dict[str, Any]) -> None:
        """
            validate the credentials

            :param credentials: the credentials
            :param parameters: the parameters
        """
        if 'smtp_server' not in self.runtime.credentials or not self.runtime.credentials.get('smtp_server'):
            raise ToolProviderCredentialValidationError("STMP server is required.")

        if 'smtp_port' not in self.runtime.credentials or not self.runtime.credentials.get('smtp_port'):
            raise ToolProviderCredentialValidationError("STMP port is required.")

        if 'smtp_username' not in self.runtime.credentials or not self.runtime.credentials.get('smtp_username'):
            raise ToolProviderCredentialValidationError("STMP username  is required.")

        if 'smtp_password' not in self.runtime.credentials or not self.runtime.credentials.get('smtp_password'):
            raise ToolProviderCredentialValidationError("STMP password key is required.")

        if 'smtp_from' not in self.runtime.credentials or not self.runtime.credentials.get('smtp_from'):
            raise ToolProviderCredentialValidationError("STMP from  is required.")

        if 'smtp_use_tls' not in self.runtime.credentials or not self.runtime.credentials.get('smtp_use_tls'):
            raise ToolProviderCredentialValidationError("STMP use tls is required.")
