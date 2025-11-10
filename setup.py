from setuptools import setup, find_packages
import os

# __init__.pyからバージョンを読み込む
here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, '__init__.py'), 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line, about)
            break

setup(
    name='fmtshift',
    version=about['__version__'],
    description='フォーマット変換ツール',
    author='',
    author_email='',
    url='https://github.com/adreamer1074/fmtshift.git',
    
    # パッケージ構成
    packages=find_packages(),  # converters, parsers, writers を自動検出
    py_modules=['fmtshift'],   # fmtshift.py
    
    # 依存パッケージ
    install_requires=[
        'openpyxl>=3.1.2',
        'pandas>=2.0.0',
    ],
    
    # コンソールスクリプト
    entry_points={
        'console_scripts': [
            'fmtshift=fmtshift:main',
        ],
    },
    
    # Python バージョン
    python_requires='>=3.7',
    
    # 分類情報
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    
    # キーワード
    keywords='excel markdown converter pdf csv format-converter',
)
