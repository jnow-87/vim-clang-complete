import re
import vim

def snippetsInit():
  if int(vim.eval("g:clang_conceal_snippets")) == 1:
    vim.command("syntax region clang_arg matchgroup=None start='`<' end='>`' concealends")
    vim.command("highlight default clang_arg ctermbg=39")

# The two following function are performance sensitive, do _nothing_
# more that the strict necessary.

def snippetsFormatPlaceHolder(word):
  return "`<%s>`" % word

def snippetsAddSnippet(fullname, word, abbr):
  # do not include closing bracket
  if word[-1] == ")":
    return word[0:-1]
  else:
    return word

r = re.compile('`<[^>]*>`')
rv = re.compile('`>[^<]*<`')

def snippetsTrigger():
  if r.search(vim.current.line) is None:
    return
  vim.command('call feedkeys("\<esc>^\<c-n>")')

def snippetsReset():
  pass

def updateSnips(reverse):
  line = vim.current.line
  row, col = vim.current.window.cursor

  # check if to search backwards
  if reverse:
    # invert line and use inversely defined regex
    # also ajdust column
    reg = rv
    line = line[::-1]
    col = len(line) - col - 1
  else:
    reg = r

  # perform search
  result = reg.search(line, col)

  if result is None:
    result = reg.search(line)
    if result is None:
      if reverse:
        vim.command('call feedkeys("i\<c-p>", "n")')
      else:
        vim.command('call feedkeys("i\<c-n>", "n")')
      return

  # get start and end position of match
  start, end = result.span()

  if reverse:
    # convert result for original string (not inverted)
    start = len(line) - result.span()[1]
    end = len(line) - result.span()[0]

  # select match in vim
  vim.current.window.cursor = row, start
  isInclusive = vim.eval("&selection") == "inclusive"
  vim.command('call feedkeys("\<ESC>v%dl\<C-G>", "n")' % (end - start - isInclusive))

# vim: set ts=2 sts=2 sw=2 expandtab :
