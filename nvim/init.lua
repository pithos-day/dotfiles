vim.g.mapleader = " "
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.expandtab = true
vim.opt.softtabstop = 2

vim.pack.add({
  { src = 'https://github.com/navarasu/onedark.nvim' },
});

require('onedark').setup({
  transparent = true,
  style = 'darker',
})

vim.cmd('colorscheme onedark')
