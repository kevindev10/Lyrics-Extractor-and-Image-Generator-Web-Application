from pydantic import BaseModel



class LyricsPayload(BaseModel):
    lyrics: str
