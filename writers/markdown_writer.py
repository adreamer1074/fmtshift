"""
Markdown ライター - 中間形式からMarkdownファイルを生成
"""
from pathlib import Path
from converters.base import Document, Sheet, Content, ContentType, Table


class MarkdownWriter:
    """中間形式からMarkdownファイルを生成"""
    
    def write(self, document: Document, file_path: Path):
        """
        Documentオブジェクトをmarkdownファイルに書き込み
        
        Args:
            document: 中間形式のドキュメント
            file_path: 出力先Markdownファイルのパス
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            # 複数シートの場合
            for sheet_idx, sheet in enumerate(document.sheets):
                # シート名を見出しとして追加（複数シートの場合）
                if len(document.sheets) > 1:
                    if sheet_idx > 0:
                        f.write('\n\n')
                    f.write(f'## {sheet.name}\n\n')
                
                # シートの内容を書き込み
                self._write_sheet_content(f, sheet)
    
    def _write_sheet_content(self, f, sheet: Sheet):
        """シートのコンテンツをMarkdownとして書き込み"""
        for content in sheet.contents:
            if content.type == ContentType.TITLE:
                f.write(f'# {content.value}\n\n')
            
            elif content.type == ContentType.TEXT:
                f.write(f'{content.value}\n\n')
            
            elif content.type == ContentType.LIST_ITEM:
                f.write(f'- {content.value}\n')
            
            elif content.type == ContentType.NUMBERED_LIST:
                f.write(f'1. {content.value}\n')
            
            elif content.type == ContentType.CODE_BLOCK:
                lang = content.metadata.get('language', '')
                f.write(f'```{lang}\n')
                f.write(content.value)
                f.write('\n```\n\n')
            
            elif content.type == ContentType.TABLE:
                table: Table = content.value
                self._write_table(f, table)
            
            elif content.type == ContentType.EMPTY:
                f.write('\n')
    
    def _write_table(self, f, table: Table):
        """テーブルをMarkdown形式で書き込み"""
        if not table.headers:
            return
        
        # ヘッダー行
        f.write('| ' + ' | '.join(table.headers) + ' |\n')
        
        # 区切り行
        f.write('| ' + ' | '.join(['---'] * len(table.headers)) + ' |\n')
        
        # データ行
        for row in table.rows:
            # 列数を揃える
            row_data = row + [''] * (len(table.headers) - len(row))
            f.write('| ' + ' | '.join(row_data[:len(table.headers)]) + ' |\n')
        
        f.write('\n')
