
src = """
sed -ie 's/^\\(.*\\)/#\\1/' /etc/ld.so.preload
cat >/etc/udev/rules.d/90-qemu.rules <<EOL
KERNEL=="sda", SYMLINK+="mmcblk0"
KERNEL=="sda?", SYMLINK+="mmcblk0p%n"
KERNEL=="sda2", SYMLINK+="root"
EOL
exit

"""

specials = 
  ' ': 'spc'

  '[': 'bracket_left'
  '{': 'shift-bracket_left'

  ']': 'bracket_right'
  '}': 'shift-bracket_right'
  
  '\\': 'backslash'
  '|': 'shift-backslash'

  ';': 'semicolon'
  ':': 'shift-semicolon'

  '\'': 'apostrophe'
  '"': 'shift-apostrophe'

  '\n': 'ret'

  ',': 'comma'
  '<': 'shift-comma'

  '.': 'dot'
  '>': 'shift-dot'

  '/': 'slash'
  '?': 'shift-slash'

  '-': 'minus'
  '_': 'shift-minus'

  '=': 'equal'
  '+': 'shift-equal'

  '!': 'shift-1'
  '@': 'shift-2'
  '#': 'shift-3'
  '$': 'shift-4'
  '%': 'shift-5'
  '^': 'shift-6'
  '&': 'shift-7'
  '*': 'shift-8'
  '(': 'shift-9'
  ')': 'shift-0'

sendkey = (k) ->
  k = specials[k] if k of specials
  k = "shift-#{k.toLowerCase()}" if k.toLowerCase() isnt k
  "sendkey #{k}"

console.log (sendkey k for k in src).join '\n'