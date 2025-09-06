from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Base de datos simulada del centro comercial
MALL_DATABASE = {
    "stores": {
        "zara": {
            "name": "Zara",
            "location": "Piso 2, Local 201-205",
            "category": "moda",
            "hours": "Lunes a Domingo: 10:00 AM - 10:00 PM",
            "products": ["ropa femenina", "ropa masculina", "accesorios", "zapatos"],
            "description": "Moda contemporánea para hombre y mujer"
        },
        "nike": {
            "name": "Nike",
            "location": "Piso 1, Local 115-118",
            "category": "deportes",
            "hours": "Lunes a Domingo: 10:00 AM - 10:00 PM",
            "products": ["calzado deportivo", "ropa deportiva", "accesorios deportivos"],
            "description": "Todo para el deporte y estilo de vida activo"
        },
        "mcdonald's": {
            "name": "McDonald's",
            "location": "Piso 3, Plazoleta de Comidas",
            "category": "restaurante",
            "hours": "Lunes a Domingo: 7:00 AM - 11:00 PM",
            "products": ["hamburguesas", "papas fritas", "nuggets", "ensaladas", "postres"],
            "description": "Comida rápida internacional"
        },
        "starbucks": {
            "name": "Starbucks",
            "location": "Piso 1, Local 102 (entrada principal)",
            "category": "cafetería",
            "hours": "Lunes a Domingo: 6:00 AM - 11:00 PM",
            "products": ["café", "frappuccinos", "té", "sandwiches", "pasteles"],
            "description": "Café de especialidad y bebidas artesanales"
        },
        "h&m": {
            "name": "H&M",
            "location": "Piso 2, Local 210-215",
            "category": "moda",
            "hours": "Lunes a Domingo: 10:00 AM - 10:00 PM",
            "products": ["ropa casual", "ropa formal", "accesorios", "ropa infantil"],
            "description": "Moda accesible para toda la familia"
        },
        "adidas": {
            "name": "Adidas",
            "location": "Piso 1, Local 120-123",
            "category": "deportes",
            "hours": "Lunes a Domingo: 10:00 AM - 10:00 PM",
            "products": ["calzado deportivo", "ropa deportiva", "equipamiento deportivo"],
            "description": "Marca deportiva líder mundial"
        },
        "apple store": {
            "name": "Apple Store",
            "location": "Piso 2, Local 220-225",
            "category": "tecnología",
            "hours": "Lunes a Domingo: 10:00 AM - 10:00 PM",
            "products": ["iPhone", "iPad", "MacBook", "Apple Watch", "accesorios"],
            "description": "Productos y servicios Apple oficiales"
        }
    },
    "categories": {
        "moda": ["Zara", "H&M", "Forever 21", "Pull & Bear", "Bershka"],
        "deportes": ["Nike", "Adidas", "Puma", "Under Armour", "Reebok"],
        "restaurante": ["McDonald's", "KFC", "Subway", "Domino's Pizza", "Crepes & Waffles"],
        "cafetería": ["Starbucks", "Juan Valdez", "Tostao", "Dunkin' Donuts"],
        "tecnología": ["Apple Store", "Samsung", "Ktronix", "Alkosto", "Éxito Tecnología"],
        "belleza": ["Sephora", "MAC", "L'Oréal", "Bodyshop", "Kiko Milano"],
        "servicios": ["Bancolombia", "Davivienda", "Cruz Verde", "Locatel", "Western Union"]
    }
}

class ActionGetStoreLocation(Action):
    def name(self) -> Text:
        return "action_get_store_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        store_name = tracker.get_slot("store_name")
        if not store_name:
            store_name = next(tracker.get_latest_entity_values("store_name"), None)
        
        if store_name:
            store_key = store_name.lower()
            store_info = MALL_DATABASE["stores"].get(store_key)
            
            if store_info:
                message = f"📍 **{store_info['name']}** se encuentra en:\n{store_info['location']}\n\n{store_info['description']}"
            else:
                message = f"No encontré la tienda '{store_name}' en nuestro directorio. ¿Podrías verificar el nombre o preguntar por nuestro listado completo de tiendas?"
        else:
            message = "¿Qué tienda estás buscando? Puedo ayudarte con la ubicación de cualquiera de nuestras tiendas."
        
        dispatcher.utter_message(text=message)
        return []

class ActionGetStoreHours(Action):
    def name(self) -> Text:
        return "action_get_store_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        store_name = tracker.get_slot("store_name")
        if not store_name:
            store_name = next(tracker.get_latest_entity_values("store_name"), None)
        
        if store_name:
            store_key = store_name.lower()
            store_info = MALL_DATABASE["stores"].get(store_key)
            
            if store_info:
                message = f"🕐 **Horarios de {store_info['name']}:**\n{store_info['hours']}\n\nUbicada en: {store_info['location']}"
            else:
                message = f"No encontré la tienda '{store_name}'. ¿Podrías verificar el nombre?"
        else:
            message = "¿De qué tienda necesitas conocer los horarios?"
        
        dispatcher.utter_message(text=message)
        return []

class ActionGetStoreProducts(Action):
    def name(self) -> Text:
        return "action_get_store_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        store_name = tracker.get_slot("store_name")
        if not store_name:
            store_name = next(tracker.get_latest_entity_values("store_name"), None)
        
        if store_name:
            store_key = store_name.lower()
            store_info = MALL_DATABASE["stores"].get(store_key)
            
            if store_info:
                products_list = ", ".join(store_info['products'])
                message = f"🛍️ **{store_info['name']}** ofrece:\n{products_list}\n\n{store_info['description']}\n📍 Ubicación: {store_info['location']}"
            else:
                message = f"No encontré información sobre los productos de '{store_name}'. ¿Podrías verificar el nombre de la tienda?"
        else:
            message = "¿De qué tienda te gustaría conocer los productos?"
        
        dispatcher.utter_message(text=message)
        return []

class ActionGetCategoryStores(Action):
    def name(self) -> Text:
        return "action_get_category_stores"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extraer la categoría del mensaje del usuario
        user_message = tracker.latest_message.get('text', '').lower()
        
        category_mapping = {
            'ropa': 'moda',
            'moda': 'moda',
            'restaurantes': 'restaurante',
            'comida': 'restaurante',
            'restaurant': 'restaurante',
            'café': 'cafetería',
            'cafeteria': 'cafetería',
            'cafetería': 'cafetería',
            'tecnología': 'tecnología',
            'tecnologia': 'tecnología',
            'deportes': 'deportes',
            'deporte': 'deportes',
            'deportivas': 'deportes',
            'belleza': 'belleza',
            'servicios': 'servicios'
        }
        
        category = None
        for keyword, cat in category_mapping.items():
            if keyword in user_message:
                category = cat
                break
        
        if category and category in MALL_DATABASE["categories"]:
            stores = MALL_DATABASE["categories"][category]
            stores_list = "\n• ".join(stores)
            
            category_names = {
                'moda': 'Tiendas de Moda',
                'restaurante': 'Restaurantes',
                'cafetería': 'Cafeterías',
                'tecnología': 'Tiendas de Tecnología',
                'deportes': 'Tiendas Deportivas',
                'belleza': 'Tiendas de Belleza',
                'servicios': 'Servicios'
            }
            
            message = f"🏪 **{category_names[category]}:**\n• {stores_list}\n\n¿Te interesa información específica de alguna de estas tiendas?"
        else:
            message = "Nuestras categorías disponibles son:\n🛍️ Moda\n🍔 Restaurantes\n☕ Cafeterías\n💻 Tecnología\n⚽ Deportes\n💄 Belleza\n🏦 Servicios\n\n¿Sobre cuál categoría te gustaría saber?"
        
        dispatcher.utter_message(text=message)
        return []