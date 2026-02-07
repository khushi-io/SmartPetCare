import random
import re

# =========================================================
# PET TYPE DETECTION
# =========================================================

PET_TYPES = {
    "dog": ["dog", "dogs", "puppy", "puppies"],
    "cat": ["cat", "cats", "kitten", "kittens"],
    "bird": ["bird", "birds", "parrot", "sparrow", "cockatiel"],
    "rabbit": ["rabbit", "rabbits", "bunny", "bunnies"]
}


def detect_pet_type(message: str) -> str:
    for pet, keywords in PET_TYPES.items():
        for word in keywords:
            if re.search(rf"\b{word}\b", message):
                return pet
    return "default"


# =========================================================
# INTENTS (ADVANCED & COMPLETE)
# =========================================================

INTENTS = {

    # ---------------- GREETINGS ----------------
    "greeting": {
        "patterns": [
            "hi", "hello", "hey", "good morning", "good evening"
        ],
        "responses": {
            "default": [
                "👋 Hello! I'm your AI Pet Care Assistant.",
                "Hi there! 🐾 How can I help you with your pet today?",
                "Hey! 😊 Ask me anything about pet care."
            ]
        }
    },

    # ---------------- THANKS ----------------
    "thanks": {
        "patterns": [
            "thanks", "thank you", "thx", "appreciate"
        ],
        "responses": {
            "default": [
                "You're welcome! 😊",
                "Happy to help 🐶🐱",
                "Anytime! Let me know if you need more help."
            ]
        }
    },

    # ---------------- GOODBYE ----------------
    "goodbye": {
        "patterns": [
            "bye", "goodbye", "see you", "exit"
        ],
        "responses": {
            "default": [
                "Goodbye! 👋 Take good care of your pet 🐾",
                "See you soon! 😊",
                "Bye! Come back anytime."
            ]
        }
    },

    # ---------------- FOOD ----------------
    "food": {
        "patterns": [
            "food", "diet", "feed", "feeding", "eat", "eating", "nutrition"
        ],
        "responses": {
            "dog": [
                "Dogs need a balanced diet with protein, carbs, and healthy fats.",
                "Avoid chocolate, grapes, onions, and spicy food for dogs.",
                "Feed adult dogs twice a day with quality dog food."
            ],
            "cat": [
                "Cats require high-protein diets and taurine-rich food.",
                "Avoid giving milk regularly to cats.",
                "Cats should always have access to fresh water."
            ],
            "bird": [
                "Birds need seeds, fruits, vegetables, and fresh water daily.",
                "Avoid avocado and chocolate — they are toxic to birds."
            ],
            "rabbit": [
                "Rabbits should eat hay daily along with fresh vegetables.",
                "Avoid sugary foods and processed treats."
            ],
            "default": [
                "Provide species-appropriate food and clean water.",
                "Consult a veterinarian for a proper diet plan."
            ]
        }
    },

    # ---------------- HEALTH ----------------
    "health": {
        "patterns": [
            "health", "sick", "ill", "vomit", "fever", "pain", "injured", "disease"
        ],
        "responses": {
            "dog": [
                "If a dog is lethargic or vomiting, consult a vet immediately.",
                "Regular deworming and checkups keep dogs healthy."
            ],
            "cat": [
                "Cats hide illness well. Appetite loss is a serious sign.",
                "Regular vaccinations help prevent feline diseases."
            ],
            "bird": [
                "Fluffed feathers or inactivity can signal illness in birds.",
                "Birds are sensitive — seek an avian vet quickly."
            ],
            "rabbit": [
                "Rabbits stop eating when sick — this is an emergency.",
                "Gut health is critical for rabbits."
            ],
            "default": [
                "If your pet shows unusual symptoms, consult a veterinarian.",
                "Early diagnosis prevents serious health issues."
            ]
        }
    },

    # ---------------- GROOMING ----------------
    "grooming": {
        "patterns": [
            "groom", "grooming", "bath", "wash", "fur", "hair", "clean"
        ],
        "responses": {
            "dog": [
                "Dogs should be bathed every 2–4 weeks depending on breed.",
                "Regular brushing reduces shedding and skin problems."
            ],
            "cat": [
                "Cats groom themselves but still need brushing.",
                "Long-haired cats require frequent grooming."
            ],
            "bird": [
                "Birds groom naturally but need clean environments.",
                "Provide shallow water so birds can bathe themselves."
            ],
            "rabbit": [
                "Brush rabbits regularly to prevent hairballs.",
                "Never bathe rabbits — it causes stress."
            ],
            "default": [
                "Regular grooming keeps pets healthy and comfortable."
            ]
        }
    },

    # ---------------- VACCINATION ----------------
    "vaccination": {
        "patterns": [
            "vaccine", "vaccines", "vaccination",
            "vaccinate", "vaccinated",
            "shot", "shots",
            "immunization", "immunize"
        ],
        "responses": {
            "dog": [
                "Dogs need vaccines like rabies, distemper, and parvovirus.",
                "Puppies usually start vaccinations at 6–8 weeks."
            ],
            "cat": [
                "Cats need core vaccines like FVRCP and rabies.",
                "Vaccination protects cats from deadly viruses."
            ],
            "bird": [
                "Some birds require vaccinations depending on species.",
                "Consult an avian vet before vaccinating birds."
            ],
            "rabbit": [
                "Rabbits need vaccines against viral hemorrhagic disease.",
                "Vaccination is essential for rabbit survival."
            ],
            "default": [
                "Vaccinations protect pets from dangerous diseases.",
                "A veterinarian can recommend a proper vaccine schedule."
            ]
        }
    },

    # ---------------- ADOPTION ----------------
    "adoption": {
        "patterns": [
            "adopt", "adoption", "adopting"
        ],
        "responses": {
            "default": [
                "Adopting a pet is a wonderful responsibility ❤️",
                "Check the adoption section to find a pet in need."
            ]
        }
    },

    # ---------------- EMERGENCY ----------------
    "emergency": {
        "patterns": [
            "emergency", "bleeding", "accident", "injury", "unconscious"
        ],
        "responses": {
            "default": [
                "🚨 This is an emergency. Please contact a veterinarian immediately.",
                "Urgent care is required — do not delay veterinary help."
            ]
        }
    }
}


# =========================================================
# MAIN CHATBOT FUNCTION
# =========================================================

def get_chatbot_response(user_message: str) -> str:
    message = user_message.lower()
    pet_type = detect_pet_type(message)

    for intent, data in INTENTS.items():
        for pattern in data["patterns"]:
            if re.search(rf"\b{pattern}\b", message):
                responses = data["responses"].get(
                    pet_type,
                    data["responses"]["default"]
                )
                return random.choice(responses)

    return (
        "🤔 I'm not sure I understood that.\n\n"
        "You can ask about:\n"
        "🍖 Food • 💉 Vaccination • ✂️ Grooming • 🏥 Health • 🐾 Adoption\n\n"
        "Examples:\n"
        "• food for dog\n"
        "• how to vaccinate my cat\n"
        "• grooming tips for bird"
    )
