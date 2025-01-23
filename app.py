import os
import uuid
from aiohttp import web
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Session, File, Base
from utils import convert_image_to_pdf
from config import  DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Создание таблиц
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Загрузка файла и конвертация
async def upload_file(request):
    data = await request.post()
    file = data['file']
    session_id = data['session_id']
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("converted", exist_ok=True)
    # Сохраняем оригинальный файл
    original_filename = f"uploads/{uuid.uuid4()}_{file.filename}"
    with open(original_filename, 'wb') as f:
        f.write(file.file.read())

    # Конвертируем в PDF
    converted_filename = f"converted/{uuid.uuid4()}.pdf"
    convert_image_to_pdf(original_filename, converted_filename)

    async with async_session() as session:
        # Проверяем, существует ли session_id в таблице sessions
        result = await session.execute(select(Session).where(Session.session_id == session_id))
        existing_session = result.scalars().first()

        # Если session_id не существует, создаем новую запись
        if not existing_session:
            new_session = Session(session_id=session_id)
            session.add(new_session)
            await session.commit()

        # Добавляем запись в таблицу files
        new_file = File(
            session_id=session_id,
            original_filename=original_filename,
            converted_filename=converted_filename
        )
        session.add(new_file)
        await session.commit()

    return web.json_response({"status": "success", "file_id": new_file.id})

# Получение списка файлов
async def list_files(request):
    session_id = request.query.get('session_id')
    async with async_session() as session:
        result = await session.execute(select(File).where(File.session_id == session_id))
        files = result.scalars().all()
        files_data = [{"id": file.id, "original_filename": file.original_filename, "converted_filename": file.converted_filename} for file in files]
    return web.json_response(files_data)

# Скачивание файла
async def download_file(request):
    file_id = request.match_info['file_id']
    file_id = int(file_id)
    file_type = request.query.get('type', 'original')  # 'original' или 'converted'

    async with async_session() as session:
        result = await session.execute(select(File).where(File.id == file_id))
        file = result.scalars().first()
        if not file:
            return web.json_response({"status": "error", "message": "File not found"}, status=404)

        file_path = file.original_filename if file_type == 'original' else file.converted_filename
        if not os.path.exists(file_path):
            return web.json_response({"status": "error", "message": "File not found"}, status=404)

        return web.FileResponse(file_path)

# Инициализация приложения
async def init_app():
    await init_db()
    app = web.Application()
    app.router.add_post('/upload', upload_file)
    app.router.add_get('/files', list_files)
    app.router.add_get('/download/{file_id}', download_file)
    return app

# Запуск приложения
if __name__ == '__main__':
    web.run_app(init_app())