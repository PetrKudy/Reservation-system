from django.core.management.base import BaseCommand, CommandError
from club.models import ReservationDate, PersonInfo
import schedule
import time
from datetime import date, timedelta
from django.db import connection
import datetime

class Command(BaseCommand):
    help = 'Runs for updating database every-day and delete old records'

    def handle(self, *args, **options):
        print('database_Refresh is ON!')
        def job():
            print( f'updating {datetime.datetime.now()}')
            todays_date = date.today()

            for day_number in range(0,20): #i want to create next 20 days
                check_date = todays_date+ timedelta(days=day_number)

                check_answer = ReservationDate.objects.filter(Date = check_date)# check if date exist if not return empty
                if not check_answer: # if empty
                    ReservationDate(Date= check_date).save() # date created

                    # edit open hours
                    check_date_list = str(check_date).split('-')
                    day_name = datetime.datetime(int(check_date_list[0]), int(check_date_list[1]), int(check_date_list[2])).strftime("%A") #name of day

                    if day_name in ['Monday','Tuesday','Wednesday','Thursday','Friday']: # open from 7 to 22
                        ReservationDate.objects.filter(Date = check_date).update(T6_7 = 'closed', T22_23 = 'closed', T23_24 = 'closed')

                    elif day_name == 'Saturday': # open from 9 to 24
                        ReservationDate.objects.filter(Date = check_date).update(T6_7 = 'closed', T7_8 = 'closed', T8_9 = 'closed')

                    elif day_name =='Sunday': # open from 10 to 20
                        ReservationDate.objects.filter(Date = check_date).update(T6_7 = 'closed', T7_8 = 'closed', T8_9 = 'closed', T20_21 = 'closed', T21_22 = 'closed', T22_23 = 'closed', T23_24 = 'closed')







                # deleting old dates + records


            with connection.cursor() as cursor:
                select_dates_query = f"SELECT  Day_id FROM club_ReservationDate WHERE Date < '{todays_date}' " # should be just one, but in care

                for day_id_to_check in cursor.execute(select_dates_query):
                    delete_person_query = f"DELETE FROM club_PersonInfo WHERE date_id = '{day_id_to_check[0]}'"
                    cursor.execute(delete_person_query)


                delete_date_query = f"DELETE FROM club_ReservationDate WHERE Date < '{todays_date}' "
                cursor.execute(delete_date_query)


        #schedule.every().day.at("00:01").do(job) # 00:01 just be sure its next day
        schedule.every(2).seconds.do(job)

        while True:
            schedule.run_pending()
            time.sleep(1)
