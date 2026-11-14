import discord
from discord.ext import commands
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- FIX PRO RENDER (Drží port otevřený, aby služba nepadala na timeout) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Meeting Bot is online 24/7!")
    def log_message(self, format, *args):
        pass

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()
# -------------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class MeetingModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Naplánovat meeting")
        
        self.title_input = discord.ui.TextInput(
            label="Nadpis meetingu",
            style=discord.TextStyle.short,
            placeholder="Např. Důležitá porada vedení...",
            required=True,
            max_length=100
        )
        
        self.ping_input = discord.ui.TextInput(
            label="Koho pingnout (role nebo uživatelé)",
            style=discord.TextStyle.short,
            placeholder="Např. @Vedení nebo @everyone...",
            required=True,
            max_length=100
        )

        self.time_input = discord.ui.TextInput(
            label="Kdy se meeting koná",
            style=discord.TextStyle.short,
            placeholder="Např. Zítra ve 20:00...",
            required=True,
            max_length=100
        )

        self.location_input = discord.ui.TextInput(
            label="Kde (místnost / kanál)",
            style=discord.TextStyle.short,
            placeholder="Např. Hlavní hlasovna / Kancelář...",
            required=True,
            max_length=100
        )

        self.content_input = discord.ui.TextInput(
            label="O čem se bude jednat",
            style=discord.TextStyle.paragraph,
            placeholder="Stručný přehled bodů k jednání...",
            required=True,
            max_length=1000
        )

        self.add_item(self.title_input)
        self.add_item(self.ping_input)
        self.add_item(self.time_input)
        self.add_item(self.location_input)
        self.add_item(self.content_input)

    async def on_submit(self, interaction: discord.Interaction):
        meeting_title = self.title_input.value.strip()
        ping_target = self.ping_input.value.strip()
        meeting_time = self.time_input.value.strip()
        meeting_location = self.location
