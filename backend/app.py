from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from backend.recommendation_engine import analyze_image, recommend_style

app = FastAPI(title="AI Personal Stylist API")

# Allow CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_color(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")
    try:
        contents = await file.read()
        image_stream = BytesIO(contents)
        results = analyze_image(image_stream)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")

@app.post("/recommend")
async def full_recommendation(file: UploadFile = File(...)):
    """
    Endpoint that returns both color analysis and stylist recommendations.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")
    try:
        contents = await file.read()
        image_stream = BytesIO(contents)
        analysis_results = analyze_image(image_stream)
        recommendation_results = recommend_style(image_stream, analysis_results)
        return {
            "analysis": analysis_results,
            "recommendation": recommendation_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing recommendation: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
