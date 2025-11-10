"""
Converter - 形式間の変換を調整
"""
from pathlib import Path
from parsers.excel_parser import ExcelParser
from parsers.markdown_parser import MarkdownParser
from writers.excel_writer import ExcelWriter
from writers.markdown_writer import MarkdownWriter


class FormatConverter:
    """形式変換のコーディネーター"""
    
    def __init__(self):
        self.parsers = {
            '.xlsx': ExcelParser(),
            '.xls': ExcelParser(),
            '.md': MarkdownParser(),
        }
        
        self.writers = {
            '.xlsx': ExcelWriter(),
            '.xls': ExcelWriter(),
            '.md': MarkdownWriter(),
        }
    
    def convert(self, from_file: Path, to_file: Path):
        """
        ファイル形式を変換
        
        Args:
            from_file: 変換元ファイル
            to_file: 変換先ファイル
            
        Raises:
            ValueError: サポートされていない形式の場合
        """
        from_ext = from_file.suffix.lower()
        to_ext = to_file.suffix.lower()
        
        # パーサーとライターを取得
        parser = self.parsers.get(from_ext)
        writer = self.writers.get(to_ext)
        
        if parser is None:
            raise ValueError(f'サポートされていない入力形式: {from_ext}')
        
        if writer is None:
            raise ValueError(f'サポートされていない出力形式: {to_ext}')
        
        # 変換実行
        # 1. 読み込み（パース）
        document = parser.parse(from_file)
        
        # 2. 書き込み
        writer.write(document, to_file)
    
    def get_supported_formats(self):
        """サポートされている形式のリストを返す"""
        return {
            'input': list(self.parsers.keys()),
            'output': list(self.writers.keys())
        }
    
    def add_parser(self, extension: str, parser):
        """新しいパーサーを追加（拡張用）"""
        self.parsers[extension] = parser
    
    def add_writer(self, extension: str, writer):
        """新しいライターを追加（拡張用）"""
        self.writers[extension] = writer
