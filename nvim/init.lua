vim.g.mapleader = " "
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.expandtab = true
vim.opt.softtabstop = 2
vim.opt.number = true
vim.opt.relativenumber = false

vim.pack.add({
  { src = 'https://github.com/lewis6991/gitsigns.nvim' },
  { src = 'https://github.com/nvim-mini/mini.pick' },
  { src = 'https://github.com/navarasu/onedark.nvim' },
  { src = "https://github.com/nvim-treesitter/nvim-treesitter", version = "master" },
});

require('gitsigns').setup()
require('mini.pick').setup()
require('onedark').setup({
  transparent = true,
  style = 'darker',
})
require('nvim-treesitter').setup({
  ensure_installed = {
    "lua",
    "go",
    "vim",
    "vimdoc",
    "query",
    "java",
    "html",
    "scss",
    "css",
    "typescript",
    "javascript",
    "bash",
    "json",
    "yaml",
    "markdown",
    "markdown_inline",
  },
  auto_install = true,
  highlight = { enable = true, additional_vim_regex_highlighting = false },
  indent = { enable = true },
})

vim.keymap.set('n', '<leader>f', ':Pick files<CR>');
vim.keymap.set('n', '<leader>s', ':Pick grep<CR>');
vim.keymap.set('n', '<leader>b', ':Pick buffers<CR>');

vim.cmd('colorscheme onedark')
