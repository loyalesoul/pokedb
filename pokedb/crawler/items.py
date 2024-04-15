# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class PokemonItem(Item):
    name = Field()
    national_no = Field()
    attributes = Field()
    training = Field()
    breeding = Field()
    stats = Field()
    evolution_chain = Field()
    pokedex_entries = Field()
    moves_levelup = Field()
    moves_tm = Field()
    moves_egg = Field()
    location = Field()
    other_languages = Field()
    artwork_urls = Field()
    _validation = Field()


class PokemonList(Item):
    urls = Field()
