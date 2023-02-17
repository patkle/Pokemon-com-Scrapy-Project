import logging

from scrapy import Request, Spider
from w3lib.html import remove_tags


class TCGSpider(Spider):
    name = "tcg"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.pages = int(kwargs.get("pages", 10))

    def start_requests(self):
        for i in range(1, self.pages + 1):
            yield Request(
                f"https://www.pokemon.com/us/pokemon-tcg/pokemon-cards/{i}?cardName=&cardText=&evolvesFrom=&simpleSubmit=&format=unlimited&hitPointsMin=0&hitPointsMax=340&retreatCostMin=0&retreatCostMax=5&totalAttackCostMin=0&totalAttackCostMax=5&particularArtist="
            )

    def parse(self, response):
        for card_link in response.xpath(".//ul[@id='cardResults']/li/a/@href").getall():
            yield response.follow(card_link, callback=self.parse_card)

    def parse_card(self, response):
        card_data = {
            "title": self._get_title(response),
            "card_type": response.xpath(".//div[@class='card-type']/h2/text()").get(),
            "hp": response.xpath(".//span[@class='card-hp']/text()").get(),
            "pokemon_type": response.xpath(
                ".//div[@class='card-basic-info']/div[@class='right']/a/i/@title"
            ).get(),
            "evolves_from": self._get_evolves_from(response),
            "skills": list(self._get_skills(response)),
            "expansion": response.xpath(
                ".//div[@class='stats-footer']/h3/a/text()"
            ).get(),
            "name": response.xpath(".//div[@class='stats-footer']/span/text()").get(),
            "illustrator": response.xpath(
                ".//div[contains(@class, 'illustrator')]/h4/a/text()"
            ).get(),
        }
        card_data["poke_body"] = self._get_poke_body(response)
        card_data["poke_power"] = self._get_poke_power(response)
        card_data.update(self._get_stats(response))
        yield card_data

    def _get_poke_body(self, card):
        has_poke_body = (
            True if card.xpath(".//h3/div[@class='poke-body']/text()") else False
        )
        if not has_poke_body:
            return None

        return {
            "name": card.xpath(
                ".//div[@class='pokemon-abilities']/h3/div[2]/text()"
            ).get(),
            "description": remove_tags(
                card.xpath(".//div[@class='pokemon-abilities']/p").get()
            ),
        }

    def _get_poke_power(self, card):
        has_poke_power = (
            True if card.xpath(".//h3/div[@class='poke-power']/text()") else False
        )
        if not has_poke_power:
            return None

        return {
            "name": card.xpath(
                ".//div[@class='pokemon-abilities']/h3/div[2]/text()"
            ).get(),
            "description": remove_tags(
                card.xpath(".//div[@class='pokemon-abilities']/p").get()
            ),
        }

    def _get_title(self, card):
        title = card.xpath(".//h1").get()
        if title is None:
            logging.critical(card.text)
        title = remove_tags(card.xpath(".//h1").get())
        is_star_card = True if card.xpath(".//h1/img/@alt") else False
        # title = remove_tags(title.get())
        return title + "*" if is_star_card else title

    def _get_evolves_from(self, card):
        evolves_from = card.xpath(".//div[@class='card-basic-info']/div/h4/a").get()
        if isinstance(evolves_from, str):
            evolves_from = remove_tags(evolves_from).strip()
        return evolves_from

    def _is_ability(self, skill) -> bool:
        return True if skill.xpath(".//h3/div[@class='poke-ability']/text()") else False

    def _get_skill_text(self, skill):
        skill_text = skill.xpath("./pre").get()
        if not isinstance(skill_text, str):
            skill_text = skill.xpath(".//p").get()
        if isinstance(skill_text, str):
            skill_text = remove_tags(skill_text)
        return skill_text

    def _get_skill_cost(self, skill):
        return skill.xpath(".//ul/li/@title").getall()

    def _get_skill_name(self, skill):
        skill_name = skill.xpath(".//h4").get()
        if isinstance(skill_name, str):
            skill_name = remove_tags(skill_name)
        return skill_name

    def _get_skills(self, card):
        for skill in card.xpath(".//div[@class='ability']"):
            yield {
                "is_ability": self._is_ability(skill),
                "skill_cost": self._get_skill_cost(skill),
                "skill_name": self._get_skill_name(skill),
                "skill_damage": skill.xpath(
                    ".//span[contains(@class, 'right')]/text()"
                ).get(),
                "skill_text": self._get_skill_text(skill),
            }

    def _get_stats(self, card):
        stats = {}
        for i, stat in enumerate(
            card.xpath(".//div[@class='pokemon-stats']/div[contains(@class, 'stat')]")
        ):
            cost = stat.xpath(".//ul/li/@title").getall()
            txt = stat.xpath(".//ul/li/text()").get()
            stat_text = " ".join(cost) + txt if txt is not None else ""
            stat_text = stat_text.strip()
            if i == 0:
                stats["weakness"] = stat_text
            elif i == 1:
                stats["resistance"] = stat_text
            elif i == 2:
                stats["retreat_cost"] = stat_text
        return stats
