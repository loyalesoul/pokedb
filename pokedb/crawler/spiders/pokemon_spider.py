import scrapy
import json
import logging

logger = logging.getLogger(__name__)


class PokemonSpider(scrapy.Spider):
    name = "pokemon"
    start_urls = [
        "https://www.serebii.net/pokedex-sv/bulbasaur/"
    ]  # Replace with your URL containing the provided HTML

    def parse(self, response):
        # Extracting data
        data = {
            "generation_dex": [
                link.xpath(".//text()").get()
                for link in response.xpath('//table[@class="dextab"]/tr/td/a')
            ],
            "picture": {
                "normal_sprite": response.xpath(
                    '//table[@class="dextable"]//img[@alt="Normal Sprite"]/@src'
                ).get(),
                "shiny_sprite": response.xpath(
                    '//table[@class="dextable"]//img[@alt="Shiny Sprite"]/@src'
                ).get(),
            },
            "pokemon_info": {
                "name": response.xpath(
                    '//table[@class="dextable"]//td[@class="fooinfo"][1]/text()'
                ).get(),
                "other_names": {
                    row.xpath("./td[1]/b/text()").get(): row.xpath(
                        "./td[2]/text()"
                    ).get()
                    for row in response.xpath(
                        '//table[@class="dextable"]//td[@class="fooinfo"][2]//tr'
                    )
                },
                "numbers": {
                    row.xpath("./td[1]/b/text()").get(): row.xpath(
                        "./td[2]/text()"
                    ).get()
                    for row in response.xpath(
                        '//table[@class="dextable"]//td[@class="fooinfo"][3]//tr'
                    )
                },
                "gender_ratio": {
                    row.xpath("./td[1]/text()").get(): row.xpath("./td[2]/text()").get()
                    for row in response.xpath(
                        '//table[@class="dextable"]//td[@class="fooinfo"][4]//tr'
                    )
                },
                "types": [
                    img.xpath("./@alt").get()
                    for img in response.xpath(
                        '//table[@class="dextable"]//td[@class="cen"]//img'
                    )
                ],
                "classification": response.xpath(
                    '//table[@class="dextable"]//td[@class="fooinfo"][5]/text()'
                ).get(),
                "height": response.xpath(
                    '//table[@class="dextable"]//td[@class="fooinfo"][6]//text()'
                ).get(),
                "weight": response.xpath(
                    '//table[@class="dextable"]//td[@class="fooinfo"][7]//text()'
                ).get(),
                "capture_rate": response.xpath(
                    '//table[@class="dextable"]//td[@class="fooinfo"][8]//text()'
                ).get(),
                "base_egg_steps": response.xpath(
                    '//table[@class="dextable"]//td[@class="fooinfo"][9]//text()'
                ).get(),
                "abilities": {
                    "primary": response.xpath(
                        '//table[@class="dextable"]//td[@class="fooinfo"][10]/a[1]/text()'
                    ).get(),
                    "secondary": response.xpath(
                        '//table[@class="dextable"]//td[@class="fooinfo"][10]/a[2]/text()'
                    ).get(),
                    "hidden": response.xpath(
                        '//table[@class="dextable"]//td[@class="fooinfo"][10]/i/text()'
                    ).get(),
                },
                "experience_growth": response.xpath(
                    '//table[@class="dextable"]//td[@class="fooinfo"][11]//text()'
                ).get(),
                "base_happiness": response.xpath(
                    '//table[@class="dextable"]//td[@class="fooinfo"][12]//text()'
                ).get(),
                "effort_values_earned": response.xpath(
                    '//table[@class="dextable"]//td[@class="fooinfo"][13]//text()'
                ).get(),
                "can_change_tera_type": response.xpath(
                    '//table[@class="dextable"]//td[@class="fooinfo"][14]//text()'
                ).get(),
                "weakness": {
                    img.xpath("./@alt").get(): row.xpath(
                        "./td[position() > 1]//text()"
                    ).get()
                    for img, row in zip(
                        response.xpath(
                            '//table[@class="dextable"]//tr[@class="footype"]/td[position() <= 18]/a'
                        ),
                        response.xpath(
                            '//table[@class="dextable"]//tr[@class="footype"]/td[position() > 18]'
                        ),
                    )
                },
            },
        }

        # Convert data to JSON format
        json_data = json.dumps(data, ensure_ascii=False, indent=4)

        # Save data to file
        with open("pokemon.json", "w", encoding="utf-8") as f:
            f.write(json_data)

        # Output the JSON data
        yield {"pokemon_data": json_data}
