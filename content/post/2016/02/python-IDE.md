---
date: "2016-02-22T15:48:44+08:00"
title: "python IDE"
categories:
    - python
    - IDE

---
## VIM
#### 1. 参考链接：
https://github.com/yangyangwithgnu/use_vim_as_ide
https://github.com/spf13/spf13-vim

#### 2. install
sudo pip install pyflakes

sudo pip install pylint

sudo pip install pep8  

或者使用这个vim插件

https://github.com/scrooloose/syntastic

#### 3. 我的vimrc
```
call pathogen#infect()

syntax enable
syntax on
set background=dark
set number
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set laststatus=2
set ruler
" set cursorcolumn " 突出显示当前列
set cursorline " 突出显示当前行
set hlsearch
set incsearch
set ignorecase
set autoindent
set nowrap
set showcmd       " 显示输入命令
let g:solarized_termcolors=16
colorscheme solarized
set textwidth=79
autocmd FileType text setlocal textwidth=78
" 一旦一行的字符超出79个的话就把那些字符的背景设为红色
highlight OverLength ctermbg=red ctermfg=white guibg=#592929
match OverLength /\%80v.\+/

filetype on " 检测文件类型
filetype indent on " 针对不同的文件类型采用不同的缩进格式
filetype plugin on " 允许插件
filetype plugin indent on " 启动自动补全

set autoread " 文件修改之后自动载入
set shortmess=atI " 启动的时候不显示那个援助索马里儿童的提示
set scrolloff=7 " 在上下移动光标时，光标的上方或下方至少会保留显示的行数
set ffs=unix,dos,mac " Use Unix as the standard file type

set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open=1
let g:syntastic_check_on_wq=0
let g:syntastic_enable_highlighting=1
let g:syntastic_python_checkers=['pep8'] " pyflakes, pylint, pep8
let g:syntastic_python_pylint_args='--disable=C0111'
```

## PyCharm

#### 参考链接
http://blog.csdn.net/u013088062/article/details/50100121

#### 操作步骤
1. 在Settings/Preferences对话框中的Inspections页面，键入PEP8来找到所有相关选项，在对应的下拉菜单中选中warning选项；在Ignore erros中添加可忽略警告，C0111

2. 在Settings/Preferences对话框中的Auto Import中选择Python下的Show import popup

3. 在Settings/Preferences对话框中的 File Encoding中IDE Encoding和Project Encoding都使用UTF-8

#### 我的Settings文件
[settings.jar](https://github.com/guozhaoxia007/guozhaoxia-hugo-blog/tree/master/content/post/2016/02)

## Sublime Text 2

#### 参考链接

#### 操作步骤

1. Ctrl+Shift+p打开命令面板输入install，就可以看到安装列表

2. 安装以下插件：sublime linter, pylinter 或 python flake8 lint

#### 我的Settings文件
```
{
    "auto_indent": true,
    "color_scheme": "Packages/Color Scheme - Default/Twilight.tmTheme",
    "default_line_ending": "unix",
    "detect_indentation": true,
    "font_size": 15.0,
    "ignored_packages":
    [
        "Vintage"
    ],
    "indent_to_bracket": false,
    "smart_indent": true,
    "tab_size": 4,
    "translate_tabs_to_spaces": true,
    "trim_automatic_white_space": true,
    "use_tab_stops": true
}
```

