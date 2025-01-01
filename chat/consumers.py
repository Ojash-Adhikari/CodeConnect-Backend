# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.roomGroupName = "group_chat_gfg"
#         await self.channel_layer.group_add(
#             self.roomGroupName,
#             self.channel_name
#         )
#         await self.accept()
#     async def disconnect(self):
#         await self.channel_layer.group_discard(
#             self.roomGroupName,
#             self.channel_name 
#         )
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         username = text_data_json["username"]
#         await self.channel_layer.group_send(
#             self.roomGroupName,{
#                 "type" : "sendMessage" ,
#                 "message" : message , 
#                 "username" : username ,
#             })
#     async def sendMessage(self , event) : 
#         message = event["message"]
#         username = event["username"]
#         await self.send(text_data = json.dumps({"message":message ,"username":username}))
      
import json
import time
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from sphereEngine.service import SphereEngineAPI  # Adjust the import according to your app structure
from chat import views as view

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()
        print(f"WebSocket connection established for {self.channel_name}")

    async def disconnect(self, close_code):
        print(f"WebSocket connection closed: {close_code}")
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name 
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        username = text_data_json.get("username")
        compiler_id = text_data_json.get("compiler_id")
        version_id = text_data_json.get("version_id")

        print(f"Received message: {text_data_json}")

        # Handle code compilation if necessary
        if message.startswith("compile:"):
            compile_result = await self.handle_code_compilation(message, compiler_id, version_id)
        else:
            compile_result = message  # Regular chat message

        # Send the message to the group, including the compilation result if any
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": compile_result,
                "username": username,
            }
        )

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        print(f"Sending message: {message} from {username}")
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))

    @sync_to_async
    def handle_code_compilation(self, message, compiler_id=None, version_id=None):
        """
        Handles SphereEngine code compilation and fetching the submission result.
        """
        if message.startswith("compile:"):
            # Extract the code and optional compiler_id and version_id
            parts = message.replace("compile:", "").strip().split(";", 2)
            code_to_compile = parts[0].strip()

            # Use the passed compiler_id and version_id, or fallback to defaults
            try:
                compiler_id = int(compiler_id) if compiler_id else 11  # Default to C++ compiler
                version_id = int(version_id) if version_id else 1  # Default to version 1
            except (TypeError, ValueError):
                compiler_id = 11
                version_id = 1

            # Call the SphereEngineAPI for compilation
            api = SphereEngineAPI()
            result = api.compile_code(code_to_compile, compiler_id=compiler_id, version_id=version_id)

            # Extract the compile ID from the result
            compile_id = result.get('id')
            if not compile_id:
                return "Error: Failed to get a compile ID."

            print(f"Compilation request submitted. Compile ID: {compile_id}")

            # Poll for the submission result using the compile ID
            submission_result = None
            for _ in range(15):
                submission = api.get_submission(compile_id)
                print(f"Submission result: {submission}")

                # Check if it's still executing
                if not submission.get('executing', True):
                    if 'result' in submission:
                        submission_result = submission['result']
                        break
                time.sleep(3)  # Sleep for 2 seconds between polls
        
            
            execution = view.fetch_submission_output(compile_id)  
            print(f"Code Execution result: {execution}")

            if not execution:
                    print("Error getting output")
                

            # Check the submission result
            if submission_result and 'status' in submission_result:
                status_name = submission_result['status'].get("name", "").lower()
                if status_name == "accepted":
                    time_taken = submission_result.get("time", "N/A")
                    memory_used = submission_result.get("memory", "N/A")
                    return f"Compilation accepted: Output = {execution} Time = {time_taken}s, Memory = {memory_used}KB"
                else:
                    return f"Compilation failed with status: {submission_result['status']['name']}"
            else:
                return "Error: Could not fetch the submission result in time."

        # Return if the message is not a compilation request
        return "Compilation request invalid."