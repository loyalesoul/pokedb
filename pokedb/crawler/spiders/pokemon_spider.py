import scrapy
import logging
from crawler.items import PokemonItem

logger = logging.getLogger(__name__)


class PokemonListSpider(scrapy.Spider):
    name = "pokemon_list"
    allowed_domains = ["pokemondb.net"]
    start_urls = ["https://pokemondb.net/pokedex/all"]

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set(
            "ITEM_PIPELINES",
            {
                "crawler.pipelines.PokemonURLsPipeline": 1,
            },
            priority="spider",
        )

    def __init__(self, *args, **kwargs):
        super(PokemonListSpider, self).__init__(*args, **kwargs)
        self.pokemon_urls = []

    def parse(self, response):
        # Using XPath to extract the URLs
        pokemon_urls = response.xpath('//td[@class="cell-name"]/a/@href').getall()
        pokemon_urls = [response.urljoin(url) for url in pokemon_urls]

        # Remove duplicates
        seen = set()
        unique_urls = []
        for pokemon_url in pokemon_urls:
            if pokemon_url not in seen:
                unique_urls.append(pokemon_url)
                seen.add(pokemon_url)

        for pokemon_url in unique_urls:
            yield {
                "pokemon_url": pokemon_url,
            }


class PokemonSpider(scrapy.Spider):
    name = "pokemon"
    allowed_domains = ["pokemondb.net"]

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set(
            "ITEM_PIPELINES",
            {
                "crawler.pipelines.PokemonFilesPipeline": 2,
                "crawler.pipelines.MongoPipeline": 3,
            },
            priority="spider",
        )
        settings.set("FILES_URLS_FIELD", "artwork_urls", priority="spider")

    def start_requests(self):
        files_store = self.settings.get("FILES_STORE")
        with open(f"{files_store}/pokemon_urls.txt", "r") as f:
            urls = [url.strip() for url in f.readlines()]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_pokedex_entries(self, response):
        entries = {}

        rows = response.css(
            'h2:contains("Pokédex entries") + div.resp-scroll table.vitals-table tbody tr'
        )

        # Iterate over each row to extract the game name and Pokédex entry
        for row in rows:
            game_names = row.css("th span::text").getall()
            game_names = " / ".join(game_names)

            pokedex_entry = row.css("td.cell-med-text::text").get().strip()

            entries[game_names] = pokedex_entry

        return entries

    def parse_moves_levelup(self, response):
        moves = []

        selector_moves = response.css(
            'h3:contains("Moves learnt by level up") + p + div.resp-scroll table.data-table tbody tr'
        )

        for s in selector_moves:
            move = {}
            move["level"] = s.css("td:nth-of-type(1)::text").get()
            move["move"] = s.css("td.cell-name a.ent-name::text").get()
            move["type"] = s.css("td.cell-icon a.type-icon::text").get()
            move["category"] = s.css("td.cell-icon img::attr(alt)").get()
            move["power"] = s.css("td:nth-of-type(5)::text").get()
            move["accuracy"] = s.css("td:nth-of-type(6)::text").get()

            moves.append(move)

        return moves

    def parse_moves_tm(self, response):
        moves = []

        selector_moves = response.css(
            'h3:contains("Moves learnt by TM") + p + div.resp-scroll table.data-table tbody tr'
        )

        for s in selector_moves:
            move = {}
            move["tm"] = s.css("td:nth-of-type(1) a::attr(title)").get()
            move["move"] = s.css("td.cell-name a.ent-name::text").get()
            move["type"] = s.css("td.cell-icon a.type-icon::text").get()
            move["category"] = s.css("td.cell-icon img::attr(alt)").get()
            move["power"] = s.css("td:nth-of-type(5)::text").get()
            move["accuracy"] = s.css("td:nth-of-type(6)::text").get()

            moves.append(move)

        return moves

    def parse_moves_egg(self, response):
        moves = []

        selector_moves = response.css(
            'h3:contains("Egg moves") + p + div.resp-scroll table.data-table tbody tr'
        )

        for s in selector_moves:
            move = {}
            move["move"] = s.css("td.cell-name a.ent-name::text").get()
            move["type"] = s.css("td.cell-icon a.type-icon::text").get()
            move["category"] = s.css("td.cell-icon img::attr(alt)").get()
            move["power"] = s.css("td:nth-of-type(4)::text").get()
            move["accuracy"] = s.css("td:nth-of-type(5)::text").get()

            moves.append(move)

        return moves

    def parse_location(self, response):
        selector_location = response.css(
            'h2:contains("Where to find") + div.resp-scroll table.vitals-table tbody tr'
        )
        locations = {}
        for s in selector_location:
            game_names = s.css("th span::text").getall()
            game_names = " / ".join(game_names)

            location = s.css("td a::text").get()
            if not location:
                location = s.css("td small::text").get()

            locations[game_names] = location

        return locations

    def parse_other_languages(self, response):
        selector_language = response.css(
            'h2:contains("Other languages") + div.resp-scroll table.vitals-table tbody tr'
        )
        languages = {}
        for s in selector_language:
            language = s.css("th::text").get()
            name = s.css("td::text").get()
            languages[language] = name

        return languages

    def parse_national_no(self, response):
        return response.css(
            'h2:contains("Pokédex data") + table.vitals-table tbody tr:nth-of-type(1) td strong::text'
        ).get()

    def parse_attributes(self, response):
        data = {}
        selector_attributes = response.css(
            'h2:contains("Pokédex data") + table.vitals-table tbody'
        )

        # Don't get type of mega and regional
        types = selector_attributes.css("tr:nth-of-type(2) td a::text").getall()
        if len(types) == 4:
            data["type"] = types[:2]
        elif len(types) == 2 and types[0] != types[1]:
            data["type"] = types[:2]
        else:
            data["type"] = types[0]

        data["species"] = selector_attributes.css("tr:nth-of-type(3) td::text").get()
        data["height"] = selector_attributes.css("tr:nth-of-type(4) td::text").get()
        data["weight"] = selector_attributes.css("tr:nth-of-type(5) td::text").get()

        abilities = selector_attributes.css("tr:nth-of-type(6) a::text").getall()
        if (len(abilities) >= 2) and (abilities[0] == abilities[1]):
            data["abilities"] = abilities[0]
        else:
            data["abilities"] = abilities[:2]

        return data

    def parse_breeding(self, response):
        breeding = {}
        selector_breeding = response.css(
            'h2:contains("Breeding") + table.vitals-table tbody'
        )

        breeding["egg_groups"] = list(
            set(selector_breeding.css("tr:nth-of-type(1) td a::text").getall())
        )
        breeding["gender_ratio"] = list(
            set(selector_breeding.css("tr:nth-of-type(2) td span::text").getall())
        )

        egg_td_text = selector_breeding.css("tr:nth-child(3) td::text").get()
        egg_small_text = selector_breeding.css("tr:nth-child(3) small::text").get()
        breeding["egg_cycle"] = (
            f"{egg_td_text.strip()} {egg_small_text.strip()}"
            if egg_td_text and egg_small_text
            else None
        )

        return breeding

    def parse_training(self, response):
        training = {}
        selector_training = response.css('h2:contains("Training") + table.vitals-table')

        training["ev_yield"] = (
            selector_training.css("tr:nth-of-type(1) td::text").get().strip()
        )
        training["catch_rate"] = (
            selector_training.css("tr:nth-of-type(2) td::text").get().strip()
        )
        training["base_happiness"] = (
            selector_training.css("tr:nth-of-type(3) td::text").get().strip()
        )
        training["base_exp"] = selector_training.css("tr:nth-of-type(4) td::text").get()
        training["growth_rate"] = selector_training.css(
            "tr:nth-of-type(5) td::text"
        ).get()

        return training

    def parse_stats(self, response):
        stats = {}
        selector_stats = response.css(
            'h2:contains("Base stats") + div.resp-scroll table.vitals-table'
        )

        stats["hp"] = selector_stats.css(
            "tbody tr:nth-child(1) td.cell-num::text"
        ).get()
        stats["attack"] = selector_stats.css(
            "tbody tr:nth-child(2) td.cell-num::text"
        ).get()
        stats["defense"] = selector_stats.css(
            "tbody tr:nth-child(3) td.cell-num::text"
        ).get()
        stats["sp. atk"] = selector_stats.css(
            "tbody tr:nth-child(4) td.cell-num::text"
        ).get()
        stats["sp. def"] = selector_stats.css(
            "tbody tr:nth-child(5) td.cell-num::text"
        ).get()
        stats["speed"] = selector_stats.css(
            "tbody tr:nth-child(6) td.cell-num::text"
        ).get()
        stats["total"] = selector_stats.css(
            "tfoot tr:nth-child(1) td.cell-total::text"
        ).get()

        return stats

    def parse_evolution_chain(self, response):
        return response.css("div.infocard-list-evo a.ent-name::text").getall()

    def parse_artwork(self, response):
        url = response.css("meta[property='og:image']::attr(content)").get()
        return [url] if url else []

    def parse_name(self, response):
        return response.css("h1::text").get()

    def parse(self, response):
        pkm = PokemonItem()

        pkm["name"] = self.parse_name(response)
        pkm["national_no"] = self.parse_national_no(response)
        pkm["attributes"] = self.parse_attributes(response)
        pkm["training"] = self.parse_training(response)
        pkm["breeding"] = self.parse_breeding(response)
        pkm["stats"] = self.parse_stats(response)
        pkm["evolution_chain"] = self.parse_evolution_chain(response)
        pkm["pokedex_entries"] = self.parse_pokedex_entries(response)
        pkm["moves_levelup"] = self.parse_moves_levelup(response)
        pkm["moves_tm"] = self.parse_moves_tm(response)
        pkm["moves_egg"] = self.parse_moves_egg(response)
        pkm["location"] = self.parse_location(response)
        pkm["other_languages"] = self.parse_other_languages(response)
        pkm["artwork_urls"] = self.parse_artwork(response)

        yield pkm

        # Follow the link to the next Pokemon's page
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
