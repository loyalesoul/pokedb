import scrapy
import json
import logging

logger = logging.getLogger(__name__)


class PokemonSpider(scrapy.Spider):
    name = "pokemon"
    start_urls = ["https://pokemondb.net/pokedex/bulbasaur"]

    def parse_egg_cycle(self, response):
        # Select the text of td and small elements separately
        td_text = response.css(
            'h2:contains("Breeding") + table.vitals-table tr:nth-child(3) td::text'
        ).get()
        small_text = response.css(
            'h2:contains("Breeding") + table.vitals-table tr:nth-child(3) small::text'
        ).get()

        # Combine the text into one string
        egg_cycle = (
            f"{td_text.strip()} {small_text.strip()}"
            if td_text and small_text
            else None
        )

        return egg_cycle

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

    def parse(self, response):
        # local_numbers = self.parse_local_numbers(response)
        # Extract the data from the page
        data = {
            "name": response.css("h1::text").get(),
            "national_no": response.css(
                'h2:contains("Pokédex data") + table.vitals-table tr:nth-of-type(1) td strong::text'
            ).get(),
            "type": response.css(
                'h2:contains("Pokédex data") + table.vitals-table tr:nth-of-type(2) td a::text'
            ).getall(),
            "species": response.css(
                'h2:contains("Pokédex data") + table.vitals-table tr:nth-child(3) td::text'
            ).get(),
            "height": response.css(
                'h2:contains("Pokédex data") + table.vitals-table tr:nth-child(4) td::text'
            ).get(),
            "weight": response.css(
                'h2:contains("Pokédex data") + table.vitals-table tr:nth-child(5) td::text'
            ).get(),
            "abilities": response.css(
                'h2:contains("Pokédex data") + table.vitals-table tr:nth-child(6) td a::text'
            ).getall(),
            "ev_yield": response.css(
                'h2:contains("Training") + table.vitals-table tr:nth-child(1) td::text'
            ).get(),
            "catch_rate": response.css(
                'h2:contains("Training") + table.vitals-table tr:nth-child(2) td::text'
            ).get(),
            "base_happiness": response.css(
                'h2:contains("Training") + table.vitals-table tr:nth-child(3) td::text'
            ).get(),
            "base_exp": response.css(
                'h2:contains("Training") + table.vitals-table tr:nth-child(4) td::text'
            ).get(),
            "growth_rate": response.css(
                'h2:contains("Training") + table.vitals-table tr:nth-child(5) td::text'
            ).get(),
            "egg_groups": response.css(
                'h2:contains("Breeding") + table.vitals-table tr:nth-child(1) td a::text'
            ).getall(),
            "gender_ratio": response.css(
                'h2:contains("Breeding") + table.vitals-table tr:nth-child(2) td span::text'
            ).getall(),
            "egg_cycle": self.parse_egg_cycle(response),
            "stats": {
                "hp": response.css(
                    'h2:contains("Base stats") + div.resp-scroll table.vitals-table tbody tr:nth-child(1) td.cell-num::text'
                ).get(),
                "attack": response.css(
                    'h2:contains("Base stats") + div.resp-scroll table.vitals-table tbody tr:nth-child(2) td.cell-num::text'
                ).get(),
                "defense": response.css(
                    'h2:contains("Base stats") + div.resp-scroll table.vitals-table tbody tr:nth-child(3) td.cell-num::text'
                ).get(),
                "sp. atk": response.css(
                    'h2:contains("Base stats") + div.resp-scroll table.vitals-table tbody tr:nth-child(4) td.cell-num::text'
                ).get(),
                "sp. def": response.css(
                    'h2:contains("Base stats") + div.resp-scroll table.vitals-table tbody tr:nth-child(5) td.cell-num::text'
                ).get(),
                "speed": response.css(
                    'h2:contains("Base stats") + div.resp-scroll table.vitals-table tbody tr:nth-child(6) td.cell-num::text'
                ).get(),
                "total": response.css(
                    'h2:contains("Base stats") + div.resp-scroll table.vitals-table tfoot tr:nth-child(1) td.cell-total::text'
                ).get(),
            },
            "evolution_chain": response.css(
                "div.infocard-list-evo a.ent-name::text"
            ).getall(),
            "pokedex_entries": self.parse_pokedex_entries(response),
            "moves_levelup": self.parse_moves_levelup(response),
            "moves_tm": self.parse_moves_tm(response),
            "moves_egg": self.parse_moves_egg(response),
            "location": self.parse_location(response),
            "other_languages": self.parse_other_languages(response),
        }

        # Save the data to a JSON file
        with open(f'pokemon/{data["name"]}.json', "w") as f:
            json.dump(data, f, indent=4)

        # Yield the data to Scrapy
        yield data

        # Follow the link to the next Pokemon's page
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
