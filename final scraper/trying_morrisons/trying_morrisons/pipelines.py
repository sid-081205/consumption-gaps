import sqlite3
from itemadapter import ItemAdapter


class TryingMorrisonsPipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('morrisons_products.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                title TEXT,
                price TEXT,
                link TEXT,
                energy_per_100g TEXT,
                fat_per_100g TEXT,
                saturated_fat_per_100g TEXT,
                protein_per_100g TEXT
            )
        ''')
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT INTO products (category, title, price, link, energy_per_100g, fat_per_100g, saturated_fat_per_100g, protein_per_100g)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('category'),
            item.get('title'),
            item.get('price'),
            item.get('link'),
            item.get('energy_per_100g'),
            item.get('fat_per_100g'),
            item.get('saturated_fat_per_100g'),
            item.get('protein_per_100g')
        ))
        self.connection.commit()
        return item
