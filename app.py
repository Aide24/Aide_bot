from utils import set_default_commands
from loader import db, scheduler


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    import pytz
    from handlers.users.migraine_diary.recording_time import migraine_record
    from utils.notify_admins import on_startup_notify

    try:
        # db.delete_diary_entries()
        db.create_table_users()
        db.create_table_schedule_migraine()
    except Exception as e:
        print(e)

    #  запуск дневника мигрени
    users = db.select_all_users()
    for user in users:
        if user[4] is not None:
            time = user[4]
            hour = int(f'{time[0]}{time[1]}')
            minute = int(f'{time[3]}{time[4]}')
            job = scheduler.add_job(migraine_record, 'cron', day_of_week='mon-sun', hour=hour, minute=minute,
                                    timezone=pytz.timezone('Europe/Moscow'),
                                    args=(dp, user[0]))
            db.update_user_id_job(id_job=job.id, id=user[0])
            print(user)

    # db.delete_users()
    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
