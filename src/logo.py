bot = r"""
                  
  ____        _   
 |  _ \      | |  
 | |_) | ___ | |_ 
 |  _ < / _ \| __|
 | |_) | (_) | |_ 
 |____/ \___/ \__|
"""

LOGO = r"""
⠀⠀⠀                            
 _____ _ _   _   _ _           
| ___ (_) | | | | (_)          
| |_/ /_| |_| |_| |___   _____ 
| ___ \ | __|  _  | \ \ / / _ \
| |_/ / | |_| | | | |\ V /  __/
\____/|_|\__\_| |_/_| \_/ \___|
"""

hexag = r"""
    __    
 __/  \__ 
/  \__/  \
\__/  \__/
/  \__/  \
\__/  \__/
   \__/   
   """
logo_split = LOGO.split('\n')
hexag_split = hexag.split('\n')
bot_split = bot.split('\n')
result = ''
for logo_line, hex_line, bot_line in zip(logo_split, hexag_split, bot_split):
    result += f"{logo_line}{' '*4}{hex_line}{' '*4}{bot_line}\n"

NEW_LOGO = result
