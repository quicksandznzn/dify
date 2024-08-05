from core.tools.provider.builtin.mysql.tools.mysql import MySQLTool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController


class MySQLProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict) -> None:
        MySQLTool()
