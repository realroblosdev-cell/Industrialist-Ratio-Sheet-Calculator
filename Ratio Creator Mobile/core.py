import json
import os


class RatioCore:
    def __init__(self, json_path):
        self.json_path = json_path
        self.data = self.load_data()

    def load_data(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # --------------------------------------------------
    # Build list of all craftable items
    # --------------------------------------------------
    def get_all_items(self):
        items = set()

        for machine in self.data.get("machines", {}).values():
            for recipe in machine.get("recipes", []):
                for o in recipe.get("outputs", []):
                    items.add(o["item"])
                for i in recipe.get("inputs", []):
                    items.add(i["item"])

        return sorted(items)

    # --------------------------------------------------
    # Find best recipe producing an item
    # (simple version — you can expand later)
    # --------------------------------------------------
    def find_recipe(self, item_name):
        for machine in self.data.get("machines", {}).values():
            for recipe in machine.get("recipes", []):
                for out in recipe.get("outputs", []):
                    if out["item"] == item_name:
                        return machine, recipe
        return None, None

    # --------------------------------------------------
    # Main calculation entry
    # --------------------------------------------------
    def calculate(self, item_name, target_rate):
        machine, recipe = self.find_recipe(item_name)

        if recipe is None:
            return f"No recipe found for {item_name}"

        duration = recipe.get("duration", 1)

        produced = recipe["outputs"][0]["amount"]
        crafts_per_sec = target_rate / produced

        machines_needed = crafts_per_sec * duration

        result = []
        result.append(f"Item: {item_name}")
        result.append(f"Target rate: {target_rate:.3f}/s")
        result.append("")
        result.append(f"Machine: {machine.get('name','Unknown')}")
        result.append(f"Machines required: {machines_needed:.2f}")
        result.append("")
        result.append("Inputs:")

        for inp in recipe.get("inputs", []):
            rate = inp["amount"] * crafts_per_sec
            result.append(f"  - {inp['item']}: {rate:.3f}/s")

        return "\n".join(result)