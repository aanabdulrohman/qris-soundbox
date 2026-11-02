import os
from fastapi import FastAPI, HTTPException
from gtts import gTTS

app = FastAPI()

def speak_amount(amount: int):
    text = f"Pembayaran berhasil sebesar {amount:,} rupiah".replace(",", ".")
    print(f"[AUDIO SPEAK] Mengucapkan: '{text}'")
    
    # Generate audio Bahasa Indonesia dari Google TTS
    tts = gTTS(text=text, lang='id')
    filename = "temp_sound.mp3"
    tts.save(filename)
    
    # Putar file mp3 di Ubuntu
    os.system(f"mpg123 -q {filename}")
    
    # Hapus file temporary setelah diputar
    if os.path.exists(filename):
        os.remove(filename)

@app.post("/webhook/payment")
async def receive_payment(data: dict):
    status = data.get("status")
    amount = data.get("amount")
    
    if status == "SUCCESS" and amount:
        print(f"\n[WEBHOOK RECEIVED] Transaksi Berhasil! Nominal: Rp {amount}")
        try:
            speak_amount(int(amount))
        except Exception as e:
            print(f"[ERROR] Gagal memutar suara: {e}")
            
        return {"status": "success", "message": "Virtual soundbox triggered"}
    
    raise HTTPException(status_code=400, detail="Invalid status or amount")
