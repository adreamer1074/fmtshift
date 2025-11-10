#!/usr/bin/env python3
"""
fmtshift - Format Shift Tool
Excel ↔ Markdown 双方向変換ツール

Version 2.0 - リファクタリング版
"""
import argparse
import sys
from pathlib import Path

# スクリプトのディレクトリをパスに追加
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from converters.converter import FormatConverter

# バージョン情報 (ルートの__init__.pyと同期)
__version__ = '0.2'


def main():
    """CLIエントリーポイント"""
    parser = argparse.ArgumentParser(
        description=f'fmtshift - 複数フォーマット変換ツール (v{__version__})',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用例:
  fmtshift -f test.xlsx -t test.md      # Excel → Markdown
  fmtshift -f test.md -t test.xlsx      # Markdown → Excel
  fmtshift -f input.xlsx -t output.md   # ファイル名を指定
  
サポート形式:
  入力: .xlsx, .xls, .md
  出力: .xlsx, .xls, .md
  
今後追加予定:
  - PDF (.pdf)
  - CSV (.csv)
        '''
    )
    
    parser.add_argument('-f', '--from', dest='from_file', required=True,
                        help='変換元ファイル')
    parser.add_argument('-t', '--to', dest='to_file', required=True,
                        help='変換先ファイル')
    parser.add_argument('-v', '--version', action='version', 
                        version=f'fmtshift {__version__}')
    
    args = parser.parse_args()
    
    # ファイルパスを取得
    from_path = Path(args.from_file)
    to_path = Path(args.to_file)
    
    # 変換元ファイルの存在確認
    if not from_path.exists():
        print(f'✗ エラー: ファイルが見つかりません: {from_path}', file=sys.stderr)
        sys.exit(1)
    
    # 変換実行
    try:
        converter = FormatConverter()
        converter.convert(from_path, to_path)
        print(f'✓ 変換完了: {from_path.name} → {to_path.name}')
    
    except ValueError as e:
        print(f'✗ エラー: {e}', file=sys.stderr)
        print(f'\nサポートされている形式:', file=sys.stderr)
        supported = converter.get_supported_formats()
        print(f'  入力: {", ".join(supported["input"])}', file=sys.stderr)
        print(f'  出力: {", ".join(supported["output"])}', file=sys.stderr)
        sys.exit(1)
    
    except Exception as e:
        print(f'✗ 予期しないエラー: {e}', file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
