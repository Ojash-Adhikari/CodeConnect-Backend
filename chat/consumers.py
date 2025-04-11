import json
import random
import string
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class MatchmakingConsumer(AsyncWebsocketConsumer):
    matchmaking_pool = []  # Queue to store waiting users
    active_rooms = {}      # Maps room names to participants
    ready_users = {}       # Tracks ready users per room

    async def connect(self):
        await self.accept()
        self.username = self.scope["query_string"].decode("utf-8").split("=")[-1]
        print(f"User {self.username} connected!")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message")
            username = data.get("username") 

            if data.get("type") == "find_match":
                self.gamemode = data.get("gamemode")
                self.language = data.get("language")

                if self not in MatchmakingConsumer.matchmaking_pool:
                    MatchmakingConsumer.matchmaking_pool.append(self)

                matched_user = None
                for user in MatchmakingConsumer.matchmaking_pool:
                    if user != self and user.gamemode == self.gamemode and user.language == self.language:
                        matched_user = user
                        break

                if matched_user:
                    MatchmakingConsumer.matchmaking_pool.remove(self)
                    MatchmakingConsumer.matchmaking_pool.remove(matched_user)

                    room_id = self.generate_room_id()
                    self.roomGroupName = matched_user.roomGroupName = room_id

                    MatchmakingConsumer.active_rooms[room_id] = [self.username, matched_user.username]

                    await self.start_game_session(room_id)
                    await matched_user.start_game_session(room_id)
                else:
                    print(f"{self.username} is waiting for a match...")

            elif data.get("type") == "ready":
                room_id = data.get("room_id")
                if room_id not in MatchmakingConsumer.ready_users:
                    MatchmakingConsumer.ready_users[room_id] = set()

                MatchmakingConsumer.ready_users[room_id].add(self.username)
                print(f"{self.username} is ready in room {room_id}")

                if len(MatchmakingConsumer.ready_users[room_id]) == 2:
                    # Both users are ready — send questions
                    gamemode = self.gamemode  # Assuming both users have same mode

                    battle_config = {
                        "Ranked": {"questionCount": 1, "timeLimit": 15, "difficulty": "medium"},
                        "Blitz": {"questionCount": 5, "timeLimit": 10, "difficulty": "easy"},
                        "Death": {"questionCount": 1, "timeLimit": 30, "difficulty": "hard"},
                    }.get(gamemode, {"questionCount": 1, "timeLimit": 10, "difficulty": "easy"})

                    questions = await get_questions_from_db(
                        difficulty=battle_config["difficulty"],
                        count=battle_config["questionCount"]
                    )

                    await self.channel_layer.group_send(
                        room_id,
                        {
                            "type": "send_questions",
                            "questions": questions
                        }
                    )
            elif data.get("type") == "sendMessage":
                message = data.get("message")
                username = data.get("username")

                await self.channel_layer.group_send(
                    self.roomGroupName,
                    {
                        "type": "send_message",
                        "message": message,
                        "username": username,
                    }
                )
                print(f"{message} received from {username}")


        except Exception as e:
            print("Error in receive:", e)

    def generate_room_id(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    async def start_game_session(self, room_id):
        self.roomGroupName = room_id
        await self.channel_layer.group_add(room_id, self.channel_name)

        users_in_room = MatchmakingConsumer.active_rooms.get(room_id, [])
        await self.send(text_data=json.dumps({
            "status": "matched",
            "room_id": room_id,
            "users": users_in_room,
            "gamemode": self.gamemode,
            "language": self.language,
            "questionCount": 0,  # frontend gets real count after "send_questions"
            "timeLimit": 0
        }))

    async def disconnect(self, close_code):
        try:
            if hasattr(self, "roomGroupName") and self.roomGroupName in MatchmakingConsumer.active_rooms:
                users_in_room = MatchmakingConsumer.active_rooms[self.roomGroupName]
                if self.username in users_in_room:
                    users_in_room.remove(self.username)

                if users_in_room:
                    remaining_user = users_in_room[0]
                    await self.channel_layer.group_send(
                        self.roomGroupName,
                        {
                            "type": "sendVictory",
                            "winner": remaining_user
                        }
                    )

                del MatchmakingConsumer.active_rooms[self.roomGroupName]

            if hasattr(self, "roomGroupName"):
                await self.channel_layer.group_discard(self.roomGroupName, self.channel_name)
        except Exception as e:
            print("Disconnect error:", e)

    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "receive_message",
            "message": event["message"],
            "username": event["username"],
        }))

    async def sendVictory(self, event):
        await self.send(text_data=json.dumps({"type": "victory"}))

    async def send_questions(self, event):
        questions = event["questions"]
        await self.send(text_data=json.dumps({
            "type": "send_questions",
            "questions": questions
        }))

@sync_to_async
def get_questions_from_db(difficulty, count):
    from chat.models import CachedQuestion  # Lazy import inside function
    questions = CachedQuestion.objects.filter(difficulty=difficulty).order_by('?')[:count]
    return [
        {
            "difficulty": q.difficulty,
            "question": q.question.strip().split('.')[0],
            "answer": q.answer.strip() if q.answer else 'No answer available'
        }
        for q in questions
    ]
