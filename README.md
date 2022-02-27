# ScheduleReminder
Telegram Bot which notify every day about lesson schedule

---

How to setup environment 

Lunux:

    python3 -m venv env
    source env/bin/activate
    python3 -m pip install -r requirements.txt

Windows:

    python -m venv env
    .\env\Scripts\activate.bat
    python -m pip install -r requirements.txt

For deactivate the Python venv:

    deactivate

* web page with xlsx: https://kpfu.ru/computing-technology/raspisanie 
* xpath to xlsx in web page: //*[@id="ss_content"]/div[2]/div/div/div[1]/div/div[2]/div/p[1]/a
* Jira task board: https://schedulebot.atlassian.net/jira/software/projects/SR/boards/1
* Confluence: https://schedulebot.atlassian.net/wiki/spaces/~799618195/pages/33109/Home
