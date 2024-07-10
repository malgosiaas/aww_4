from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import random
import asyncio
from typing import Dict

app = FastAPI()

@app.get("/image")
async def get_image():
    # Randomly decide the outcome
    outcome = random.choice(["success", "error", "large", "delay"])

    if outcome == "error":
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if outcome == "large":
        # Simulate a large image (10MB base64 string)
        large_image = "data:image/jpeg;base64," + "A" * 10 * 1024 * 1024
        return JSONResponse(content={"image": large_image})

    if outcome == "delay":
        await asyncio.sleep(10)  # Simulate a long delay

    # Simulate a successful image fetch
    image = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAAAAAD/..."  # Add a valid base64 image string here
    return JSONResponse(content={"image": image})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
