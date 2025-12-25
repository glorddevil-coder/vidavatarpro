from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import os
import tempfile
from app.models.schemas import TricksterEffectRequest, AudioProcessingResponse
from app.services.audio_processor import processor

router = APIRouter(prefix="/api/audio", tags=["audio"])

@router.post("/trickster", response_model=AudioProcessingResponse)
async def apply_trickster_effect(
    request: TricksterEffectRequest,
    background_tasks: BackgroundTasks
):
    """
    Apply Trickster vocal effect to audio.
    
    Applies:
    - Pitch shift: +4 semitones (default)
    - Formant shift: 0.65x (default)
    - Tempo: 1.1x speedup (default)
    """
    try:
        # Create temporary output file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_output:
            output_path = tmp_output.name

        # Download audio from URL (in production, would use signed URLs)
        # For now, assume local file path
        if not os.path.exists(request.audio_url):
            raise HTTPException(status_code=400, detail="Audio file not found")

        # Process audio
        result = await processor.process_async(
            audio_path=request.audio_url,
            output_path=output_path,
            pitch_shift=request.pitch_shift,
            formant_shift=request.formant_shift,
            tempo_rate=request.tempo_rate,
        )

        if result["success"]:
            # In production, upload to S3 and return signed URL
            return AudioProcessingResponse(
                success=True,
                processed_url=output_path,  # Should be S3 URL
                processing_time_ms=0,
            )
        else:
            raise HTTPException(status_code=500, detail=result["error"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload audio file for processing.
    Returns file path for use in Trickster endpoint.
    """
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            contents = await file.read()
            tmp_file.write(contents)
            tmp_file_path = tmp_file.name

        return {
            "filename": file.filename,
            "path": tmp_file_path,
            "size": len(contents),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
