"" From http://mislav.uniqpath.com/2011/12/vim-revisited/
"" Note the "ln -s <this-file> ~/.vimrc" :-)
set nocompatible
syntax on
set encoding=utf-8
set showcmd                     " display incomplete commands

"" Whitespace
set wrap
set textwidth=80
"set nowrap                      " don't wrap lines
set tabstop=2 shiftwidth=2 softtabstop=2     " a tab is two spaces
set expandtab                   " use spaces, not tabs
set backspace=indent,eol,start  " backspace through everything in insert mode

"" Searching
set hlsearch                    " highlight matches
set incsearch                   " incremental searching
set ignorecase                  " searches are case insensitive...
set smartcase                   " ... unless they contain at least one capital letter

"" Enda's color
color elflord
color macvim                    " Setting the color to macvim is what I want to do, but
                                " for an unknown reason, it isn't picked up on
                                " its own, so I need to set and then reset it
                                " here.
" Show me a ruler
set ruler

" Set up puppet manifest and spec options
au BufRead,BufNewFile *.pp
  \ set filetype=puppet
au BufRead,BufNewFile *_spec.rb
  \ nmap <F8> :!rspec --color %<CR>

filetype plugin indent on       " load file type plugins + indentation

"" http://blog.dispatched.ch/2009/05/24/vim-as-python-ide/
"" http://www.vim.org/scripts/script.php?script_id=159
let g:miniBufExplMapWindowNavVim = 1
let g:miniBufExplMapWindowNavArrows = 1
let g:miniBufExplMapCTabSwitchBufs = 1
let g:miniBufExplModSelTarget = 1
map T :TaskList<CR>
map P :TlistToggle<CR>
