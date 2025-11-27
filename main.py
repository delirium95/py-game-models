import json

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main():
    with open("players.json", "r", encoding="utf-8") as f:
        players_data = json.load(f)

    for pdata in players_data:
        # 1️⃣ Race
        race_data = pdata.get("race")
        race, _ = Race.objects.get_or_create(
            name=race_data["name"],
            defaults={"description": race_data.get("description", "")}
        )

        # 2️⃣ Skills
        for skill_data in race_data.get("skills", []):
            Skill.objects.get_or_create(
                name=skill_data["name"],
                defaults={"bonus": skill_data["bonus"], "race": race},
                race=race
            )

        # 3️⃣ Guild (опційно)
        guild_data = pdata.get("guild")
        if guild_data:
            guild, _ = Guild.objects.get_or_create(
                name=guild_data["name"],
                defaults={"description": guild_data.get("description")}
            )
        else:
            guild = None

        # 4️⃣ Player
        Player.objects.get_or_create(
            nickname=pdata["nickname"],
            defaults={
                "email": pdata.get("email", ""),
                "bio": pdata.get("bio", ""),
                "race": race,
                "guild": guild
            }
        )


if __name__ == "__main__":
    main()
