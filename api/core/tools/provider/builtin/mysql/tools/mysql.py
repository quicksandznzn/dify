import json
from datetime import datetime
from typing import Any, Union
from urllib.parse import quote

from sqlalchemy import create_engine, text

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool


class MySQLTool(BuiltinTool):
    @staticmethod
    def _convert_datetime(item):
        if isinstance(item, datetime):
            return item.isoformat()
        return item
    def _create_engine(self):
        password = quote('temp_admin@2018',safe='')
        url = f'mysql+pymysql://temp_admin:{password}@10.6.1.15:3306/ai_car_video'
        engine = create_engine(url)
        return engine
    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]
                ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
            invoke tools
        """
        sql = tool_parameters.get('sql', '')
        if not sql:
            return self.create_text_message('Invalid parameter sql')
        result_list = []
        with self._create_engine().connect() as connection:

            rows = connection.execute(text('select * from new_media_leads_info'))
            columns = rows.keys()
            data = [dict(zip(columns, [self._convert_datetime(item) for item in row])) for row in rows]

            markdown = '| ' + ' | '.join(columns) + ' |\n'
            markdown += '| ' + ' | '.join(['---'] * len(columns)) + ' |\n'
            for row in data:
                markdown += '| ' + ' | '.join(str(row[column]) for column in columns) + ' |\n'

            return self.create_text_message(markdown + "\n\n" + json.dumps(data, ensure_ascii=False))
