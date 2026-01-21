FROM nvcr.io/nvidia/physicsnemo/physicsnemo:latest

# Дополнительные пакеты (если нужны для твоего кода)
RUN pip install --no-cache-dir tinycudann e3nn trimesh pyvista

# Копируем код (опционально, если не используешь volume в compose)
# COPY . /workspace
WORKDIR /workspace

CMD ["python", "train.py"]
