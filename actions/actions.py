# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import random

class ActionBuscarLibro(Action):
    def name(self) -> Text:
        return "action_buscar_libro"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        titulo = tracker.get_slot("titulo_libro")
        autor = tracker.get_slot("autor")
        
        # Simulamos una base de datos de libros
        libros_db = {
            "cien años de soledad": {
                "autor": "Gabriel García Márquez",
                "disponible": True,
                "ubicacion": "Sección Literatura - Estante L-15",
                "codigo": "LIT-001"
            },
            "1984": {
                "autor": "George Orwell",
                "disponible": False,
                "ubicacion": "Sección Ciencia Ficción - Estante CF-08",
                "codigo": "CF-045",
                "fecha_devolucion": "2024-03-15"
            },
            "el principito": {
                "autor": "Antoine de Saint-Exupéry",
                "disponible": True,
                "ubicacion": "Sección Infantil - Estante I-03",
                "codigo": "INF-012"
            },
            "don quijote": {
                "autor": "Miguel de Cervantes",
                "disponible": True,
                "ubicacion": "Sección Clásicos - Estante C-02",
                "codigo": "CLA-001"
            }
        }
        
        if titulo:
            titulo_lower = titulo.lower()
            if titulo_lower in libros_db:
                libro = libros_db[titulo_lower]
                if libro["disponible"]:
                    mensaje = f"📚 **{titulo.title()}** de {libro['autor']}\n"
                    mensaje += f"✅ **Disponible**\n"
                    mensaje += f"📍 Ubicación: {libro['ubicacion']}\n"
                    mensaje += f"🔢 Código: {libro['codigo']}\n"
                    mensaje += f"¿Te gustaría que te ayude con algo más?"
                else:
                    mensaje = f"📚 **{titulo.title()}** de {libro['autor']}\n"
                    mensaje += f"❌ **No disponible actualmente**\n"
                    mensaje += f"📅 Fecha estimada de devolución: {libro['fecha_devolucion']}\n"
                    mensaje += f"💡 Puedes reservarlo o buscar títulos similares."
                
                dispatcher.utter_message(text=mensaje)
            else:
                dispatcher.utter_message(text=f"Lo siento, no encontré '{titulo}' en nuestro catálogo. ¿Podrías verificar el título o consultar con el bibliotecario?")
        elif autor:
            dispatcher.utter_message(text=f"Buscaré libros de {autor}. Por favor, especifica un título para una búsqueda más precisa.")
        else:
            dispatcher.utter_message(text="Para ayudarte mejor, ¿podrías decirme el título del libro que buscas?")
        
        return []

class ActionUbicacionLibro(Action):
    def name(self) -> Text:
        return "action_ubicacion_libro"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        titulo = tracker.get_slot("titulo_libro")
        autor = tracker.get_slot("autor")
        
        if titulo or autor:
            # Simulamos información de ubicación
            ubicaciones = [
                "🏢 **Planta Baja**: Recepción, Hemeroteca, Sección Infantil",
                "🏢 **Primer Piso**: Literatura, Ciencias Sociales, Referencias",
                "🏢 **Segundo Piso**: Ciencias Exactas, Medicina, Tecnología",
                "🏢 **Tercer Piso**: Salas de estudio, Archivo histórico"
            ]
            
            mensaje = "📍 **Mapa de la biblioteca:**\n\n"
            mensaje += "\n".join(ubicaciones)
            mensaje += "\n\n💡 También puedes usar los mapas interactivos en cada piso o preguntar en el mostrador de información."
            
            dispatcher.utter_message(text=mensaje)
        else:
            dispatcher.utter_message(text="¿Qué libro específico necesitas ubicar? Dame el título o autor para orientarte mejor.")
        
        return []

class ActionRenovarPrestamo(Action):
    def name(self) -> Text:
        return "action_renovar_prestamo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        numero_carnet = tracker.get_slot("numero_carnet")
        
        if numero_carnet:
            # Simulamos verificación de préstamos
            mensaje = f"🔍 Consultando préstamos para carnet {numero_carnet}...\n\n"
            mensaje += "📚 **Préstamos activos:**\n"
            mensaje += "• 'Cien años de soledad' - Vence: 2024-03-20 ✅ Renovado por 15 días más\n"
            mensaje += "• '1984' - Vence: 2024-03-25 ✅ Renovado por 15 días más\n\n"
            mensaje += "✅ **Renovación completada exitosamente**\n"
            mensaje += "📧 Recibirás un email de confirmación.\n"
            mensaje += "⏰ Recuerda devolver antes de las nuevas fechas para evitar multas."
        else:
            mensaje = "Para renovar tu préstamo necesito:\n"
            mensaje += "🎫 Número de carnet de biblioteca\n"
            mensaje += "📞 También puedes llamar al (555) 123-4567\n"
            mensaje += "💻 O renovar online en nuestro sitio web\n\n"
            mensaje += "¿Tienes tu número de carnet?"
        
        dispatcher.utter_message(text=mensaje)
        return []