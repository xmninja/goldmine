"""Welcome and goodbye messages."""
import discord
import util.commands as commands
from util.const import bool_true
from .cog import Cog

welcome = '''Welcome {0.mention} to **{1.name}**. Have a good time here! :wink:
Learn more about me with `{2}help`.'''
goodbye = '''**{0}** has just left this server. Bye!
**{1.name}** just lost a {2}. We'll miss you!'''
class Welcome(Cog):
    """Welcomes and goodbyes. 🤗"""
    def __init__(self, bot):
        super().__init__(bot)
        self.logger = self.logger.getChild('welcome')

    async def on_member_join(self, member: discord.Member):
        """On_member_join event for newly joined members."""
        if self.bot.selfbot: return
        target = member.server
        bc = self.store.get_prop(member, 'broadcast_join')
        cmdfix = self.store.get_prop(member, 'command_prefix')
        if str(bc).lower() in bool_true:
            try:
                await self.bot.send_message(target, welcome.format(member, target, cmdfix))
            except discord.Forbidden:
                self.logger.warning(f'Couldn\'t announce join of {member} to {member.server}')

    async def on_member_remove(self, member: discord.Member):
        """On_member_remove event for members leaving."""
        if self.bot.selfbot: return
        target = member.server
        bc = self.store.get_prop(member, 'broadcast_leave')
        if str(bc).lower() in bool_true:
            utype = ('bot' if member.bot else 'member')
            try:
                await self.bot.send_message(target, goodbye.format(str(member), target, utype))
            except discord.Forbidden:
                self.logger.warning(f'Couldn\'t announce leave of {member} from {member.server}')

def setup(bot):
    bot.add_cog(Welcome(bot))
