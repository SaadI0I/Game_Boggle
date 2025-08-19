import pygame
import random

def create_trie_node(): # O(1), Returns a dictionary only
    return {
        'children': {}, # Dictionary to store child nodes, where keys are characters and values are child trie nodes
        'is_end_of_word': False, # Boolean flag to indicate if this node represents the end of a complete word
        'word': None # Stores the actual word string when this node is the end of a word (None otherwise)
    }

def trie_insert(root, word): # O(n), n is the length of the word
   node = root
   for char in word.lower():  # Iterate through each character in the word
       if char not in node['children']:  # Check if current character doesn't exist as a child of current node
           node['children'][char] = create_trie_node()  # Create a new trie node for this character if it doesn't exist
       node = node['children'][char]  # Move to the child node corresponding to current character
   node['is_end_of_word'] = True  # Mark the final node as the end of a complete word
   node['word'] = word.lower()  # Store the complete word (in lowercase) at the final node

def trie_search(root, word): #O(n), n is the length of the word
   node = root
   for char in word.lower():  # Iterate through each character in the word
       if char not in node['children']:  # Check if current character doesn't exist as a child of current node
           return False  # Return False immediately if any character is not found (word doesn't exist)
       node = node['children'][char]  # Move to the child node corresponding to current character
   return node['is_end_of_word']  # Return True if we've reached a node marked as end of word, False otherwise

def trie_traverse(root): # O(n), n is the total number of nodes in the trie
   words = []
   def traverse_helper(node, current_word):
       if node['is_end_of_word']:  # Check if current node marks the end of a complete word
           words.append(current_word)  # Add the complete word to our results list
       for char, child_node in node['children'].items():  # Iterate through all child nodes of current node
           traverse_helper(child_node, current_word + char)  # Recursively traverse each child, building word by adding current character
   traverse_helper(root, "")  # Start the traversal from root with empty string
   return words

def trie_has_prefix(root, prefix):
   node = root
   for char in prefix.lower():  # Iterate through each character in the prefix (converted to lowercase)
       if char not in node['children']:  # Check if current character doesn't exist as a child of current node
           return False  # Return False immediately if any character is not found (prefix doesn't exist)
       node = node['children'][char]  # Move to the child node corresponding to current character
   return True  # Return True if we successfully traversed all characters of the prefix

def create_board(): # Creates a 4x4 grid of letters for the boggle game
    weighted_letters = 'AAABCDEEEEFGHIIIJKLMNOOOPRSSTTUUVWXYZ' # The probability of the letters to appear on the grid
    board = []
    for _ in range(4): # 4x4 matrix initialization
        row = []
        for _ in range(4):
            letter = random.choice(weighted_letters) # Adds letters onto the 4x4 matrix
            row.append(letter)
        board.append(row)
    return board # O(n^2)

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
BOARD_SIZE = 4
CELL_SIZE = 80
BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_SIZE * CELL_SIZE) // 2  # Center horizontally
BOARD_OFFSET_Y = 250  # Position below score/timer area

# Defined Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
GREEN = (0, 150, 0)
RED = (200, 50, 50)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
DARK_GREEN = (0, 100, 0)

# Window Screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Boggle Game")

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Word List
def load_dictionary():
    # Common English words for Boggle
    dictionary_words = [
    "cat", "car", "card", "care", "careful", "dog", "dodge", "art", "are", "ace", "age",
    "bag", "bad", "bat", "bed", "bet", "big", "bit", "bug", "but", "bus", "cut", "cup",
    "can", "cap", "egg", "eat", "end", "eye", "ear", "far", "fat", "fun", "get", "got",
    "hat", "hit", "hot", "ice", "job", "key", "kid", "leg", "let", "map", "mud", "net",
    "new", "old", "pan", "pen", "pet", "pig", "put", "run", "sun", "sit", "six", "tag",
    "tea", "ten", "top", "toy", "use", "van", "web", "win", "yes", "zoo", "the", "and",
    "for", "you", "all", "not", "but", "can", "had", "her", "was", "one", "our", "out",
    "day", "way", "who", "boy", "did", "its", "let", "old", "see", "two", "how", "now",
    "may", "say", "she", "use", "her", "man", "new", "too", "any", "try", "ask", "came",
    "each", "like", "made", "many", "over", "such", "take", "than", "them", "well", "were",
    "about", "above", "after", "again", "against", "along", "always", "among", "another", "around",
    "because", "before", "being", "below", "between", "both", "business", "called", "came", "come",
    "could", "course", "during", "early", "every", "example", "family", "find", "first", "found",
    "general", "getting", "give", "given", "going", "good", "great", "group", "hand", "have",
    "help", "here", "high", "home", "however", "important", "information", "interest", "into", "just",
    "keep", "kind", "know", "large", "last", "later", "life", "little", "local", "long",
    "look", "make", "might", "more", "most", "much", "name", "need", "never", "next",
    "night", "number", "only", "order", "other", "part", "people", "place", "point", "power",
    "problem", "program", "public", "question", "right", "room", "same", "school", "seem", "several",
    "should", "show", "since", "small", "some", "something", "state", "still", "system", "that",
    "there", "these", "they", "thing", "think", "this", "those", "though", "three", "through",
    "time", "today", "together", "under", "until", "upon", "very", "water", "what", "when",
    "where", "which", "while", "will", "with", "within", "without", "work", "world", "would",
    "write", "year", "young", "your", "able", "accept", "access", "account", "across", "action",
    "activity", "actually", "address", "administration", "admit", "adult", "affect", "afford", "afraid", "african",
    "agency", "agent", "agree", "agreement", "ahead", "allow", "almost", "alone", "although", "american",
    "amount", "analysis", "animal", "announce", "annual", "answer", "anyone", "anything", "anywhere", "appear",
    "application", "apply", "approach", "appropriate", "area", "argue", "argument", "arise", "army", "article",
    "artist", "assume", "attack", "attempt", "attend", "attention", "attitude", "attract", "audience", "author",
    "authority", "available", "avoid", "away", "baby", "back", "balance", "ball", "bank", "base",
    "basic", "battle", "bear", "beat", "beautiful", "become", "begin", "behavior", "behind", "believe",
    "benefit", "best", "better", "bill", "billion", "black", "blood", "blue", "board", "body",
    "book", "born", "box", "break", "bring", "brother", "budget", "build", "building", "campaign",
    "cancer", "candidate", "capital", "career", "carry", "case", "catch", "cause", "cell", "center",
    "central", "century", "certain", "certainly", "chair", "challenge", "chance", "change", "character", "charge",
    "check", "child", "choice", "choose", "church", "citizen", "city", "civil", "claim", "class",
    "clear", "clearly", "close", "cold", "collection", "college", "color", "commercial", "common", "community",
    "company", "compare", "computer", "concern", "condition", "conference", "congress", "consider", "consumer", "contain",
    "continue", "control", "cost", "country", "couple", "court", "cover", "create", "crime", "cultural",
    "culture", "current", "customer", "daughter", "dead", "deal", "death", "debate", "decade", "decide",
    "decision", "deep", "defense", "degree", "democratic", "describe", "design", "despite", "detail", "determine",
    "develop", "development", "die", "difference", "different", "difficult", "dinner", "direction", "director", "discover",
    "discuss", "discussion", "disease", "doctor", "door", "down", "draw", "dream", "drive", "drop",
    "drug", "each", "east", "easy", "economic", "economy", "edge", "education", "effect", "effort",
    "eight", "either", "election", "electric", "employee", "energy", "enough", "entire", "environment", "environmental",
    "especially", "establish", "even", "evening", "event", "ever", "everyone", "everything", "evidence", "exactly",
    "examine", "executive", "exist", "expect", "experience", "expert", "explain", "face", "fact", "factor",
    "fail", "fall", "fast", "father", "fear", "federal", "feel", "feeling", "few", "field",
    "fight", "figure", "fill", "film", "final", "finally", "financial", "fine", "fire", "firm",
    "five", "floor", "focus", "follow", "food", "foot", "force", "foreign", "forget", "form",
    "former", "forward", "four", "free", "friend", "from", "front", "full", "fund", "future",
    "game", "garden", "gas", "girl", "glass", "goal", "government", "green", "ground", "grow",
    "growth", "guess", "gun", "guy", "hair", "half", "happen", "happy", "hard", "head",
    "health", "hear", "heart", "heavy", "herself", "history", "hold", "hope", "hospital", "hotel",
    "hour", "house", "human", "hundred", "husband", "idea", "identify", "image", "imagine", "impact",
    "improve", "include", "including", "increase", "indeed", "indicate", "individual", "industry", "inside", "instead",
    "institution", "investment", "involve", "issue", "item", "itself", "join", "kill", "kitchen", "knowledge",
    "land", "language", "late", "law", "lawyer", "lay", "lead", "leader", "learn", "least",
    "leave", "left", "legal", "less", "level", "lie", "line", "list", "listen", "live",
    "loan", "lose", "loss", "lot", "love", "low", "machine", "magazine", "mail", "main",
    "maintain", "major", "management", "manager", "market", "marriage", "material", "matter", "maybe", "mean",
    "measure", "media", "medical", "meet", "meeting", "member", "memory", "mention", "message", "method",
    "middle", "military", "million", "mind", "minute", "miss", "mission", "model", "modern", "moment",
    "money", "month", "morning", "mother", "mouth", "move", "movement", "movie", "music", "must",
    "myself", "nation", "national", "natural", "nature", "near", "nearly", "necessary", "neck", "news",
    "newspaper", "nice", "none", "nor", "north", "note", "nothing", "notice", "nuclear", "obviously",
    "occur", "ocean", "offer", "office", "officer", "official", "often", "once", "open", "operation",
    "opportunity", "option", "organization", "original", "outside", "own", "owner", "page", "pain", "painting",
    "paper", "parent", "park", "participant", "particular", "particularly", "partner", "party", "pass", "past",
    "patient", "pattern", "pay", "peace", "performance", "perhaps", "period", "person", "personal", "phone",
    "physical", "pick", "picture", "piece", "plan", "plant", "play", "player", "please", "pocket",
    "police", "policy", "political", "politics", "poor", "popular", "population", "position", "positive", "possible",
    "practice", "prepare", "present", "president", "pressure", "pretty", "prevent", "price", "private", "probably",
    "process", "produce", "product", "production", "professional", "professor", "provide", "pull", "purpose", "push",
    "quality", "radio", "raise", "range", "rate", "rather", "reach", "read", "ready", "real",
    "reality", "realize", "really", "reason", "receive", "recent", "recently", "recognize", "record", "red",
    "reduce", "reflect", "region", "relate", "relationship", "religious", "remain", "remember", "remove", "report",
    "represent", "republican", "require", "research", "resource", "respond", "response", "responsibility", "rest", "result",
    "return", "reveal", "rich", "rise", "risk", "road", "rock", "role", "rule", "safe",
    "safety", "sale", "save", "scene", "science", "scientist", "score", "sea", "season", "seat",
    "second", "section", "security", "seek", "sell", "send", "senior", "sense", "series", "serious",
    "serve", "service", "set", "seven", "shake", "share", "shoot", "shop", "short", "shot",
    "shoulder", "side", "sign", "significant", "similar", "simple", "simply", "sing", "single", "sister",
    "site", "situation", "size", "skill", "skin", "sky", "sleep", "smile", "social", "society",
    "soldier", "solid", "solution", "solve", "somebody", "someone", "song", "soon", "sort", "sound",
    "source", "south", "southern", "space", "speak", "special", "specific", "spend", "spent", "sport",
    "staff", "stage", "stand", "standard", "start", "station", "stay", "step", "stop", "storage",
    "store", "story", "strategy", "street", "strong", "structure", "student", "study", "stuff", "style",
    "subject", "success", "successful", "suddenly", "suffer", "suggest", "summer", "support", "sure", "surface",
    "table", "talk", "task", "tax", "teach", "teacher", "team", "technology", "television", "tell",
    "term", "test", "text", "theory", "therefore", "third", "thought", "thousand", "threat", "throw",
    "thus", "ticket", "tight", "title", "toward", "town", "trade", "traditional", "training", "travel",
    "treat", "treatment", "tree", "trial", "trip", "trouble", "true", "truth", "turn", "type",
    "understand", "union", "unit", "united", "university", "unless", "usually", "value", "various", "view",
    "violence", "visit", "voice", "vote", "wait", "walk", "wall", "want", "war", "watch",
    "week", "weight", "west", "western", "white", "wide", "wife", "wind", "window", "wish",
    "woman", "wonder", "word", "worker", "working", "worry", "worth", "yard", "yeah", "yellow",
    "able", "about", "above", "accept", "according", "account", "across", "action", "activity", "actually",
    "add", "address", "administration", "admit", "adult", "affect", "after", "again", "against", "age",
    "agency", "agent", "ago", "agree", "agreement", "ahead", "air", "all", "allow", "almost",
    "alone", "along", "already", "also", "although", "always", "american", "among", "amount", "analysis",
    "and", "animal", "another", "answer", "any", "anyone", "anything", "appear", "apply", "approach",
    "area", "argue", "arm", "around", "art", "article", "artist", "ask", "assume", "attack",
    "attention", "attorney", "audience", "author", "authority", "available", "avoid", "away", "baby", "back",
    "bad", "bag", "ball", "bank", "bar", "base", "battle", "beat", "beautiful", "because",
    "become", "bed", "before", "begin", "behavior", "behind", "believe", "benefit", "best", "better",
    "between", "beyond", "big", "bill", "billion", "bit", "black", "blood", "blue", "board",
    "body", "book", "born", "both", "box", "boy", "break", "bring", "brother", "budget",
    "build", "building", "business", "buy", "call", "camera", "campaign", "can", "cancer", "candidate",
    "capital", "car", "card", "care", "career", "carry", "case", "catch", "cause", "cell",
    "center", "central", "century", "certain", "certainly", "chair", "challenge", "chance", "change", "character",
    "charge", "check", "child", "choice", "choose", "church", "citizen", "city", "civil", "claim",
    "class", "clear", "clearly", "close", "coach", "cold", "collection", "college", "color", "come",
    "commercial", "common", "community", "company", "compare", "computer", "concern", "condition", "conference", "congress",
    "consider", "consumer", "contain", "continue", "control", "cost", "could", "country", "couple", "course",
    "court", "cover", "create", "crime", "cultural", "culture", "cup", "current", "customer", "cut",
    "dark", "data", "daughter", "day", "dead", "deal", "death", "debate", "decade", "decide",
    "decision", "deep", "defense", "degree", "democratic", "describe", "design", "despite", "detail", "determine",
    "develop", "development", "die", "difference", "different", "difficult", "dinner", "direction", "director", "discover",
    "discuss", "discussion", "disease", "doctor", "dog", "door", "down", "draw", "dream", "drive",
    "drop", "drug", "during", "each", "early", "east", "easy", "eat", "economic", "economy",
    "edge", "education", "effect", "effort", "eight", "either", "election", "electric", "employee", "end",
    "energy", "enjoy", "enough", "enter", "entire", "environment", "environmental", "especially", "establish", "even",
    "evening", "event", "ever", "every", "everyone", "everything", "evidence", "exactly", "example", "executive",
    "exist", "expect", "experience", "expert", "explain", "eye", "face", "fact", "factor", "fail",
    "fall", "family", "far", "fast", "father", "fear", "federal", "feel", "feeling", "few",
    "field", "fight", "figure", "fill", "film", "final", "finally", "financial", "find", "fine",
    "finger", "finish", "fire", "firm", "first", "fish", "five", "floor", "fly", "focus",
    "follow", "food", "foot", "for", "force", "foreign", "forget", "form", "former", "forward",
    "four", "free", "friend", "from", "front", "full", "fund", "future", "game", "garden",
    "gas", "general", "generation", "get", "girl", "give", "glass", "goal", "god", "good",
    "government", "great", "green", "ground", "group", "grow", "growth", "guess", "gun", "guy",
    "hair", "half", "hand", "hang", "happen", "happy", "hard", "have", "head", "health",
    "hear", "heart", "heat", "heavy", "help", "her", "here", "herself", "high", "him",
    "himself", "his", "history", "hit", "hold", "home", "hope", "hospital", "hot", "hotel",
    "hour", "house", "how", "however", "huge", "human", "hundred", "husband", "idea", "identify",
    "image", "imagine", "impact", "important", "improve", "include", "including", "increase", "indeed", "indicate",
    "individual", "industry", "information", "inside", "instead", "institution", "interest", "international", "interview", "into",
    "investment", "involve", "issue", "item", "its", "itself", "job", "join", "just", "keep",
    "key", "kid", "kill", "kind", "kitchen", "know", "knowledge", "land", "language", "large",
    "last", "late", "later", "laugh", "law", "lawyer", "lay", "lead", "leader", "learn",
    "least", "leave", "left", "leg", "legal", "less", "let", "letter", "level", "lie",
    "life", "light", "like", "likely", "line", "list", "listen", "little", "live", "local",
    "long", "look", "lose", "loss", "lot", "love", "low", "machine", "magazine", "main",
    "maintain", "major", "make", "man", "management", "manager", "many", "market", "marriage", "material",
    "matter", "may", "maybe", "mean", "measure", "media", "medical", "meet", "meeting", "member",
    "memory", "mention", "message", "method", "middle", "might", "military", "million", "mind", "minute",
    "miss", "mission", "model", "modern", "moment", "money", "month", "more", "morning", "most",
    "mother", "mouth", "move", "movement", "movie", "much", "music", "must", "myself", "name",
    "nation", "national", "natural", "nature", "near", "nearly", "necessary", "neck", "need", "network",
    "never", "new", "news", "newspaper", "next", "nice", "night", "nine", "none", "nor",
    "north", "not", "note", "nothing", "notice", "now", "nuclear", "number", "numerous", "object",
    "obviously", "occur", "ocean", "offer", "office", "officer", "official", "often", "old", "once",
    "one", "only", "onto", "open", "operation", "opportunity", "option", "order", "organization", "original",
    "other", "others", "our", "out", "outside", "over", "own", "owner", "page", "pain",
    "painting", "paper", "parent", "park", "part", "participant", "particular", "particularly", "partner", "party",
    "pass", "past", "patient", "pattern", "pay", "peace", "people", "per", "performance", "perhaps",
    "period", "person", "personal", "phone", "physical", "pick", "picture", "piece", "place", "plan",
    "plant", "play", "player", "please", "pocket", "point", "police", "policy", "political", "politics",
    "poor", "popular", "population", "position", "positive", "possible", "power", "practice", "prepare", "present",
    "president", "pressure", "pretty", "prevent", "price", "private", "probably", "problem", "process", "produce",
    "product", "production", "professional", "professor", "program", "project", "property", "protect", "prove", "provide",
    "public", "pull", "purpose", "push", "put", "quality", "question", "quickly", "quite", "race",
    "radio", "raise", "range", "rate", "rather", "rating", "reach", "read", "ready", "real",
    "reality", "realize", "really", "reason", "receive", "recent", "recently", "recognize", "record", "red",
    "reduce", "reflect", "region", "relate", "relationship", "religious", "remain", "remember", "remove", "report",
    "represent", "republican", "require", "research", "resource", "respond", "response", "responsibility", "rest", "result",
    "return", "reveal", "rich", "right", "rise", "risk", "road", "rock", "role", "room",
    "rule", "run", "safe", "same", "save", "say", "scene", "school", "science", "scientist",
    "score", "sea", "season", "seat", "second", "section", "security", "see", "seek", "seem",
    "sell", "send", "senior", "sense", "series", "serious", "serve", "service", "set", "seven",
    "several", "sex", "shake", "share", "she", "shoot", "shop", "short", "shot", "should",
    "shoulder", "show", "side", "sign", "significant", "similar", "simple", "simply", "since", "sing",
    "single", "sister", "sit", "site", "situation", "six", "size", "skill", "skin", "sky",
    "sleep", "small", "smile", "social", "society", "soldier", "solid", "solution", "solve", "some",
    "somebody", "someone", "something", "sometimes", "son", "song", "soon", "sort", "sound", "source",
    "south", "southern", "space", "speak", "special", "specific", "spend", "spent", "sport", "spring",
    "staff", "stage", "stand", "standard", "star", "start", "state", "station", "stay", "step",
    "still", "stock", "stop", "storage", "store", "story", "strategy", "street", "strong", "structure",
    "student", "study", "stuff", "style", "subject", "success", "successful", "such", "suddenly", "suffer",
    "suggest", "summer", "support", "sure", "surface", "system", "table", "take", "talk", "task",
    "tax", "teach", "teacher", "team", "technology", "television", "tell", "ten", "term", "test",
    "text", "than", "thank", "that", "the", "their", "them", "themselves", "then", "theory",
    "there", "therefore", "these", "they", "thing", "think", "third", "this", "those", "though",
    "thought", "thousand", "threat", "three", "through", "throughout", "throw", "thus", "ticket", "tight",
    "time", "title", "today", "together", "tonight", "tool", "top", "total", "tough", "toward",
    "town", "trade", "traditional", "training", "travel", "treat", "treatment", "tree", "trial", "trip",
    "trouble", "true", "truth", "try", "turn", "twelve", "twenty", "two", "type", "under",
    "understand", "union", "unit", "united", "university", "unless", "until", "upon", "use", "used",
    "useful", "user", "using", "usually", "value", "various", "very", "victim", "view", "violence",
    "visit", "voice", "vote", "wait", "walk", "wall", "want", "war", "watch", "water",
    "way", "weapon", "wear", "week", "weight", "well", "west", "western", "what", "whatever",
    "when", "where", "whether", "which", "while", "white", "who", "whole", "whom", "whose",
    "why", "wide", "wife", "will", "win", "wind", "window", "wish", "with", "within",
    "without", "woman", "wonder", "word", "work", "worker", "working", "world", "worry", "worth",
    "would", "write", "writer", "wrong", "yard", "yeah", "year", "yes", "yet", "you",
    "young", "your", "yourself", "zone"
]
    
    root = create_trie_node()
    for word in dictionary_words:
        trie_insert(root, word)
    return root

# Game state variables
board = create_board()
dictionary_root = load_dictionary()
current_path = []
current_word = ""
found_words = []
score = 0
selected_cells = []
game_time = 180
start_time = pygame.time.get_ticks()
game_over = False
all_possible_words = []
game_won = False

def get_neighbors(row, col):
   neighbors = []
   for diagonal_row in [-1, 0, 1]:  # Iterate through row offsets: up (-1), same (0), down (1)
       for diagonal_col in [-1, 0, 1]:  # Iterate through column offsets: left (-1), same (0), right (1)
           if diagonal_row == 0 and diagonal_col == 0:  # Check if we're looking at the current cell itself
               continue  # Skip the current cell (0,0 offset) since it's not a neighbor
           new_row, new_col = row + diagonal_row, col + diagonal_col  # Calculate potential neighbor coordinates
           if 0 <= new_row < 4 and 0 <= new_col < 4:  # Check if neighbor coordinates are within 4x4 grid bounds
               neighbors.append((new_row, new_col))  # Add valid neighbor coordinates to the list
   return neighbors  # Return list of all valid neighboring positions

def is_valid_move(row, col):
   if (row, col) in current_path:  # Check if the target position is already used in the current path
       return False  # Return False if position is already visited (can't reuse cells)
   if not current_path:  # Check if current_path is empty (first move of the game)
       return True  # Return True since any position is valid for the first move
   last_row, last_col = current_path[-1]  # Get the coordinates of the last position in the current path
   neighbors = get_neighbors(last_row, last_col)  # Get all valid neighboring positions of the last position
   return (row, col) in neighbors  # Return True if target position is adjacent to last position, False otherwise

def mouse_click(mouse_pos):
    x, y = mouse_pos
    if (BOARD_OFFSET_X <= x <= BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE and
        BOARD_OFFSET_Y <= y <= BOARD_OFFSET_Y + BOARD_SIZE * CELL_SIZE):
        col = (x - BOARD_OFFSET_X) // CELL_SIZE
        row = (y - BOARD_OFFSET_Y) // CELL_SIZE
        return row, col
    return None, None

def add_to_path(row, col):
   global current_word, current_path  # Declare access to global variables for current word and path
   if is_valid_move(row, col):  # Check if the move to (row, col) is valid using previously defined validation
       current_path.append((row, col))  # Add the new position coordinates to the path list
       current_word += board[row][col].lower()  # Append the letter at this board position to current word (in lowercase)
       return True  # Return True to indicate the move was successfully added
   return False  # Return False if the move was invalid and nothing was added

def submit_word(): 
   global current_word, current_path, found_words, score, game_over, game_won
   
   if len(current_word) >= 3 and current_word not in found_words:  # Check if word is at least 3 letters and hasn't been found before
       if trie_search(dictionary_root, current_word):  # Search the dictionary trie to validate if the word exists
           found_words.append(current_word)  # Add the valid word to the list of found words
           word_score = len(current_word) * 10  # Calculate score based on word length (10 points per letter)
           score += word_score  # Add the word score to the total game score
           print(f"Found word: {current_word} (+{word_score} points)")  # Display success message with word and points earned
           
           if len(found_words) == len(all_possible_words):  # Check if player has found all possible words in the puzzle
               game_over = True  # Set game over flag to true
               game_won = True  # Set game won flag to true
               print("Congratulations! You found all possible words!")  # Display victory message
       else:  # Execute if word is not found in dictionary
           print(f"'{current_word}' is not a valid word")  # Display message indicating invalid word
   current_path = []  # Reset the path coordinates to empty list for next word attempt
   current_word = ""  # Reset the current word string to empty for next word attempt

def clear_path(): # Clears the path made.
    global current_path, current_word
    current_path = []
    current_word = ""

def new_board():
    global board, found_words, score, current_path, current_word, start_time, game_over, all_possible_words, game_won
    board = create_board()
    found_words = []
    score = 0
    current_path = []
    current_word = ""
    start_time = pygame.time.get_ticks()
    game_over = False
    game_won = False
    all_possible_words = get_all_possible_words()
    print(f"New board generated! {len(all_possible_words)} words possible.")

def can_form_word_on_board(word):
   def dfs(word_index, row, col, visited):
       if word_index == len(word):  # Check if we've successfully matched all characters in the word
           return True  # Return True if entire word has been found on the board
       
       neighbors = get_neighbors(row, col)  # Get all valid neighboring positions from current cell
       for i, j in neighbors:  # Iterate through each neighboring cell
           if (i, j) not in visited and board[i][j].lower() == word[word_index]:  # Check if neighbor is unvisited and matches next letter
               new_visited = visited.copy()  # Create a copy of visited cells to avoid modifying original
               new_visited.add((i, j))  # Add current neighbor to the visited set
               if dfs(word_index + 1, i, j, new_visited):  # Recursively search for remaining letters starting from this neighbor
                   return True  # Return True if path to complete word is found
       return False  # Return False if no valid path found from current position
   
   # Try starting from each cell that matches the first letter
   for i in range(4):  # Iterate through all rows in the 4x4 board
       for j in range(4):  # Iterate through all columns in the 4x4 board
           if board[i][j].lower() == word[0]:  # Check if current cell matches the first letter of the word
               if dfs(1, i, j, {(i, j)}):  # Start DFS from this cell, looking for remaining letters (index 1 onwards)
                   return True  # Return True if word can be formed starting from this cell
   return False  # Return False if word cannot be formed starting from any cell on the board

def get_all_possible_words(): 
   all_dictionary_words = trie_traverse(dictionary_root)  # Get complete list of all words stored in the dictionary trie
   possible_words = []  # Initialize empty list to store words that can be formed on the board
   
   # For each dictionary word, check if it can be formed on the board
   for word in all_dictionary_words:  # Iterate through every word in the dictionary
       if len(word) >= 3 and can_form_word_on_board(word):  # Check if word is at least 3 letters and can be traced on board
           possible_words.append(word)  # Add valid word to the list of possible words
   
   return sorted(possible_words)  # Return alphabetically sorted list of all possible words

def show_all_words():
    possible_words = get_all_possible_words()
    print(f"All possible words ({len(possible_words)}):")
    for word in possible_words:
        print(word)

def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = BOARD_OFFSET_X + col * CELL_SIZE
            y = BOARD_OFFSET_Y + row * CELL_SIZE
            
            # Determine cell color
            if (row, col) in current_path:
                color = YELLOW
            else:
                color = WHITE
            
            # Draw cell
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
            
            # Draw letter
            letter = board[row][col]
            text = font_large.render(letter, True, BLACK)
            text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            screen.blit(text, text_rect)

def game_ui():
    # Title
    title = font_large.render("BOGGLE", True, BLACK)
    screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))
    
    if game_over:
        if game_won:
            # Congratulations message for finding all words
            congrats_text = font_large.render("CONGRATULATIONS!", True, GREEN)
            screen.blit(congrats_text, (WINDOW_WIDTH // 2 - congrats_text.get_width() // 2, 80))
            perfect_text = font_medium.render("You found all possible words!", True, GREEN)
            screen.blit(perfect_text, (WINDOW_WIDTH // 2 - perfect_text.get_width() // 2, 120))
            final_score_text = font_medium.render(f"Perfect Score: {score}", True, BLACK)
            screen.blit(final_score_text, (WINDOW_WIDTH // 2 - final_score_text.get_width() // 2, 150))
        else:
            # Game over message when time runs out
            game_over_text = font_large.render("TIME'S UP!", True, RED)
            screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 80))
            final_score_text = font_medium.render(f"Final Score: {score}", True, BLACK)
            screen.blit(final_score_text, (WINDOW_WIDTH // 2 - final_score_text.get_width() // 2, 120))
            
            # Show missed words count
            missed_count = len(all_possible_words) - len(found_words)
            if missed_count > 0:
                missed_text = font_small.render(f"You missed {missed_count} word(s). Press S to see all possible words.", True, RED)
                screen.blit(missed_text, (WINDOW_WIDTH // 2 - missed_text.get_width() // 2, 150))
    else:
        # Score and Timer above the grid
        score_text = font_medium.render(f"Score: {score}", True, GREEN)
        timer_elapsed = (pygame.time.get_ticks() - start_time) // 1000
        remaining = max(0, game_time - timer_elapsed)
        minutes = remaining // 60
        seconds = remaining % 60
        timer_text = font_medium.render(f"Time: {minutes:02d}:{seconds:02d}", True, RED)
        
        # Show progress
        progress_text = font_small.render(f"Words found: {len(found_words)}/{len(all_possible_words)}", True, BLUE)
        
        # Center score, timer, and progress horizontally
        score_x = WINDOW_WIDTH // 2 - score_text.get_width() // 2
        timer_x = WINDOW_WIDTH // 2 - timer_text.get_width() // 2
        progress_x = WINDOW_WIDTH // 2 - progress_text.get_width() // 2
        
        screen.blit(score_text, (score_x, 80))
        screen.blit(timer_text, (timer_x, 110))
        screen.blit(progress_text, (progress_x, 140))
        
        # Current word below score/timer
        word_text = font_medium.render(f"Current Word: {current_word.upper()}", True, BLUE)
        word_x = WINDOW_WIDTH // 2 - word_text.get_width() // 2
        screen.blit(word_text, (word_x, 180))
        
        # Word validation below current word
        if current_word:
            if len(current_word) >= 3:
                if trie_has_prefix(dictionary_root, current_word):
                    if trie_search(dictionary_root, current_word):
                        if current_word not in found_words:
                            status = "Valid word!"
                            color = GREEN
                        else:
                            status = "Already found"
                            color = GRAY
                    else:
                        status = "Has Prefix, but not a word"
                        color = BLUE
                else:
                    status = "Not a word"
                    color = RED
            else:
                status = "Too short"
                color = GRAY
            
            status_text = font_small.render(status, True, color)
            status_x = WINDOW_WIDTH // 2 - status_text.get_width() // 2
            screen.blit(status_text, (status_x, 210))
    
    # Instructions below the grid
    grid_bottom = BOARD_OFFSET_Y + BOARD_SIZE * CELL_SIZE + 30
    
    if not game_over:
        instructions = [
            "Click letters to form words",
            "SPACE: Submit word",
            "BACKSPACE: Clear path",
            "Press N: New board",
            "Press S: Show all words"
        ]
    else:
        instructions = [
            "Press N: New game",
            "Press S: Show all possible words"
        ]
    
    # Center instructions
    for i, instruction in enumerate(instructions):
        if instruction:
            text = font_small.render(instruction, True, BLACK)
            text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
            screen.blit(text, (text_x, grid_bottom + i * 25))
    
    # Found words section - positioned to the right of the grid
    found_words_x = BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE + 50
    found_text = font_medium.render("Found Words:", True, BLACK)
    screen.blit(found_text, (found_words_x, BOARD_OFFSET_Y))
    
    # Display found words
    for i, word in enumerate(found_words[-10:]):  # Show last 10 words
        word_text = font_small.render(f"{word.upper()} ({len(word) * 10} pts)", True, DARK_GREEN)
        screen.blit(word_text, (found_words_x, BOARD_OFFSET_Y + 30 + i * 20))

# Initialize the game with all possible words
all_possible_words = get_all_possible_words()
print(f"Game started! {len(all_possible_words)} words possible on this board.")

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if event.button == 1:  # One Left click
                row, col = mouse_click(event.pos)
                if row is not None and col is not None:
                    add_to_path(row, col) # Add the clicked cell to the path if valid
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                submit_word()
            elif event.key == pygame.K_BACKSPACE and not game_over:
                clear_path()
            elif event.key == pygame.K_n:
                new_board()
            elif event.key == pygame.K_s:
                show_all_words()
    
    # Check if time is up
    if not game_over:
        elapsed = (pygame.time.get_ticks() - start_time) // 1000
        if elapsed >= game_time:
            game_over = True
            print(f"Time's up! Final score: {score}")
            print(f"Words found: {len(found_words)}")
            show_all_words()
    
    # Draw everything
    screen.fill(WHITE)
    draw_board()
    game_ui()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()