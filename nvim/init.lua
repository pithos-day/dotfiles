vim.g.mapleader = " "
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.expandtab = true
vim.opt.softtabstop = 2
vim.opt.number = true
vim.opt.relativenumber = false

vim.opt.complete = "o"
vim.opt.pumheight = 10
vim.opt.completeopt = { "menuone", "noinsert" }
vim.api.nvim_create_autocmd("LspAttach", {
  callback = function(args)
    local client = assert(vim.lsp.get_client_by_id(args.data.client_id))
    if client:supports_method("textDocument/completion") then
      client.server_capabilities.completionProvider.triggerCharacters = nil
      vim.lsp.completion.enable(true, client.id, args.buf, {
        autotrigger = true,
        convert = function(item)
          return {
            abbr = item.label:gsub("%b()", ""),
          }
        end,
      })
    end
  end,
})

vim.pack.add({
  { src = "https://github.com/neovim/nvim-lspconfig" },
  { src = "https://github.com/lewis6991/gitsigns.nvim" },
  { src = "https://github.com/nvim-mini/mini.pick" },
  { src = "https://github.com/navarasu/onedark.nvim" },
  { src = "https://github.com/nvim-treesitter/nvim-treesitter", version = "master" },
});

require("gitsigns").setup()
require("mini.pick").setup()
require("onedark").setup({
  transparent = true,
  style = "darker",
})
require("nvim-treesitter").setup({
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

vim.keymap.set("n", "grd", vim.lsp.buf.definition);
vim.keymap.set("n", "gre", vim.diagnostic.open_float);
vim.keymap.set("n", "<leader>lf", vim.lsp.buf.format);
vim.keymap.set({ "n", "v", "x" }, "<leader>y", [["+y<CR>]])

vim.keymap.set("n", "<leader>f", [[:Pick files<CR>]]);
vim.keymap.set("n", "<leader>s", [[:Pick grep<CR>"]]);
vim.keymap.set("n", "<leader>b", [[:Pick buffers<CR>]]);

vim.lsp.enable("gopls")
vim.lsp.enable("ts_ls")
vim.lsp.enable("lua_ls")
vim.lsp.enable("bashls")

vim.cmd("colorscheme onedark")
