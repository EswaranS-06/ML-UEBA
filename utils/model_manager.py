# model_manager.py
"""
A modern CLI tool for saving and loading NER models to/from Hugging Face Hub.
Author: Your Name
"""
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

import typer
from pathlib import Path
from huggingface_hub import HfApi, upload_folder
from transformers import AutoTokenizer, AutoModelForTokenClassification

app = typer.Typer(help="✨ Model Manager CLI for HuggingFace ✨")


# -------------------------------------------------------------------
# COMMAND 1: SAVE MODEL TO HUGGINGFACE
# -------------------------------------------------------------------
@app.command("save")
def save_model(
    model_path: str = typer.Argument(..., help="Local directory containing your trained model"),
    repo_id: str = typer.Argument(..., help="HuggingFace repo id -> username/model-name"),
    private: bool = typer.Option(False, "--private", help="Upload as private model")
):
    """
    Upload your trained NER model to Hugging Face Hub.
    """
    
    model_dir = Path(PROJECT_ROOT) / model_path
    if not model_dir.exists():
        typer.secho("❌ Error: Model path does not exist!", fg=typer.colors.RED)
        raise typer.Exit()

    typer.secho(f"🚀 Uploading model from: {model_dir}", fg=typer.colors.GREEN)
    typer.secho(f"📡 Destination repo: {repo_id}", fg=typer.colors.CYAN)

    api = HfApi()

    # Create repo if not exist
    api.create_repo(repo_id=repo_id, exist_ok=True, private=private)

    # Upload folder
    upload_folder(
        folder_path=str(model_dir),
        repo_id=repo_id,
        repo_type="model",
    )

    typer.secho("✅ Upload complete!", fg=typer.colors.GREEN, bold=True)


# -------------------------------------------------------------------
# COMMAND 2: PULL (DOWNLOAD) MODEL FROM HUGGINGFACE
# -------------------------------------------------------------------
@app.command("pull")
def pull_model(
    repo_id: str = typer.Argument(..., help="HuggingFace repo id -> username/model-name"),
    output_dir: str = typer.Option("downloaded_model", help="Where the model will be saved locally")
):
    """
    Download a model from HuggingFace Hub.
    """
    print(output_dir, Path(output_dir))
    output_path = Path(output_dir)
    print(output_path, output_dir)

    typer.secho(f"📥 Downloading model: {repo_id}", fg=typer.colors.GREEN)
    

    output_path.mkdir(parents=True, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(repo_id)
    model = AutoModelForTokenClassification.from_pretrained(repo_id)

    tokenizer.save_pretrained(output_path)
    model.save_pretrained(output_path)

    typer.secho(f"✅ Model downloaded to {output_path}", fg=typer.colors.GREEN, bold=True)


# -------------------------------------------------------------------
# MAIN ENTRY
# -------------------------------------------------------------------
if __name__ == "__main__":
    app()



# 🎉 CLI Usage
# 1️⃣ Upload your NER model

# Your trained model folder:

# nlp/bert/model


# Run:

# python model_manager.py save nlp/bert/model your-username/ner-log-model


# Upload as private:

# python model_manager.py save nlp/bert/model your-username/ner-log-model --private

# 2️⃣ Pull (download) a model
# python model_manager.py pull your-username/ner-log-model --output nlp/bert/model


# Result folder:

# ner_model/
#     config.json
#     model.safetensors
#     tokenizer.json
#     ...