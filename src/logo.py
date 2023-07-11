BOT_TITLE = r"""
                  
  ____        _   
 |  _ \      | |  
 | |_) | ___ | |_ 
 |  _ < / _ \| __|
 | |_) | (_) | |_ 
 |____/ \___/ \__|
"""

TEAM_TITLE = r"""
⠀⠀⠀                            
 _____ _ _   _   _ _           
| ___ (_) | | | | (_)          
| |_/ /_| |_| |_| | |_   _____ 
| ___ \ | __|  _  | \ \ / / _ \
| |_/ / | |_| | | | |\ V /  __/
\____/|_|\__\_| |_/_| \_/ \___|
"""

HONEYCOMB = r"""
    __    
 __/  \__ 
/  \__/  \
\__/  \__/
/  \__/  \
\__/  \__/
   \__/   
   """
team_split = TEAM_TITLE.split('\n')
honeycomb_split = HONEYCOMB.split('\n')
bot_split = BOT_TITLE.split('\n')
result = ''
for team_line, honeycomb_line, bot_line in zip(team_split, honeycomb_split, bot_split):
    result += f"{team_line}{' '*4}{honeycomb_line}{' '*4}{bot_line}\n"

LOGO = result
