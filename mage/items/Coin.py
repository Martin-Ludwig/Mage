from mongoengine import IntField, ReferenceField
import discord

from mage.models.Item import Item
from mage.models.User import User
from random import randint
import utils.data_access as data


class Coin(Item):
    # overriden attributes
    name = "Coin"
    brief = 'flips a coin'
    description = 'flips a coin to gain or lose points'
    price = 500
    use_cost = 60
    level_restriction = 0

    categories = ["Gamble"]
    is_consumable = False
    is_enabled = True
    is_event_item = False
    is_shop_item = True

    Item.append_categories(categories, is_consumable, is_event_item, level_restriction)

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)

    @staticmethod
    def on_buy(context):
        pass

    @classmethod
    async def on_use(cls, context):
        user = data.find_one(User, discord_user_id=context.author.id, discord_guild_id=context.guild.id)
        user.name = context.author.display_name
        guild = context.guild

        if Coin.pre_use(user):
            await Coin.action_is_ok(user, context)
        else:
            await context.send(Coin.action_is_not_ok(guild))


    @staticmethod
    async def action_is_ok(user, context):
        role_result = randint(1, 2)
        if role_result == 1:
            amount = 100
        else:
            amount = 0

        user.points = user.points + amount - Coin.use_cost
        user.save()
        msg = Coin.action_success(context, user, role_result)
        await context.send(msg)

    @staticmethod
    def action_success(context, user, role_result):
        if role_result == 1:
            return f"{context.author.display_name} flipped head. That's a win." \
               f" Your points now: {user.points}"
        else:
            return f"{context.author.display_name} flipped tail. That's a lose." \
               f" Your points now: {user.points}"





    @staticmethod
    def action_is_not_ok(guild):
        return "You dont meet the Requirements or you have used invalid arguments"
