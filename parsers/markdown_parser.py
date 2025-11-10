"""
Markdown パーサー - Markdownファイルを中間形式に変換
"""
from pathlib import Path
from converters.base import Document, Sheet, Content, ContentType, Table


class MarkdownParser:
    """Markdownファイルを読み込んで中間形式に変換"""
    
    def parse(self, file_path: Path) -> Document:
        """
        Markdownファイルを解析してDocumentオブジェクトに変換
        
        Args:
            file_path: Markdownファイルのパス
            
        Returns:
            Document: 中間形式のドキュメント
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        doc = Document(title=file_path.stem)
        lines = content.split('\n')
        
        current_sheet = Sheet(name='Sheet1')
        in_code_block = False
        code_lines = []
        code_lang = ''
        
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # コードブロックの開始/終了
            if stripped.startswith('```'):
                if not in_code_block:
                    # 開始
                    in_code_block = True
                    code_lang = stripped[3:].strip()
                    code_lines = []
                else:
                    # 終了
                    in_code_block = False
                    code_content = '\n'.join(code_lines)
                    content = Content(
                        type=ContentType.CODE_BLOCK,
                        value=code_content,
                        metadata={'language': code_lang}
                    )
                    current_sheet.add_content(content)
                    code_lines = []
                    code_lang = ''
                i += 1
                continue
            
            # コードブロック内
            if in_code_block:
                code_lines.append(line)
                i += 1
                continue
            
            # シート名（##見出し）
            if stripped.startswith('##') and not stripped.startswith('###'):
                # 前のシートを保存
                if current_sheet.contents:
                    doc.add_sheet(current_sheet)
                
                sheet_name = stripped.lstrip('#').strip()
                current_sheet = Sheet(name=sheet_name)
                i += 1
                continue
            
            # テーブル行
            if stripped.startswith('|'):
                # 区切り行の場合
                if '---' in stripped:
                    i += 1
                    continue
                
                # テーブルヘッダーまたはデータ行
                cells = [cell.strip() for cell in stripped.split('|')[1:-1]]
                
                # 次の行がテーブルかチェック
                table_rows = [cells]
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    if next_line.startswith('|') and '---' not in next_line:
                        next_cells = [cell.strip() for cell in next_line.split('|')[1:-1]]
                        table_rows.append(next_cells)
                        j += 1
                    elif '---' in next_line:
                        j += 1
                    else:
                        break
                
                # テーブルを作成
                if len(table_rows) > 1:
                    table = Table(headers=table_rows[0], rows=table_rows[1:])
                else:
                    table = Table(headers=table_rows[0], rows=[])
                
                content = Content(
                    type=ContentType.TABLE,
                    value=table,
                    metadata={'source': 'markdown'}
                )
                current_sheet.add_content(content)
                
                i = j
                continue
            
            # リスト
            if stripped.startswith('- ') or stripped.startswith('* '):
                list_text = stripped[2:]
                content = Content(
                    type=ContentType.LIST_ITEM,
                    value=list_text
                )
                current_sheet.add_content(content)
                i += 1
                continue
            
            # 番号付きリスト
            if stripped and stripped[0].isdigit() and '. ' in stripped[:4]:
                list_text = stripped.split('. ', 1)[1] if '. ' in stripped else stripped
                content = Content(
                    type=ContentType.NUMBERED_LIST,
                    value=list_text
                )
                current_sheet.add_content(content)
                i += 1
                continue
            
            # 見出し（#）- ドキュメントタイトル
            if stripped.startswith('#') and not stripped.startswith('##'):
                title_text = stripped.lstrip('#').strip()
                if not doc.title or doc.title == file_path.stem:
                    doc.title = title_text
                content = Content(
                    type=ContentType.TITLE,
                    value=title_text
                )
                current_sheet.add_content(content)
                i += 1
                continue
            
            # 通常のテキスト
            if stripped:
                content = Content(
                    type=ContentType.TEXT,
                    value=stripped
                )
                current_sheet.add_content(content)
            elif current_sheet.contents:
                # 空行（内容がある場合のみ）
                content = Content(
                    type=ContentType.EMPTY,
                    value=''
                )
                current_sheet.add_content(content)
            
            i += 1
        
        # 最後のシートを保存
        if current_sheet.contents:
            doc.add_sheet(current_sheet)
        
        return doc
