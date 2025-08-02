import asyncio
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from pydantic_models.chat_body import ChatBody
from services.llm_service import LLMService
from services.sort_source_service import SortSourceService
from services.search_service import SearchService


app = FastAPI()

search_service = SearchService()
sort_source_service = SortSourceService()
llm_service = LLMService()


# chat websocket
@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        await asyncio.sleep(0.1)
        data = await websocket.receive_json()
        query = data.get("query")
        print(f"WebSocket - Received query: {query}")
        
        search_results = search_service.web_search(query)
        print(f"WebSocket - Search results found: {len(search_results)} items")
        print(f"WebSocket - Search results: {search_results}")
        
        sorted_results = sort_source_service.sort_sources(query, search_results)
        print(f"WebSocket - Sorted results: {sorted_results}")
        
        await asyncio.sleep(0.1)
        await websocket.send_json({"type": "search_result", "data": sorted_results})
        print(f"WebSocket - Sent search results to client")
        
        for chunk in llm_service.generate_response(query, sorted_results):
            await asyncio.sleep(0.1)
            await websocket.send_json({"type": "content", "data": chunk})
            print(f"WebSocket - Sent chunk: {chunk}")

    except WebSocketDisconnect:
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    finally:
        # Only close if the connection is still open
        if websocket.client_state.value != 3:  # 3 = CLOSED
            try:
                await websocket.close()
            except Exception as e:
                print(f"Error closing WebSocket: {e}")


# chat
@app.post("/chat")
def chat_endpoint(body: ChatBody):
    print(f"POST /chat - Received query: {body.query}")
    
    search_results = search_service.web_search(body.query)
    print(f"POST /chat - Search results found: {len(search_results)} items")
    print(f"POST /chat - Search results: {search_results}")

    sorted_results = sort_source_service.sort_sources(body.query, search_results)
    print(f"POST /chat - Sorted results: {sorted_results}")

    response = llm_service.generate_response(body.query, search_results)
    print(f"POST /chat - Generated response: {response}")

    return response